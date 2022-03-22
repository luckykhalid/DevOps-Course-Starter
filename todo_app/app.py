from flask_login.mixins import AnonymousUserMixin
from todo_app.data.MongoDbApi import MongoDbApi
from todo_app.ViewModel import ViewModel
from todo_app.data.Items import Items
from flask import Flask, render_template, request, redirect, send_from_directory
from todo_app.flask_config import Config
import os
from flask_login import LoginManager, login_required, current_user
from todo_app.security.Auth import Auth
from loggly.handlers import HTTPSHandler
from logging import Formatter



def create_app(db_name=None):
    app = Flask(__name__)
    app.config.from_object(Config())
    app.logger.setLevel(app.config['LOG_LEVEL'])
    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
        app.logger.addHandler(handler)
    MongoDbApi.init(db_name)
    Auth.init()

    def can_write():
        can_current_user_write = app.config['LOGIN_DISABLED'] or current_user.has_write_permission()
        app.logger.info("Does current user have write permission? %s", can_current_user_write)
        return can_current_user_write

    @app.route('/')
    @login_required
    def index():  # pylint:disable=unused-variable
        item_view_model = ViewModel(
            Items.get_items(), Items.get_current_sort_order(), can_write())
        return render_template('index.html', view_model=item_view_model)

    @app.route('/', methods=['POST'])
    @login_required
    def create_item():  # pylint:disable=unused-variable
        if can_write():
            Items.add_item(request.form['title'])
            app.logger.info("New item '%s' successfully created.", request.form['title'])
        return redirect('/')

    @app.route('/actions/<action>/<id>')
    @login_required
    def perform_item_action(action, id):  # pylint:disable=unused-variable
        if can_write():
            if action == 'doing':
                Items.doing_item(id)
                app.logger.debug("Item status for '%s' successfully changed to 'Doing'.", id)
            elif action == 'done':
                Items.done_item(id)
                app.logger.debug("Item status for '%s' successfully changed to 'Done'.", id)

        return redirect('/')

    @app.route('/sortby/<sortby>')
    @login_required
    def sort_by(sortby):  # pylint:disable=unused-variable
        Items.set_current_sort_order(sortby)
        return redirect('/')

    @app.route('/deleteitem/<id>')
    @login_required
    def remove_item(id):  # pylint:disable=unused-variable
        if can_write():
            Items.delete_item(id)
            app.logger.debug("Item '%s' successfully deleted.", id)
        return redirect('/')

    @app.route('/favicon.ico')
    def favicon():  # pylint:disable=unused-variable
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        app.logger.debug("Current user is not authenticated.")
        return redirect(Auth.unauthenticated())

    @login_manager.user_loader
    def load_user(user_id):
        return Auth.load_user(user_id)

    @app.route('/login/callback')
    def login_callback():  # pylint:disable=unused-variable
        Auth.login_callback(request)
        app.logger.debug("Current user has been authenticated.")
        return redirect('/')

    login_manager.init_app(app)

    return app
