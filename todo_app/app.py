from flask_login.mixins import AnonymousUserMixin
from todo_app.data.MongoDbApi import MongoDbApi
from todo_app.ViewModel import ViewModel
from todo_app.data.Items import Items
from flask import Flask, render_template, request, redirect, send_from_directory
from todo_app.flask_config import Config
import os
from flask_login import LoginManager, login_required, current_user
from todo_app.security.Auth import Auth


def create_app(db_name=None):
    app = Flask(__name__)
    app.config.from_object(Config())
    MongoDbApi.init(db_name)
    Auth.init()

    @app.route('/')
    @login_required
    def index():  # pylint:disable=unused-variable
        item_view_model = None
        if app.config['LOGIN_DISABLED']:
            item_view_model = ViewModel(
                Items.get_items(), Items.get_current_sort_order(), True)
        else:
            item_view_model = ViewModel(Items.get_items(
            ), Items.get_current_sort_order(), current_user.has_write_permission())
        return render_template('index.html', view_model=item_view_model)

    @app.route('/', methods=['POST'])
    @login_required
    def create_item():  # pylint:disable=unused-variable
        if current_user.has_write_permission():
            Items.add_item(request.form['title'])
        return redirect('/')

    @app.route('/actions/<action>/<id>')
    @login_required
    def perform_item_action(action, id):  # pylint:disable=unused-variable
        if current_user.has_write_permission():
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
        if current_user.has_write_permission():
            Items.delete_item(id)
        return redirect('/')

    @app.route('/favicon.ico')
    def favicon():  # pylint:disable=unused-variable
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(Auth.unauthenticated())

    @login_manager.user_loader
    def load_user(user_id):
        return Auth.load_user(user_id)

    @app.route('/login/callback')
    def login_callback():  # pylint:disable=unused-variable
        Auth.login_callback(request)
        return redirect('/')

    login_manager.init_app(app)

    return app
