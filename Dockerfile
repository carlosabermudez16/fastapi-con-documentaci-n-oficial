FROM python:3.11-slim

#ADD https://astral.sh/uv/install.sh /install.sh
#RUN chmo -R 755 /install.sh && /install.sh && rm /install.sh

#ENV PATH="/root/.local/bin:${PATH}" 

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

#ENV PATH="/src/app/.venv/bin:{$PATH}"

EXPOSE 8000
#EXPOSE $PORT

CMD ["uv", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]