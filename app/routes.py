from app import app 
from flask import render_template


#change
@app.route('/')
def index():
    """
    This route should be the main page, 
    grid of all items
    """
    parent_list = [
            {'Phone1': ["Item Description", "./static/download.jpg"]}, 
            {'Phone2': ["Item Description", "./static/download.jpg"] }, 
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