from flask import Flask, render_template, request, redirect, send_from_directory
from todo_app.flask_config import Config
from todo_app.data.sort_manager import get_current_sort_order, set_current_sort_order
from todo_app.data.trello_api import TrelloApi
import os

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = TrelloApi.get_items_lists()
    return render_template('index.html', items=items, sort=get_current_sort_order())


@app.route('/', methods=['POST'])
def create_item():
    TrelloApi.add_item(request.form['name'])
    return redirect('/')


@app.route('/actions/<action>/<id>')
def perform_item_action(action, id):
    if action in ['start', 'doing']:
        TrelloApi.start_item(id)
    elif action == 'done':
        TrelloApi.done_item(id)

    return redirect('/')


@app.route('/sortby/<sortby>')
def sort_by(sortby):
    set_current_sort_order(sortby)
    return redirect('/')


@app.route('/deleteitem/<id>')
def remove_item(id):
    TrelloApi.delete_item(id)
    return redirect('/')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


if __name__ == '__main__':
    app.run()
