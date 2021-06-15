import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')

    def __init__(self) -> None:
        """Base configuration variables."""
        SECRET_KEY = os.environ.get('SECRET_KEY')
        if not SECRET_KEY:
            raise ValueError(
                "No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
