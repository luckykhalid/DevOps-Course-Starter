FROM python:3.9-slim as base
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
WORKDIR /app
COPY . .
ENV PATH="/root/.poetry/bin:$PATH"
EXPOSE 5000

FROM base as dev
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

FROM base as prod
RUN poetry install --no-dev
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "todo_app.app:create_app()"]

