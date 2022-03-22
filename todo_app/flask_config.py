import os


class Config:

    def __init__(self) -> None:
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError(
                "No SECRET_KEY set for Flask application. Did you follow the setup instructions?")

        self.LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED')

        self.LOG_LEVEL = os.environ.get('LOG_LEVEL')
        if not self.LOG_LEVEL:
            raise ValueError(
                "No LOG_LEVEL set for Flask application. Did you follow the setup instructions?")
        
        self.LOGGLY_TOKEN = os.environ.get('LOGGLY_TOKEN')
        if not self.LOGGLY_TOKEN:
            raise ValueError(
                "No LOGGLY_TOKEN set for Flask application. Did you follow the setup instructions?")
