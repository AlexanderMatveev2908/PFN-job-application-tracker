# ——————————————————————————————————————————————————————
# 🛠️ 0 — install packages and build wheel 
# ——————————————————————————————————————————————————————

FROM  python:3.12-slim AS builder

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

RUN curl -L https://install.python-poetry.org | python3

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock README.md ./
COPY ./src ./src

ENV POETRY_HTTP_RETRIES=10
ENV POETRY_HTTP_TIMEOUT=600

RUN poetry install --no-root

RUN poetry build -f wheel

# ——————————————————————————————————————————————————————
# 🚀 0 — install wheel && ext pkg for deploy 
# ——————————————————————————————————————————————————————

FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    rm -rf /var/lib/apt/lists/*
    
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

COPY --from=builder /app/dist/*.whl .

RUN pip install --upgrade pip && pip install *.whl

EXPOSE 3000

CMD ["gunicorn", "src.server:app", "-w", "8", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:3000"]