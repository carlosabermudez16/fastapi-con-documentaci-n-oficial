FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install --no-cache-dir uv

# Copiar todo lo necesario para build
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY README.md ./

# Ahora sí
RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]