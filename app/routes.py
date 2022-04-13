from app import app, db
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, login_required
from app.forms import LoginForm, RegistrationForm
from app.models import User


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

@app.route('/item')
def item():
    item_name = "Test Item Name"
    item_price = 310.99
    item_desc = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    item_pic_path = "./static/download.jpg"
    item_rating = 3.7
    item_reviews = [["User Name", 3, """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""], ["User Name 1", 5, """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""], ["User Name 2", 1, """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""]]

    return(render_template('item.html', **locals()))


@app.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data, username=form.username.data, address=form.address.data, first_name=form.first_name.data, last_name=form.last_name.data, city=form.city.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        print("insdie")
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        print(user)
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html', title='admin')

@app.route("/ban_users", methods=['GET', 'POST'])
def ban_users():
    return render_template('banUsers.html', title='ban_users')

@app.route("/notification", methods=['GET', 'POST'])
def notification():
    return render_template('notification.html', title='notification')

@app.route("/warning", methods=['GET', 'POST'])
def warning():
    return render_template('warning.html', title='warning')