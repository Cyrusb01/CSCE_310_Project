from app import app 
from flask import render_template

@app.route('/')
def index():
    query = "shop data"
    return(render_template('index.html', data=query))

@app.route('/shop')
def shop():
    return(render_template('shop.html'))
