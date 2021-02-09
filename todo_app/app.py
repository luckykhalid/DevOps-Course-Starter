from flask import Flask, render_template, request, redirect, send_from_directory
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item, get_current_sort_order, delete_item, set_current_sort_order
import os
import requests
import json

app = Flask(__name__)
app.config.from_object(Config)

headers = {
    "Accept": "application/json"
}

#postcode_response = requests.get("https://api.postcodes.io/postcodes/NW51TL")


query = {    
}

postcode_response = requests.request("GET",
                            "https://api.postcodes.io/postcodes/NW51TL",
                            headers=headers,
                            params=query
                            )

#longitude = postcode_response.json().result.longitude
#latitude = postcode_response.json().result.latitude

#postcode_response = requests.get("api.postcodes.io/postcodes/NW5 1TL")


url = "https://transportapi.com/v3/uk/bus/stop/490015367S/live.json"



query = {
    'app_id': '23e33db4',
    'app_key': '7972b59c792d28b4819f58a1a13e7a62',
    'group': 'route',
    'limit': 5,
    'nextbuses': 'yes'
}

response = requests.request("GET",
                            url,
                            headers=headers,
                            params=query
                            )


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items, sort=get_current_sort_order(), response=response, postcode_response=postcode_response)


@app.route('/', methods=['POST'])
def create_item():
    add_item(request.form['title'])
    return index()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


if __name__ == '__main__':
    app.run()
