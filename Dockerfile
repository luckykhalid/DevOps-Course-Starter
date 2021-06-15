FROM python:3.9-slim
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
WORKDIR /app
COPY . .
ENV PATH="/root/.poetry/bin:$PATH"
RUN poetry install --no-dev
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "todo_app.app:create_app()"]

