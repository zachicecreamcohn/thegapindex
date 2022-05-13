from sre_constants import SUCCESS
import traceback
import bcrypt
from flask import Flask, escape, render_template, render_template_string, request, redirect, url_for, flash, jsonify, session, send_from_directory
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from get_data import gap, oldnavy, banana, athleta
from database import search_by_term, get_user_db, get_user_by_email, get_all_users, insert_user, update_user, search_by_term_color
import json
from flask_bcrypt import Bcrypt
import os
from bs4 import BeautifulSoup
import flask_login
import sys
import requests


# create instance of Flask
app = Flask(__name__)
app.secret_key = "23efjsdfk2j2sdfj&^alfhj3378!2llleef3345f"
bcrypt = Bcrypt(app)
app.config['UPLOAD_FOLDER'] = 'static/profile_photos/'



class User():
    def __init__(self, email, password, firstName, lastName, phone, cart, imagePath):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.cart = cart
        self.imagePath = imagePath


users = {}

@app.route('/test-get-user-by-email/<email>')
def test_get_user_by_email(email):
    user = get_user_by_email(email)
    if user is None:
        return jsonify("user not found")
    else:
        user_as_json = jsonify({'email': user.email, 'password': user.password, 'firstName': user.firstName, 'lastName': user.lastName, 'phone': user.phone, 'cart': user.cart})
        return user_as_json

def register_user(User):
    if (get_user_by_email(User.email) != None):
        return False
    else:
        insert_user(User)
        return True

def login_user(email, passAttempt):
    user = get_user_by_email(email)
    if user is None:
        return False
    else:
        if bcrypt.check_password_hash(user.password, passAttempt):
            session['user'] = email
            session['logged_in'] = True
            return True
        else:
            return False

def logout_user():
    session.pop('user', None)
    session.pop('logged_in', None)
    
    return True

def check_logged_in():
    # if 'user' in session:
    try:
        email = session['user']
        if email in users:
            return jsonify({'email': email, 'password': users[email].password, 'firstName': users[email].firstName, 'lastName': users[email].lastName, 'phone': users[email].phone, 'cart': users[email].cart})
        # else:
        return jsonify("not logged in")
    except:
        return jsonify("not logged in")

# route for registering
@app.route('/register-request', methods=['POST'])
def register_request():
    if request.method == 'POST':
        # get the post data as json
        data = request.get_json()
        firstName = data['firstName']
        lastName = data['lastName']
        phone = data['phone']
        email = data['email']
        # check that no fields are empty
        if not firstName or not lastName or not phone or not email:
            return jsonify({'message': 'Please fill out all fields', 'success': False})

        # check that phone is valid phone number
        if not phone.isdigit() or len(phone) != 10:
            return jsonify({'message': 'Please enter a valid phone number (without the +1)', 'success': False})
        import re
        # regex to check if email is valid
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'message': 'Please enter a valid email', 'success': False})


        # escape the input to prevent malicious code
        firstName = escape(firstName)
        lastName = escape(lastName)
        phone = escape(phone)
        email = escape(email)
        

        # check if email is already in use

        password = data['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # create a new user
        cart = []
        imagePath = ""
        user = User(email, hashed_password, firstName, lastName, phone, cart, imagePath)
        if (register_user(user)):

    

            # login the user
            session['user'] = email
            session['logged_in'] = True



            return jsonify({'firstName': firstName, 'message': 'User created successfully!', 'success': True})
        else :
            return jsonify({'message': 'User already exists!', 'success': False})

    return 'No POST data'







@app.route('/check-login')
def check_login():
    if 'user' in session:
        email = session['user']

        user = get_user_by_email(email)

        
        first_name = user.firstName
        last_name = user.lastName
        phone = user.phone
        cart = user.cart

        loggedIn = True
        return jsonify({'email': email, 'cart': cart, 'firstName': first_name, 'lastName': last_name, 'phone': phone, 'loggedIn': loggedIn})

    else:
        loggedIn = False
        return jsonify({'loggedIn': loggedIn})



@app.route('/login-request', methods=['POST'])
def login_request():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']
        if login_user(email, password):
            # get the user's data
            user = get_user_by_email(email)
            first_name = user.firstName
            return jsonify({'firstName': first_name, 'message': 'User logged in successfully!', 'success': True})
        else:
            return jsonify({'message': 'Incorrect email or password', 'success': False})
    return 'No POST data'
            

@app.route('/update-cart', methods=['POST'])
def update_cart():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        email = session['user']
        cart = data['cart']
        user = get_user_by_email(email)
        user.cart = cart
        update_user(user)
        return jsonify({'message': 'Cart updated successfully!', 'success': True})
    return 'No POST data'


@app.route('/get-cart', methods=['POST', 'GET'])
def get_cart():
    # if request.method == 'POST':
    if 'user' in session:
        email = session['user']
        user = get_user_by_email(email)
        cart = user.cart
        print(cart)
        return jsonify({'cart': cart, 'success': True})
    else:
        return jsonify({'message': 'Not logged in'})
   

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'loggedOut': True})

    

@app.route('/get-user-info')
def get_user_info():
    if 'user' in session:
        email = session['user']

        user = get_user_by_email(email)
        first_name = user.firstName
        last_name = user.lastName
        phone = user.phone
        cart = user.cart
        imagePath = user.imagePath
        
        loggedIn = True
        return jsonify({'email': email, 'imagePath': imagePath, 'cart': cart, 'firstName': first_name, 'lastName': last_name, 'phone': phone, 'loggedIn': loggedIn})
    else:
        loggedIn = False
        return jsonify({'loggedIn': loggedIn})

    
