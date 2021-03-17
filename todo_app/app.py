from todo_app.ViewModel import ViewModel
from todo_app.data.Items import Items
from flask import Flask, render_template, request, redirect, send_from_directory
from todo_app.flask_config import Config
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app


app = create_app()


@app.route('/')
def index():
    item_view_model = ViewModel(
        Items.get_items(), Items.get_current_sort_order())
    return render_template('index.html', view_model=item_view_model)


@app.route('/', methods=['POST'])
def create_item():
    Items.add_item(request.form['title'])
    return redirect('/')


@app.route('/actions/<action>/<id>')
def perform_item_action(action, id):
    if action == 'doing':
        Items.doing_item(id)
    elif action == 'done':
        Items.done_item(id)

    return redirect('/')


@app.route('/sortby/<sortby>')
def sort_by(sortby):
    Items.set_current_sort_order(sortby)
    return redirect('/')


@app.route('/deleteitem/<id>')
def remove_item(id):
    Items.delete_item(id)
    return redirect('/')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


if __name__ == '__main__':
    app.run()
