from turtle import title

from sqlalchemy import false
from app import app, db
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, login_required, user_logged_in, current_user, logout_user
from app.forms import LoginForm, RegistrationForm


from app.models import User, Bidding, Item, Notification, Warnings, Reviews, Orders
from datetime import datetime, timedelta

import sqlite3
con = sqlite3.connect('data.db', check_same_thread=False)
cur = con.cursor()


#create post item page
@app.route('/postItem')
@login_required
def postItem():
    return render_template('postItem.html', title="Post an Item Here!")


@app.route('/itemForm', methods=["POST"])
def itemForm():
    item_desc = request.form.get("item_desc")
    price = request.form.get("price")
    pic_url = request.form.get("pic_url")
    is_biddable = request.form.get("is_biddable")

    return render_template('itemForm.html')


# change
@app.route('/')
def index():
    """
    This route should be the main page, 
    grid of all items
    """

    # if current_user.is_authenticated:
    #     if current_user.is_admin:
    #         return redirect(url_for('index_admin'))
    
    data = db.engine.execute("SELECT * FROM item")
    data_dict = [{x.item_id: [x.item_name.title(), x.item_desc, x.pic_url]} for x in data]
    cur.execute("SELECT * FROM notification WHERE [date_made]=(SELECT MAX([date_made]) FROM notification)")
    notif = cur.fetchone()
    valid_notif = True
    if notif == None:
        valid_notif = False
        notif = ["", "", "", ""]
    
    return render_template('index.html', data=data_dict, notif=notif[2], date=notif[3], user=current_user, valid_notif=valid_notif)


# @app.route('/a')
# def index_admin():
#     """
#     This route should be the main page for admins, 
#     grid of all items
#     """

#     data = db.engine.execute("SELECT * FROM item")
#     data_dict = [{x.item_id: [x.item_name.title(), x.item_desc, x.pic_url]} for x in data]
#     cur.execute("SELECT * FROM notification WHERE [date_made]=(SELECT MAX([date_made]) FROM notification)")
#     notif = cur.fetchone()
#     valid_notif = True
#     if notif == None:
#         valid_notif = False
#         notif = ["", "", "", ""]
    
#     return render_template('index_admin.html', data=data_dict, notif=notif[2], date=notif[3], user=current_user, valid_notif=valid_notif)


@app.route('/shop')
def shop():
    return(render_template('shop.html'))


@app.route('/item/<id_>', methods=['GET', 'POST'])
@login_required
def item(id_):
    item = db.engine.execute(f"SELECT * FROM item WHERE item_id = {id_}").first()

    item_reviews = []
    reviews = db.engine.execute(f"SELECT * FROM review WHERE item_id = {id_}")

    for row in reviews:
        review_dict = dict(row._mapping)
        review_dict['user_name'] = str(db.engine.execute(f"SELECT username FROM user WHERE user_id = {review_dict['user_id']}").first())[2:-3]
        item_reviews.append(review_dict)

    # Calc rating
    item_rating = 0
    for review in item_reviews:
        item_rating += review['rating']
    
    if item_rating != 0:
        item_rating /= len(item_reviews)
    
    if request.method == 'POST' and 'reviewText' in request.form:
        review = Reviews(item_id=id_, user_id=1, message=request.form['reviewText'], rating=request.form['reviewRating'])
        db.session.add(review)
        db.session.commit()
        print("Added Review")
        return redirect(url_for('item', id_=id_))
      
    bid_data = db.engine.execute("SELECT * FROM bidding WHERE item_id = {}".format(id_)).first()
    top_bid = bid_data.top_bid if bid_data else 0
    if request.method == 'POST' and 'place_bid' in request.form:
        top_bid = float(request.form['place_bid'])
        bid = db.session.query(Bidding).filter_by(item_id= id_).first()
        now = datetime.now() + timedelta(hours=24)
        if bid is None:
            # formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            bid = Bidding(item_id=id_, top_bid=top_bid, user_id = id_, bid_expire_date = now)
            db.session.add(bid)
            db.session.commit()
            print("Bid Committed")
            # flash('Bid Placed!')
        else:
            cur.execute('UPDATE bidding SET top_bid = ?, bid_expire_date = ? WHERE item_id = ?', (top_bid, now, id_))
            con.commit()
            # flash('Bid Placed!')

    return render_template("item.html", item=item, item_reviews=item_reviews, item_rating=item_rating, top_bid=top_bid)


@app.route('/buy/<id_>', methods=['GET', 'POST'])
def buy(id_):
    
    if current_user.is_authenticated:
        bid_exist = cur.execute('SELECT * FROM bidding WHERE item_id=?',(id_)).fetchall()
        bid_id_ = 9999
        if bid_exist != []:
            bid_id_ = bid_exist[0][0]
        bid = Orders(user_id=current_user.user_id, item_id=id_, bid_id =bid_id_ )
        db.session.add(bid)
        db.session.commit()
    return render_template('purchased.html')


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
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data, password=form.password.data).first()
        if user:
            if user.is_banned:  # If this user is banned
                return redirect(url_for('ban_page'))
            else:
                login_user(user, remember=True)
                # if user.is_admin:
                #     return redirect(url_for('index_admin'))
                return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if current_user.is_authenticated:
        cur.execute('DELETE FROM user WHERE user_id = ?',(str(current_user.user_id)))
        con.commit()

    return redirect(url_for("index"))


