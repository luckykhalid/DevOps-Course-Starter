FROM python:3.9-slim
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
WORKDIR /app
COPY . .
ENV PATH="/root/.poetry/bin:$PATH"
RUN poetry install
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

