FROM python:3.11

WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && export PATH="$HOME/.local/bin:$PATH" \
    && poetry --version

ENV PATH="/root/.local/bin:$PATH"

# Copy Poetry files first for better caching
COPY pyproject.toml poetry.lock ./

# Install dependencies (without any unnecessary flags)
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

CMD ["poetry", "run", "python", "script.py"]
