from todo_app.data.Items import Items
from flask import Flask, render_template, request, redirect, send_from_directory
from todo_app.flask_config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = Items.get_items()
    return render_template('index.html', items=items, sort=Items.get_current_sort_order())


@app.route('/', methods=['POST'])
def create_item():
    Items.add_item(request.form['title'])
    return redirect('/')


@app.route('/actions/<action>/<id>')
def perform_item_action(action, id):
    if action in ['start', 'doing']:
        Items.start_item(id)
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
