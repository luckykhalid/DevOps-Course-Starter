from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items)

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

if __name__ == '__main__':
    app.run()