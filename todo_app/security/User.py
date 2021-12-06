from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, login_name):
        self.id = login_name
