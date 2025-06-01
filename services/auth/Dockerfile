FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8000


CMD ["uvicorn", "shop.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]