@app.route('/')
def index():
    return render_template('results.html', title='Search')

# route to check if file is image
def allowed_file(filename):
    allowed_extensions = set(['png', 'jpg', 'jpeg'])
    # split the extension from the filename
    ext = filename.rsplit('.', 1)[1].lower()
    # check if the extension is in the list of allowed extensions
    if ext in allowed_extensions:
        return True
    else:

        return False

# route for uploading profile picture
@app.route('/upload-image', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # return the post data as json
        # get multipart/form-data file
        data = request.files['file']
        # check if the file is an image
        if data and allowed_file(data.filename):
            # check if file size is less than 30 kb
            if data.content_length > 30 * 1024:
                thisUser = get_user_by_email(session['user'])
                return jsonify({'message': 'File size too large', 'success': False, 'imagePath': thisUser.imagePath})

            # save the file to the uploads folder
            filename = secure_filename(data.filename)
            filename = session['user'] + '-' + filename
            data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # get the user's email
            email = session['user']

            # check if the user already has a custom image
            user = get_user_by_email(email)
            if user.imagePath != "":
                # delete the old image
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.imagePath))
            # update the user's image path
            user.imagePath = filename
            update_user(user)


            return jsonify({'message': 'Image uploaded successfully!', 'success': True, 'imagePath': filename})
        else:
            return jsonify({'message': 'File not an image', 'success': False, 'imagePath': ""})
    return 'No POST data'
    

@app.route('/api/getdata-<cid>-<pageId>-<depId>', methods=['GET'])
def getdata(cid, pageId, depId):
    data = gap(cid, pageId, depId)
    # data = athleta(cid)
    return jsonify(data)


@app.route('/api/search/<term>', methods=['GET'])
def search(term):
    try:
        data = search_by_term(term)

        return jsonify(data)
    except Exception as e:
        return "Error: " + str(e)





@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')





@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('login.html')

@app.route('/account')
def account():
    if 'user' in session:
        return render_template('profile.html')
    else:
        # redirect to login page
        return redirect(url_for('login'))

@app.route('/cart')
def cart():
    return render_template('cart.html')




# Mail Stuff
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
# TODO: change the following info to env variables
app.config['MAIL_USERNAME'] = 'thegapindex@gmail.com'
app.config['MAIL_PASSWORD'] = 'zhuywskxngyzqazb'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



mail = Mail(app)


def send_email(recipient, product, productURL, oldPrice, newPrice):
    try:
        msg = Message('Price Update', sender=('Price Update', 'thegapindex@gmail.com'), recipients =[recipient])
        oldPrice = '$' + str(oldPrice)
        newPrice = '$' + str(newPrice)
        msg.html = f"""
        <p>Hello!</p>
        <p>The price of <a href="{productURL}">{product}</a> has changed from {oldPrice} to {newPrice}.</p>

        <p>Thank you for using <b>The Gap Index!</b></p>

        <p>Sincerely,</p>
        <p>The Gap Index Team</p>
        """
        
        mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False


@app.route('/test-email')
def test_email():
    send_email('zwc1223@gmail.com', 'Maternity Popover Shirt', 'https://www.gap.com/browse/product.do?pid=815450012#pdp-page-content', '79.95', '63.00')
    return 'Email sent'


# sms stuff
from twilio.rest import Client
account_sid = 'AC0e13d8524473594b720d02983fb34fd3'
auth_token = '41bca841d7db2a69508c52c408f2df6c'


client = Client(account_sid, auth_token)


@app.route('/test-text')
def test_text():
    productName = 'Maternity Popover Shirt'
    productState = 'Out of Stock'
    fromNum = '+14325294241'
    client.messages.create(
        to="+16464772420",
        from_=fromNum,
        body=f"Item {productName} is now {productState}")
    
    return 'Text sent'






import time
import threading



def look_for_price_change(email,product):
    url = product['URL']
    current_price = product['price']
    if url is None:
        return False
    else:
        html = requests.get(url)
        # find element with class "pdp-pricing--highlight pdp-pricing__selected pdp-mfe-19nkmoj"
        soup = BeautifulSoup(html.text, 'html.parser')
        price = soup.find(class_='pdp-pricing--highlight pdp-pricing__selected pdp-mfe-19nkmoj')
        if price is None:
            # look for class 'pdp-pricing--highlight pdp-pricing__selected pdp-mfe-oan334'
            price = soup.find(class_='pdp-pricing--highlight pdp-pricing__selected pdp-mfe-oan334')
        if price is None:
            # look for class 'pdp-pricing__selected pdp-mfe-1qibdru'
            price = soup.find(class_='pdp-pricing__selected pdp-mfe-1qibdru')
        if price is None:
            # look for class ' pdp-pricing__selected pdp-mfe-zlkqt3'
            price = soup.find(class_=' pdp-pricing__selected pdp-mfe-zlkqt3')
        if price is None:
            return False
        else:
            # remove $ from price
            print(f'Product: {product["name"]}')
            price = price.text.replace('$', '')
            if (float(price) == float(current_price)):
                print('No price change')
                # NO CHANGE
            else:
                print(f"Old Price: {current_price}\nNew Price: {price}")
                # CHANGE
                send_email(recipient=email, product=product['name'], productURL = product['URL'], oldPrice=current_price, newPrice=price)

            print('\n')

        
        
def check_pricechange_and_send_emails():
    for user in get_all_users():
        cart = user['cart']
        user_email = user['email']
        for product in cart:
            look_for_price_change(user_email, product)





@app.route('/check-pricechange')
def check_pricechange():
    check_pricechange_and_send_emails()
    return 'Price change checked'






# run app
if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.18', port=100)


