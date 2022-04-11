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

    data = db.engine.execute("SELECT * FROM item")
    data_dict = [{x.item_id: [x.item_name, x.item_desc, x.pic_url]} for x in data]
    print(data_dict)
    # parent_list = [
    #     {'Phone1': ["Item Description", "https://m.media-amazon.com/images/I/61s0IaMcKtL._AC_SL1500_.jpg"]},
    #     {'Phone2': ["Item Description", "./static/download.jpg"]},
    #     {'Phone3': ["Item Description", "./static/download.jpg"]},
    #     {'Phone4': ["Item Description", "./static/download.jpg"]},
    #     {'Phone5': ["Item Description", "./static/download.jpg"]},
    #     {'Phone6': ["Item Description", "./static/download.jpg"]},
    #     {'Phone7': ["Item Description", "./static/download.jpg"]},
    #     {'Phone8': ["Item Description", "./static/download.jpg"]},
    #     {'Phone9': ["Item Description", "./static/download.jpg"]},
    #     {'Phone10': ["Item Description", "./static/download.jpg"]}]


    return(render_template('index.html', data=data_dict))


@app.route('/shop')
def shop():
    return(render_template('shop.html'))

@app.route('/item/<id>')
def item(id):
    data = db.engine.execute("SELECT * FROM item WHERE item_id = {}".format(id)).first()
    item_name = data.item_name
    item_price = data.item_price
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
