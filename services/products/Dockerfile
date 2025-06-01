FROM python:3.12-slim

LABEL description="FastAPI Products Microservice"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         gcc \
         libpq-dev \
         curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry


COPY pyproject.toml poetry.lock /app/

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry"
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY app/ /app/app/

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

USER appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