# TODO: polish admin homepage fix admin button 
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    firstName = current_user.first_name
    lastName = current_user.last_name
    return render_template('admin.html', title='admin', firstName=firstName, lastName=lastName)


@app.route("/ban_users", methods=['GET', 'POST'])
def ban_users():
    if request.method == 'POST':
        # ban user
        # if user is banned, he/she should not be able to access anything on the index page
        if 'username' in request.form:
            # get the username from html input field
            username = request.form['username']
            # check if the user exists in the database
            user_exist = cur.execute('SELECT * FROM user WHERE username=?',(username,)).fetchall()
            if user_exist == []:
                flash("This username does not exist in our records, please check your spelling and try again")
                return redirect(url_for('ban_users'))  
            cur.execute('SELECT * FROM user WHERE username = ? AND is_banned = 1', (username, ))
            print('check username', username)
            check_ban = cur.fetchone()
            print('check ban', check_ban)
            # check if this user is already banned
            if check_ban is not None:
                flash('This user is already banned')
                con.commit
            else:
                cur.execute('UPDATE user SET is_banned = 1 WHERE username = ?', (username,))
                con.commit()
        # unban user   
        elif 'username_unban' in request.form:
            # get the username from html input field
            username_unban = request.form['username_unban']
            # check if the user exists in the database
            user_exist = cur.execute('SELECT * FROM user WHERE username=?',(username_unban,)).fetchall()
            if user_exist == []:
                flash("This username does not exist in our records, please check your spelling and try again")
                return redirect(url_for('ban_users'))
            cur.execute('SELECT * FROM user WHERE username = ? AND is_banned = 0', (username_unban, ))
            print('check username_un', username_unban)
            check_unban = cur.fetchone()
            print('check unban', check_unban)
            # check if this user exist in the banned users list
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

    now = datetime.now()
    if request.method == 'POST':
        # create notification
        # TO DO: Add username id after the login issue is resolved
        if current_user.is_authenticated:
            if 'notif_create' in request.form: 
                notif_create = request.form['notif_create']
                notif = Notification(user_id=current_user.user_id, notif_desc=notif_create, date_made = now)
                db.session.add(notif)
                db.session.commit()
                flash("notification added")
                redirect (url_for('notification'))
                print("test1")
            # Update Notification
            elif 'notif_update' in request.form:
                print("test")
                notif_update = request.form['notif_update']
                id = request.form['update_notif_id']
                # check if id exists in the database
                id_check = cur.execute('SELECT * FROM notification WHERE notification_id=?',(id,)).fetchone()
                if id_check is None:
                    flash("This notification does not exist, please try again")
                    return redirect(url_for('notification'))
                else:
                    cur.execute('UPDATE notification SET (notif_desc, date_made)=(?,?) WHERE notification_id=?', (notif_update, now, id,))
                    con.commit()
                    flash("notification updated")
                    redirect (url_for('notification'))
            # Delete Notification
            elif 'delete' in request.form:
                print("test delete")
                id = request.form['notif_id']
                # check if id exists in the database
                id_check = cur.execute('SELECT * FROM notification WHERE notification_id=?',(id,)).fetchone()
                if id_check is None:
                    flash("This notification does not exist, please try again")
                    return redirect(url_for('notification'))
                else:
                    cur.execute('DELETE FROM notification WHERE notification_id=?', id)
                    con.commit()
                    flash("notification deleted")
                    redirect (url_for('notification'))
    # Display notification      
    notif_list = cur.execute("SELECT notification.notification_id, notification.notif_desc, notification.date_made, user.username FROM notification INNER JOIN user ON notification.user_id=user.user_id").fetchall()
    notif_list = [(row[0], row[1], row[2][:10], row[3], row[2][11:19]) for row in notif_list]
    # print(notif_list)
    con.commit() 
    return render_template('notification.html', title='notification', notif_list=notif_list)


@app.route("/warning", methods=['GET', 'POST'])
def warning():
    return render_template('warning.html', title='warning')


@app.route("/add_admin", methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        # Add admin
        if 'username' in request.form:
            # get the username from html input field
            username = request.form['username']
            # check if the user exists in the database
            user_exist = cur.execute('SELECT * FROM user WHERE username=?',(username,)).fetchall()
            if user_exist == []:
                flash("This username does not exist in our records, please check your spelling and try again")
                return redirect(url_for('add_admin'))
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
        # delete admin   
        elif 'username_del' in request.form:
            # get the username from html input field
            username_del = request.form['username_del']
            # check if the user exists in the database
            user_exist = cur.execute('SELECT * FROM user WHERE username=?',(username_del,)).fetchall()
            if user_exist == []:
                flash("This username does not exist in our records, please check your spelling and try again")
                return redirect(url_for('add_admin'))
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
            
    # show admin list        
    cur.execute("SELECT * FROM user WHERE is_admin = 1")
    admin = cur.fetchall()
    if admin == []:
        admin = [('dummy','Currently have no admins')]     
    con.commit() 
    return render_template('addAdmin.html', title='add_admin', admin_list = admin)


@app.route("/ban_page", methods=['GET', 'POST'])
def ban_page():
    return render_template('banPage.html', title='ban_page')
