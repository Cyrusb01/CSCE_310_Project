from app import app, db
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, login_required
from app.forms import LoginForm, RegistrationForm
from app.models import User

import sqlite3
con = sqlite3.connect('data.db', check_same_thread=False)
cur = con.cursor()
# change
@app.route('/')
def index():
    """
    This route should be the main page, 
    grid of all items
    """

    data = db.engine.execute("SELECT * FROM item")
    data_dict = [{x.item_id: [x.item_name, x.item_desc, x.pic_url]} for x in data]
    # print(data_dict)
    return(render_template('index.html', data=data_dict))


@app.route('/shop')
def shop():
    return(render_template('shop.html'))

@app.route('/item/<id>')
def item(id):
    data = db.engine.execute("SELECT * FROM item WHERE item_id = {}".format(id)).first()
    item_name = data.item_name
    item_price = data.price
    item_desc = data.item_desc
    item_pic_path = data.pic_url
    item_rating = 3.7
    item_reviews = [["User Name", 3, """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""], ["User Name 1", 5, """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""], ["User Name 2", 1, """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""]]

    return(render_template('item.html', item_name=item_name, item_price=item_price, item_desc=item_desc, item_pic_path=item_pic_path, item_rating=item_rating, item_reviews=item_reviews))


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
        user = db.session.query(User).filter_by(email=form.email.data, password=form.password.data).first()
        if user:
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html', title='admin')

@app.route("/ban_users", methods=['GET', 'POST'])
def ban_users():
    if request.method == 'POST':
        # ban user
        if 'username' in request.form:
            print('check exist')
            username = request.form['username']
            cur.execute('SELECT * FROM user WHERE username = ? AND is_banned = 1', (username, ))
            print('check username', username)
            check_ban = cur.fetchone()
            print('check ban', check_ban)
            if check_ban is not None:
                flash('This user is already banned')
                con.commit
            else:
                cur.execute('UPDATE user SET is_banned = 1 WHERE username = ?', (username,))
                con.commit()
        # unban user   
        elif 'username_unban' in request.form:
            username_unban = request.form['username_unban']
            cur.execute('SELECT * FROM user WHERE username = ? AND is_banned = 0', (username_unban, ))
            print('check username_un', username_unban)
            check_unban = cur.fetchone()
            print('check unban', check_unban)
            if check_unban is not None:
                flash('This user does not exist in the banned users list')
                con.commit
            else:
                cur.execute('UPDATE user SET is_banned = 0 WHERE username = ?', (username_unban,))
                con.commit()
        return redirect(url_for('ban_users'))      
            
    # show banned users list        
    cur.execute("SELECT * FROM user WHERE is_banned = 1")
    banned_user = cur.fetchall()
    if banned_user == []:
        banned_user = [('dummy','Currently have no banned users')]    
    return render_template('banUsers.html', title='ban_users', banned_user = banned_user)

@app.route("/notification", methods=['GET', 'POST'])
def notification():
    return render_template('notification.html', title='notification')

@app.route("/warning", methods=['GET', 'POST'])
def warning():
    return render_template('warning.html', title='warning')

@app.route("/add_admin", methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        # Add admin
        if 'username' in request.form:
           
            username = request.form['username']
            cur.execute('SELECT * FROM user WHERE username = ? AND is_admin = 1', (username, ))
            print('check username', username)
            check_add = cur.fetchone()
            print('check ban', check_add)
            if check_add is not None:
                flash('This user is already admin')
                con.commit
            else:
                cur.execute('UPDATE user SET is_admin = 1 WHERE username = ?', (username,))
                con.commit()
        # unban user   
        elif 'username_del' in request.form:
            username_del = request.form['username_del']
            cur.execute('SELECT * FROM user WHERE username = ? AND is_admin = 0', (username_del, ))
            print('check username_del', username_del)
            check_del = cur.fetchone()
            print('check del', check_del)
            if check_del is not None:
                flash('This user does not exist in the admin list')
                con.commit
            else:
                cur.execute('UPDATE user SET is_admin = 0 WHERE username = ?', (username_del,))
                con.commit()
        return redirect(url_for('add_admin'))        
            
    # show banned users list        
    cur.execute("SELECT * FROM user WHERE is_admin = 1")
    admin = cur.fetchall()
    if admin == []:
        admin = [('dummy','Currently have no admins')]     
    con.commit() 
    return render_template('addAdmin.html', title='add_admin', admin_list = admin)