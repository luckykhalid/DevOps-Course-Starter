FROM python:3.9-slim as base
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
WORKDIR /app
ENV PATH="/root/.poetry/bin:$PATH"
EXPOSE 5000

FROM base as dev
COPY . .
RUN rm -r tests tests_e2e && poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

FROM base as test
RUN apt-get install -y wget bzip2 && \
    wget -O ~/FirefoxSetup.tar.bz2 "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-GB" && \
    tar xjf ~/FirefoxSetup.tar.bz2 -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/lib/firefox && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz && \
    tar -xvzf geckodriver* && \
    chmod +x geckodriver
COPY . .
RUN poetry install
ENV PATH="/app:$PATH"
ENTRYPOINT ["poetry", "run", "pytest"]

FROM base as prod
COPY . .
RUN rm -r tests tests_e2e && poetry install --no-dev
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "todo_app.app:create_app()"]

