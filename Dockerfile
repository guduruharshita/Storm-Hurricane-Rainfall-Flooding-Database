FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

COPY pyproject.toml .
RUN pip install --upgrade pip && pip install -e .

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
COPY src ./src

USER appuser
EXPOSE 8000
CMD ["uvicorn", "storm_db.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
