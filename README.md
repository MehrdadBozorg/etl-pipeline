# ETL Pipeline with Data Quality Controls

This repository contains a Python-based ETL (Extract, Transform, Load) pipeline designed to extract data from a CSV file, clean and transform it, and load it into a PostgreSQL database. It also includes basic data quality checks, logging any inconsistencies or issues during the ETL process.

## Project Overview

The main objective of this project is to create an ETL pipeline that:

- **Extracts** data from a CSV file.
- **Transforms** the data by:
  - Standardizing date formats.
  - Handling missing values appropriately.
  - Removing duplicate records.
  - Validating data types (ensuring numeric fields contain only numbers).
- **Loads** the cleaned data into a PostgreSQL database.
- Implements **data quality controls** with logging for any inconsistencies.

## Prerequisites

Before running the pipeline, ensure you have the following:

- **Python**: Version 3.11 or above
- **Docker**: To run the PostgreSQL database container and application

## Getting Started

### Clone the Repository

1- Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/etl-pipeline.git
cd etl-pipeline
```

2- Revise the `docker-compose.yml` and replace your_username, your_password, and your_database with your database connection data.  

### Setup
1- **Build docker image:** 

run this command in the root of repository:

```bash
docker build --no-cache -t etl-pipeline .
```

2- **Build docker image:** 
If you like to only make the docker image run this command in the root of repository:

```bash
docker build --no-cache -t etl-pipeline .
```

**Run the containers:**
Run this command to connect to database (the command build image and keep the container running.)
```bash
docker-compose up --build
```

### Run the app and testing

1- **Run the application:**
Run this command to run the application:
```bash
docker-compose run app
```

2-Run this command to get into the postgres container bash:
```bash
docker exec -it postgres_db bash
```

3- Inside postgres container bash run the following command with your user name and database name to connect the database:
```bash
psql -U your_user -d your_database
```

4- Run `\dt` to see the list of tables.

5- Run this query to see the 10 first saved records in the database:
```bash
SELECT * FROM transformed_data LIMIT 10;
```

6- run `\q` to quit the database.

7- run `exit` to quit the bash.


## Contributing

Pull requests are welcome! Please open an issue for feature requests or bug reports.

## License

This project is licensed under the MIT License.