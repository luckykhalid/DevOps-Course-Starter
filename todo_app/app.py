from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item, get_current_sort_order, set_current_sort_order

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items, sort=get_current_sort_order())


@app.route('/', methods=['POST'])
def create_item():
    add_item(request.form['title'])
    return index()


@app.route('/markcomplete/<id>')
def mark_complete(id):
    item = get_item(id)
    item['status'] = 'Completed'
    save_item(item)
    return redirect('/')


@app.route('/sortby/<sortby>')
def sort_by(sortby):
    current_sort_order = get_current_sort_order()
    if current_sort_order['column'] == sortby:
        current_sort_order['descending'] = not current_sort_order['descending']
    else:
        current_sort_order['descending'] = False

    current_sort_order['column'] = sortby
    items = get_items()
    return render_template('index.html', items=items, sort=current_sort_order)


if __name__ == '__main__':
    app.run()
