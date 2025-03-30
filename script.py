import pandas as pd
from sqlalchemy import create_engine
from dateutil import parser
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(filename='etl_pipeline.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_data(file_path: Path):
    logging.info(f"Extracting data from {file_path}")
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        raise

def convert_to_standard_date(date_str):
    try:
        return parser.parse(str(date_str)).strftime('%Y-%m-%d')  # Convert to string to avoid issues
    except Exception as e:
        logging.warning(f"Date parsing failed for value {date_str}: {e}")
        return None  # Return None if the date format is invalid

def transform_data(df):
    logging.info("Starting data transformation.")
    
    # Standardize date formats
    df['Date'] = df['Date'].apply(lambda x: convert_to_standard_date(x))
    
    # Identify column types
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=['number', 'datetime']).columns.tolist()

    # Fill numeric missing values with the mean of their respective columns
    for col in numeric_cols:
        if df[col].isnull().any():
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)
            logging.info(f"Filled missing values in numeric column '{col}' with mean value: {mean_value}")

    # Fill categorical/text missing values with the most frequent value
    for col in categorical_cols:
        if df[col].isnull().any():
            most_frequent = df[col].mode().iloc[0]  # Get the most frequent value
            df[col].fillna(str(most_frequent), inplace=True)
            logging.info(f"Filled missing values in categorical column '{col}' with most frequent value: {most_frequent}")
    
    # Remove duplicates
    initial_row_count = len(df)
    df.drop_duplicates(inplace=True)
    logging.info(f"Removed {initial_row_count - len(df)} duplicate rows.")
    
    return df

def load_data(df, db_url):
    logging.info("Starting data load into PostgreSQL.")
    try:
        engine = create_engine(db_url)
        df.to_sql('transformed_data', engine, if_exists='replace', index=False)
        logging.info('Data loaded successfully into PostgreSQL.')
    except Exception as e:
        logging.error(f"Error loading data into PostgreSQL: {e}")
        raise

def main():
    load_dotenv()

    db_url = os.getenv('DB_URL')
    if not db_url:
        logging.error("DB_URL environment variable is not set!")
        raise ValueError("DB_URL is required to connect to the database.")
    
    logging.info(f"Using DB_URL: {db_url}")
    
    # Extract
    data_path = Path(os.getenv('DATA_PATH', 'data/input_data.csv'))  # Use an environment variable for the path
    logging.info(f"Extracting data from {data_path}")
    df = extract_data(data_path)
    
    # Transform
    df = transform_data(df)
    
    # Load
    load_data(df, db_url)
    
    logging.info('ETL process completed successfully.')

if __name__ == "__main__":
    main()
