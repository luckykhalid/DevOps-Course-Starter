import os
from oauthlib.oauth2 import WebApplicationClient
import requests
from todo_app.security.User import User
from flask_login import login_user


class Auth:

    @classmethod
    def init(cls):

        cls.OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID')
        if not cls.OAUTH_CLIENT_ID:
            raise ValueError(
                "No OAUTH_CLIENT_ID set for OAuth calls. Did you follow the setup instructions?")

        cls.OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET')
        if not cls.OAUTH_CLIENT_SECRET:
            raise ValueError(
                "No OAUTH_CLIENT_SECRET set for OAuth calls. Did you follow the setup instructions?")

        cls.OAUTH_AUTHENTICATE_URL = os.environ.get('OAUTH_AUTHENTICATE_URL')
        if not cls.OAUTH_AUTHENTICATE_URL:
            raise ValueError(
                "No OAUTH_AUTHENTICATE_URL set for OAuth calls. Did you follow the setup instructions?")

        cls.OAUTH_ACCESS_TOKEN_URL = os.environ.get('OAUTH_ACCESS_TOKEN_URL')
        if not cls.OAUTH_ACCESS_TOKEN_URL:
            raise ValueError(
                "No OAUTH_ACCESS_TOKEN_URL set for OAuth calls. Did you follow the setup instructions?")

        cls.OAUTH_USER_URL = os.environ.get('OAUTH_USER_URL')
        if not cls.OAUTH_USER_URL:
            raise ValueError(
                "No OAUTH_USER_URL set for OAuth calls. Did you follow the setup instructions?")

        cls.client = WebApplicationClient(cls.OAUTH_CLIENT_ID)

    @classmethod
    def unauthenticated(cls):
        return cls.client.prepare_request_uri(cls.OAUTH_AUTHENTICATE_URL)

    @classmethod
    def login_callback(cls, request):
        # Step 1 Get the code from authenticated client
        code = request.args.get('code')

        # Step 2 Prepare and send the request to get access token
        url, headers, body = cls.client.prepare_token_request(
            cls.OAUTH_ACCESS_TOKEN_URL, code=code)
        headers['Accept'] = 'application/json'
        response = requests.post(url, data=body, headers=headers, auth=(
            cls.OAUTH_CLIENT_ID, cls.OAUTH_CLIENT_SECRET))
        access_token = response.json()['access_token']

        # Step 3 Use the access token to get the authenticated user details
        response = requests.get(cls.OAUTH_USER_URL, headers={
                                'Authorization': f'token {access_token}'})
        github_user = response.json()

        # Step 4 Use the user data and login the user so they are not reauthenticated in every request
        login_name = github_user['login']
        user = User(login_name)
        login_user(user)

    @staticmethod
    def load_user(user_id):
        return User(user_id)
