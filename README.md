# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

### Setup Poetry
The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```
#### Troubleshoot Poetry
In case VS Code is not able to locate Python from your virtual environment then you can find its location by running following shell command:
```bash
$ poetry show -v
```
This should show current installed location of the virtual environment. Please select Python from this location.

If the above command throws an error then the virtual environment might have gotten corrupted in which case its best to remove and recreate it by running following commands:
```bash
$ poetry env remove python
$ poetry install
```
### Setup Environment Configuration
You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.


### Create a Trello account and API key

We're going to be using Trello's API to fetch and save to-do tasks. In order to call their API, you need to first [create an account](https://trello.com/signup) then generate an API key and token by following the [instructions here](https://trello.com/app-key).

Update the `.env` file with Trello's API Key, Token and Board Id against these variables `TRELLO_KEY`, `TRELLO_TOKEN` and `BOARD_ID`. Make sure board being used has 3 lists named `To Do`, `Doing` and `Done`.

You can read the documentation for Trello's REST API [here](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/).


## Running the App Locally
### Running Locally in dev mode Without VM
Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Running locally in prod mode without VM
```bash
poetry run gunicorn -b 127.0.0.1:5000 "todo_app.app:create_app()"
```
### Running the App inside VM

 * Install [`Virtual Box`](https://www.virtualbox.org/)
 * Install [`Vagrant`](https://www.vagrantup.com/)
 * Run this command `vagrant up` to start VM running this To Do app available at [`http://localhost:5000/`](http://localhost:5000/).
 
 Some useful Vagrant commands are:
 ```bash
 * "vagrant up" - Starts your VM, creating and provisioning it automatically if required.
 * "vagrant provision" - Runs any VM provisioning steps specified in the Vagrantfile. Provisioning steps are one-off operations that adjust the system provided by the box.
 * "vagrant suspend" - Suspends any running VM. The VM will be restarted on the next vagrant up command.
 * "vagrant destroy" - Destroys the VM. It will be fully recreated the next time you run vagrant up.
 * "vagrant halt" - Gracefully shuts down the VM.
 * "vagrant ssh" - Ssh into the VM.

```
## Running the App inside Docker Container

### Run with flask in Dev Mode
Use following docker commands to build and run docker container in `dev` mode
```bash
 docker build --target dev --tag todo_app:dev .
 docker run -d -p 5000:5000 --env-file ./.env --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo_app:dev
```
Or simply run following command
```bash
 docker-compose up -d
```
 ### Run tests in tests docker container
Use following docker commands to build and run docker container in `test` mode
```bash
 docker build --target test --tag todo_app:test .
 docker run  --env-file .env.test todo_app:test tests # (unit/integration tests)
 docker run  --env-file .env todo_app:test tests_e2e # (end to end tests)
```
### Run with Gunicorn in Production mode
Use following docker commands to build and run docker container in `prod` mode
```bash
 docker build --target prod --tag todo_app:prod .
 docker run -d -p 5000:5000 --env-file ./.env todo_app:prod
```
NOTE:
 * To view the container logs, you'll need to use `docker logs <CONTAINER>` or remove `-d` flag from docker run/up commands.
 * `Gunicorn` does not run on Windows so any attempt to run it locally on Windows will fail.

## Running Tests Locally
### Unit and Integration Tests
You can run both unit and integration tests suites using pytest. Run this from the root directory:

`$ poetry run pytest tests`

Or you can run them from VSCode:

Click the conical flask icon on the activity bar on the left edge of VSCode. Click the refresh icon at the top of the panel to rediscover tests. Click the play icon at the top to run all tests. Click the play icon next to a file or test name to run that file or test individually.
* Intellisense annotations for running/debugging each test should also appear above the test functions in the code.
* If test discovery fails, check that Poetry has installed your dependencies and that the Python interpreter is selected correctly - you should be using the executable from the .venv folder.

### End to End Tests
You can run End to End tests suites using pytest. Check following dependencies are met:
* Chrome is installed on your system
* [`Chrome Driver`](https://sites.google.com/chromium.org/driver/downloads?authuser=0) is available ideally in the system/path or at least in the project folder.

Run this from the root directory:

`$ poetry run pytest tests_e2e`

Or you can change the `tests` folder configered in `.vscode/settings.json` to `tests_e2e` and then run the tests from VSCode.

NOTE: Do not run E2E tests when web application is also running as this will interfere with the environment variables resulting in inocrrect test execution.

## Setting up CI/CD with Travis
### One Time Travis Setup
Follow these steps once to setup CI/CD pipeline with [`Travis CI`](https://travis-ci.com/):
 1. Go to [`Travis CI`](https://travis-ci.com/) and Sign up with GitHub. 
 2. Accept the Authorization of Travis CI. You’ll be redirected to GitHub.
 3. Click on your profile picture in the top right of your Travis Dashboard, click Settings and then the green Activate button, and select the repositories you want to use with Travis CI.
 4. To use Travis commands locally, such as to encrypt environment variables, install [`Ruby Gem`](https://rubyinstaller.org/downloads/) using default settings.
 5. Test gem has been installed correctly by running this command: `gem -v`
 6. Install Travis locally by running this command:
    `gem install travis`
 7. Login to Travis using GitHub token by running following command:
 ```bash
    travis login --pro --github-token GIT_HUB_TOKEN # replace GIT_HUB_TOKEN with actual token
 ```
 8. Encrypt secrets and add them to the `.travis.yml` file by running following command for each secret:
 ```bash
    travis encrypt --pro VAR1="VAR1_VALUE" --add # replace VAR1 and VAR1_VALUE with actual key/value pair
 ```
 ### One Time Travis Setup
  * All notifications are sent to Slack channel. Recofnigure `.travis.yml` file to send notification to your own channel(s) if desired.
  * Failure notifications are sent to email addresses configured in the `.travis.yml` file. Change as desired.