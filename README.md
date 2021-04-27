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

### Setup Enviuronment Configuration
You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.


### Create a Trello account and API key

We're going to be using Trello's API to fetch and save to-do tasks. In order to call their API, you need to first [create an account](https://trello.com/signup) then generate an API key and token by following the [instructions here](https://trello.com/app-key).

Update the `.env` file with Trello's API Key, Token and Board Id against these variables `TRELLO_KEY`, `TRELLO_TOKEN` and `BOARD_ID`. Make sure board being used has 3 lists named `To Do`, `Doing` and `Done`.

You can read the documentation for Trello's REST API [here](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/).


## Running the App
### Running Locally Without VM
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

### Running Locally Inside VM

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

## Tests

### Unit and Integration Tests
You can run both unit and integration tests suites using pytest. Run this from the root directory:

`$ poetry run pytest`

Or you can run them from VSCode:

Click the conical flask icon on the activity bar on the left edge of VSCode. Click the refresh icon at the top of the panel to rediscover tests. Click the play icon at the top to run all tests. Click the play icon next to a file or test name to run that file or test individually.
* Intellisense annotations for running/debugging each test should also appear above the test functions in the code.
* If test discovery fails, check that Poetry has installed your dependencies and that the Python interpreter is selected correctly - you should be using the executable from the .venv folder.

### End to End Tests
You can run End to End tests suites using pytest. Run this from the root directory:

`$ poetry run pytest tests_e2e`

Or you can change the `tests` folder configered in `.vscode/settings.json` to `tests_e2e` and then run the tests from VSCode.

NOTE: Do not run E2E tests when web application is also running as this will interfere with the environment variables resulting in inocrrect test execution.