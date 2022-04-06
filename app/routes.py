from app import app
from flask import render_template


# change
@app.route('/')
def index():
    """
    This route should be the main page, 
    grid of all items
    """
    parent_list = [
        {'Phone1': ["Item Description", "./static/download.jpg"]},
        {'Phone2': ["Item Description", "./static/download.jpg"]},
        {'Phone3': ["Item Description", "./static/download.jpg"]},
        {'Phone4': ["Item Description", "./static/download.jpg"]},
        {'Phone5': ["Item Description", "./static/download.jpg"]},
        {'Phone6': ["Item Description", "./static/download.jpg"]},
        {'Phone7': ["Item Description", "./static/download.jpg"]},
        {'Phone8': ["Item Description", "./static/download.jpg"]},
        {'Phone9': ["Item Description", "./static/download.jpg"]},
        {'Phone10': ["Item Description", "./static/download.jpg"]}]
    return(render_template('index.html', data=parent_list))


@app.route('/shop')
def shop():
    return(render_template('shop.html'))


@app.route('/login', methods=["GET", "POST"])
def login():
    return(render_template('login.html'))


@app.route('/register')
def register():
    return(render_template('register.html'))


@app.route('/item')
def item():
    item_name = "Test Item Name"
    item_price = 310.99
    item_desc = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    item_pic_path = "./static/download.jpg"

    return(render_template('item.html', **locals()))
