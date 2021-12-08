from flask_login import UserMixin
import os
from todo_app.security.Roles import Roles


class User(UserMixin):
    def __init__(self, login_name):
        self.id = login_name

        writer_role_users = os.environ.get('ROLE_WRITER_USERS')

        if login_name in writer_role_users.split(','):
            self.role = Roles.WRITER
        else:
            self.role = Roles.READER

    def has_write_permission(self):
        return self.role == Roles.WRITER
