from app import app 
from flask import render_template

@app.route('/')
def index():
    query = "shop data"
    return(render_template('index.html', data=query))

@app.route('/shop')
def shop():
    return(render_template('shop.html'))

@app.route('/login', methods=["GET", "POST"])
def login():
    return(render_template('login.html'))

@app.route('/register')
def register():
    return(render_template('register.html'))