FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl && apt-get install -y libatomic1 && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root

COPY . /app/

CMD ["poetry", "run", "python", "app/queue_listener.py"]
