from turtle import title
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy import false, delete
from app import app, db
from flask import render_template, url_for, flash, redirect, request, session
from flask_login import login_user, login_required, user_logged_in, current_user, logout_user
from app.forms import LoginForm, RegistrationForm


from app.models import User, Bidding, Item, Notification, Warnings, Reviews, Orders, Banned
from datetime import datetime, timedelta

import sqlite3
con = sqlite3.connect('data.db', check_same_thread=False)
cur = con.cursor()

# create post item page
@app.route('/postItem')
@login_required
def postItem():
    return render_template('postItem.html', title="Post an Item Here!", user=current_user)


@app.route('/addItemForm', methods=["POST"])
def addItemForm():
    item_name = request.form.get("item_name")
    item_desc = request.form.get("item_desc")
    price = request.form.get("price")
    pic_url = request.form.get("pic_url")
    is_biddable = request.form.get("is_biddable")
    booleancheck = 0
    if (is_biddable == "on"):
        booleancheck = 1

    item = Item(item_name = item_name, user_id = current_user.user_id, warning_id="000", item_desc = item_desc, price =price, pic_url=pic_url, is_biddable=booleancheck)
    db.session.add(item)
    db.session.commit()
    return render_template('addItemForm.html')


@app.route('/updateItemForm', methods=["POST"])
def updateItemForm():
    item_name = request.form.get("item_name")
    price = request.form.get("price")

    db.engine.execute('UPDATE item SET price = ? WHERE item_name = ? and user_id = ?', (price,item_name,current_user.user_id))
    db.session.commit()

    return render_template('updateItemForm.html')
    

@app.route('/deleteItemForm', methods=['GET', 'POST'])
def deleteItemForm():
    _item_name = request.form.get("delete_item")
    my_var = request.args.get('my_var', None)

    db.engine.execute('DELETE FROM item WHERE item_id= ? and user_id = ?',(my_var,current_user.user_id))
    db.session.commit()
    return render_template('deleteItemForm.html')




