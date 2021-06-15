import os
from dotenv import find_dotenv, load_dotenv

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')

    def __init__(self) -> None:
        # Load environment variables from .env file for Prod WSGI web server gunicorn (not required for dev env flask run)
        file_path = find_dotenv('.env')
        load_dotenv(file_path, override=True)

        """Base configuration variables."""
        SECRET_KEY = os.environ.get('SECRET_KEY')
        if not SECRET_KEY:
            raise ValueError(
                "No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
