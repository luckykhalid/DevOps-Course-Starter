from todo_app.data.MongoDbApi import MongoDbApi
from todo_app.ViewModel import ViewModel
from todo_app.data.Items import Items
from flask import Flask, render_template, request, redirect, send_from_directory
from todo_app.flask_config import Config
import os
from flask_login import LoginManager, login_required, login_user, UserMixin, current_user
from oauthlib.oauth2 import WebApplicationClient
import requests


def create_app(db_name=None):
    app = Flask(__name__)
    app.config.from_object(Config())
    MongoDbApi.init(db_name)

    @app.route('/')
    @login_required
    def index():  # pylint:disable=unused-variable
        item_view_model = ViewModel(
            Items.get_items(), Items.get_current_sort_order())
        return render_template('index.html', view_model=item_view_model)

    @app.route('/', methods=['POST'])
    @login_required
    def create_item():  # pylint:disable=unused-variable
        Items.add_item(request.form['title'])
        return redirect('/')

    @app.route('/actions/<action>/<id>')
    @login_required
    def perform_item_action(action, id):  # pylint:disable=unused-variable
        if action == 'doing':
            Items.doing_item(id)
        elif action == 'done':
            Items.done_item(id)

        return redirect('/')

    @app.route('/sortby/<sortby>')
    @login_required
    def sort_by(sortby):  # pylint:disable=unused-variable
        Items.set_current_sort_order(sortby)
        return redirect('/')

    @app.route('/deleteitem/<id>')
    @login_required
    def remove_item(id):  # pylint:disable=unused-variable
        Items.delete_item(id)
        return redirect('/')

    @app.route('/favicon.ico')
    def favicon():  # pylint:disable=unused-variable
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        client = WebApplicationClient('29b6ec30f353fd737024')
        return redirect(client.prepare_request_uri('https://github.com/login/oauth/authorize', redirect_uri='http://127.0.0.1:5000/login/callback'))

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route('/login/callback')
    def login_callback():  # pylint:disable=unused-variable
        code = request.args.get('code')
        client = WebApplicationClient('29b6ec30f353fd737024')

        url, headers, body = client.prepare_token_request(
            'https://github.com/login/oauth/access_token', code=code)
        headers['Accept'] = 'application/json'
        response = requests.post(url, data=body, headers=headers, auth=(
            '29b6ec30f353fd737024', '33b3e83b42f9c4c27e7d7cd78947c17001aedb03'))
        access_token = response.json()['access_token']
        response = requests.get('https://api.github.com/user',
                                headers={'Authorization': f'token {access_token}'})
        github_user = response.json()
        login_name = github_user['login']
        user = User(login_name)
        login_user(user)

        return redirect('/')

    login_manager.init_app(app)

    return app


class User(UserMixin):
    def __init__(self, login_name):
        self.id = login_name