@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Cyrus 

    This route should be the main page, 
    grid of all items
    """
    data = db.engine.execute("SELECT * FROM item")
    data_dict = [{x.item_id: [x.item_name.title(), x.item_desc, x.pic_url]} for x in data]

    """
    Patcharapa
    
    This sql command will select the latest notification from notification table and display it on the index page
    """
    cur.execute("SELECT * FROM notification WHERE [date_made]=(SELECT MAX([date_made]) FROM notification)")
    notif = cur.fetchone()
    valid_notif = True
    if notif == None:
        valid_notif = False
        notif = ["", "", "", ""]

    return render_template('index.html', data=data_dict, notif=notif[2], date=notif[3], user=current_user, valid_notif=valid_notif)


@app.route('/shop')
def shop():
    return(render_template('shop.html'))


@app.route('/item/<id_>', methods=['GET', 'POST'])
@login_required
def item(id_):

    """
    Cyrus and someone 

    This route shows the item page, equipped with a couple features
    """
    item = db.engine.execute(f"SELECT * FROM item WHERE item_id = {id_}").first()

    warning = db.engine.execute(f"SELECT * FROM warning WHERE warning_id = {item.warning_id}").first()

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
        review = Reviews(item_id=id_, user_id=current_user.user_id, message=request.form['reviewText'], rating=request.form['reviewRating'])
        db.session.add(review)
        db.session.commit()
        print("Added Review")
        return redirect(url_for('item', id_=id_))

    #Cyrus 
    #BID QUERY 
    #find the top bid 
    bid_data = db.engine.execute(f"SELECT * FROM bidding WHERE item_id = {id_} ORDER BY top_bid DESC;").first()
    top_bid = bid_data.top_bid if bid_data else 0

    # This is if someone placed a bid
    if request.method == 'POST' and 'place_bid' in request.form:
        top_bid = float(request.form['place_bid'])
        user_bid = db.engine.execute("SELECT * FROM bidding WHERE item_id = ? and user_id = ?", (id_, current_user.user_id)).first()
        
        now = datetime.now() 
       
       # First bid from user
        if user_bid is None:
            #INSERT BID 
            db.engine.execute("INSERT INTO bidding (item_id, user_id, top_bid, bid_placed_date) VALUES (?, ?, ?, ?)", (id_, current_user.user_id, top_bid, now))
            db.session.commit()
    
        # User already placed a bid so we just need to update it
        else:

            #UPDATE BID 
            db.engine.execute('UPDATE bidding SET top_bid = ?, bid_placed_date = ? WHERE item_id = ? and user_id = ?', (top_bid, now, id_, current_user.user_id))
            db.session.commit()

    # Delete the bid
    if request.method == 'POST' and 'remove_bid' in request.form:

        #DELETE BID 
        db.session.execute(f'DELETE FROM bidding WHERE item_id = {id_} and user_id = {current_user.user_id}')
        db.session.commit()

        return redirect(url_for('item', id_=id_))

    if request.method == 'POST' and 'delete_review_button' in request.form:
        review_id = request.form['delete_review_button']

        cur.execute(f"DELETE FROM review WHERE review_id = {review_id}")
        con.commit()
        
        return redirect(url_for('item', id_=id_))

    if request.method == 'POST' and 'updateReviewButton' in request.form:
        review_id = request.form['updateReviewButton']
        new_review_desc = request.form['newReviewText']
        new_review_rating = request.form['newReviewRating']

        cur.execute('UPDATE review SET message = ?, rating = ? WHERE review_id = ?', (new_review_desc, new_review_rating, review_id))
        con.commit()
        
        return redirect(url_for('item', id_=id_))

    return render_template("item.html", item=item, item_reviews=item_reviews, item_rating=item_rating, top_bid=top_bid, user=current_user, warning=warning)


@app.route('/buy/<id_>', methods=['GET', 'POST'])
def buy(id_):

    if current_user.is_authenticated:
        bid_exist = cur.execute('SELECT * FROM bidding WHERE item_id=?',(id_)).fetchall()
        bid_id_ = 9999
        if bid_exist != []:
            bid_id_ = bid_exist[0][0]
        bid = Orders(user_id=current_user.user_id, item_id=id_, bid_id=bid_id_)
        db.session.add(bid)
        db.session.commit()
    return render_template('purchased.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Cyrus 

    This route should be the registration page,
    After inputting all the data the database is updated with the new user

    """

    form = RegistrationForm()
    if form.validate_on_submit():
        # INSERT USER
        user = User(email=form.email.data, password=form.password.data, username=form.username.data, address=form.address.data, first_name=form.first_name.data, last_name=form.last_name.data, city=form.city.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Cyrus 

    This route logs users in by checking if the email and password match
    and then using flask login we log the user in 
    """
    form = LoginForm()
    if form.validate_on_submit():
        #USER QUERY 
        user_1 = db.engine.execute("SELECT * FROM user WHERE email = ? and password = ?", (form.email.data, form.password.data)).first()
        user = db.session.query(User).filter_by(email=form.email.data, password=form.password.data).first()
        
        """
        Patcharapa
        
        redirect to ban page if the user is in the banned users list
        """
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
        # DELETE USER
        cur.execute('DELETE FROM user WHERE user_id = ?',(str(current_user.user_id)))
        con.commit()

    return redirect(url_for("index"))


@app.route("/change_username", methods=['GET', 'POST'])
@login_required
def change_username():
    """
    Cyrus 

    This function allows the user to change their username.
    """

    if request.method == 'POST':
        # UPDATE USERNAME
        cur.execute('UPDATE user SET username = ? WHERE user_id = ?',(request.form['change_username'], current_user.user_id))
        con.commit()
        return redirect(url_for('index'))

    return render_template('change_username.html')


# TODO: polish admin homepage fix admin button 
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    """
    Patcharapa

    contains all admin features in this page
    """
    username = current_user.username
    return render_template('admin.html', title='admin', username=username)


@app.route("/ban_users", methods=['GET', 'POST'])
def ban_users():
    """
    Patcharapa

    ban and unban user, and show banned users list
    """
    if request.method == 'POST':
        # ban user
        # if user is banned, he/she should not be able to access anything on the index page
        if 'username' in request.form:
            # get the username from html input field
            username = request.form['username']
            # check if the user exists in the database
            user_exist = cur.execute('SELECT * FROM user WHERE username=?',(username,)).fetchone()
            
            if user_exist is None:
                flash("This username does not exist in our records, please check your spelling and try again")
                return redirect(url_for('ban_users'))  
            
            # if user exist in the database then update user table and add this user to the banned_users table
            cur.execute('SELECT * FROM user WHERE username = ? AND is_banned = 1', (username, ))
            check_ban = cur.fetchone()
            print("user banned: ", check_ban)
            
            # check if this user is already banned
            if check_ban is not None:
                flash('This user is already banned')
            else:
                # update user
                cur.execute('UPDATE user SET is_banned = 1 WHERE username = ?', (username,))
                con.commit()
                # add user to banned_user
                get_id = cur.execute("SELECT user_id FROM user where username = ?", (username,)).fetchone()
                banned = Banned(user_id=get_id[0])
                db.session.add(banned)
                db.session.commit()
                
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
            else:
                # update user
                cur.execute('UPDATE user SET is_banned = 0 WHERE username = ?', (username_unban,))
                con.commit()
                # delete user from banned_user
                get_id = cur.execute("SELECT user_id FROM user where username = ?", (username_unban,)).fetchone()
                cur.execute('DELETE from banned_users WHERE user_id = ?', (get_id[0],))
                con.commit()
                
        return redirect(url_for('ban_users'))      
            
    # show banned users list        
    cur.execute("SELECT banned_users.user_id, user.username FROM banned_users INNER JOIN user ON banned_users.user_id=user.user_id")
    banned_user = cur.fetchall()
    if banned_user == []:
        banned_user = [('dummy','Currently have no banned users')]    
    return render_template('banUsers.html', title='ban_users', banned_user = banned_user)


@app.route("/notification", methods=['GET', 'POST'])
def notification():
    """
    Patcharapa
    
    add, update, delete notification
    """
    now = datetime.now()
    if request.method == 'POST':
        # create notification
        # TODO: Add username id after the login issue is resolved
        if current_user.is_authenticated:
            if 'notif_create' in request.form: 
                notif_create = request.form['notif_create']
                notif = Notification(user_id=current_user.user_id, notif_desc=notif_create, date_made = now)
                db.session.add(notif)
                db.session.commit()
                flash("notification added")
                redirect(url_for('notification'))
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
                    redirect(url_for('notification'))
    # Display notification      
    notif_list = cur.execute("SELECT notification.notification_id, notification.notif_desc, user.username, notification.date_made FROM notification INNER JOIN user ON notification.user_id=user.user_id").fetchall()
    if notif_list == []:
        notif_list = [('N/A','Currently have no notification','N/A','N/A','N/A')]  
    else:
        notif_list = [(row[0], row[1], row[2], row[3][:10], row[3][11:19]) for row in notif_list]
    # print(notif_list)
      
    return render_template('notification.html', title='notification', notif_list=notif_list)


@app.route("/warning")
def warning():
    return render_template('warning.html', title='warning')

@app.route('/warningForm', methods=["POST"])
def warningForm():
   #add_warning_title = request.form.get("add_warning_title")
    add_warning_desc = request.form.get("add_warning_desc")
    add_warning_item_id = request.form.get("add_warning_item_id")
    warning = Warnings( warning_desc = add_warning_desc)
    db.session.add(warning)
    db.session.commit()

    db.engine.execute('UPDATE item SET warning_id = ? WHERE item_id = ?', (warning.warning_id,add_warning_item_id))
    db.session.commit()
    return render_template('warningForm.html')

@app.route('/updateWarningForm', methods=["POST"])
def updateWarningForm():
    update_warning_desc = request.form.get("update_warning_desc")
    update_warning_item_id = request.form.get("update_warning_item_id")
    warning = Warnings( warning_desc = update_warning_desc)
    db.session.add(warning)
    db.session.commit()

    db.engine.execute('UPDATE item SET warning_id = ? WHERE item_id = ?', (warning.warning_id,update_warning_item_id))
    db.session.commit()
    return render_template('updateWarningForm.html')   

@app.route('/deleteWarningForm', methods=["POST"])
def deleteWarningForm():
    delete_warning_item_id = request.form.get("delete_warning_item_id")
    db.engine.execute('UPDATE item SET warning_id = ? WHERE item_id = ?', ("000",delete_warning_item_id))
    db.session.commit()
    return render_template('deleteWarningForm.html') 


@app.route("/add_admin", methods=['GET', 'POST'])
def add_admin():
    """
    Patcharapa
    
    add/delete admin role
    """
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
    """
    Patcharapa

    Display when user is in banned users list
    """
    return render_template('banPage.html', title='ban_page')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/manageOrders", methods=['GET', 'POST'])
@login_required
def manageOrders():
    """
    Michael

    Allow users to gift items to other users and cancel orders
    """

    if request.method == 'POST':
        # Handle gifting item to another user
        if request.form['submit_button'] == 'Gift Order':
            gift_username = request.form['gift_username']
            gift_order_id = request.form['gift_order_id']

            # lookup user_id
            gift_user = db.session.query(User).filter_by(username = gift_username).first()

            # update order
            order = db.session.query(Orders).filter_by(order_id = gift_order_id).first()
            if not order is None and order.user_id == current_user.user_id:
                order.user_id = gift_user.user_id
                db.session.commit()
            # else:
            #     flash("Incorrect Order ID, You did not order this item.", "danger")

            return redirect(url_for('manageOrders'))

        # handle cancelling item order
        if request.form['submit_button'] == 'Cancel Order':
            cancel_order_id = request.form['cancel_order_id']
            
            # delete order
            order = db.session.query(Orders).filter_by(order_id = cancel_order_id).first()
            if not order is None and order.user_id == current_user.user_id:
                db.session.delete(order)
                db.session.commit()

            return redirect(url_for('manageOrders'))

    # display list of past orders
    orders = db.session.query(Orders).filter_by(user_id=current_user.user_id).all()
    item_id_name = []
    for order in orders:
        cur.execute(f"SELECT item_name FROM item WHERE item_id = {order.item_id}")
        item_name = cur.fetchone()[0]
        item_id_name.append([order.order_id, item_name])

    if orders == []:
        orders = [[1, "New iphone"]]

    return render_template('manageOrders.html', user=current_user, orders=item_id_name)
