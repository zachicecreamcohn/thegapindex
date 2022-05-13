import json
import sys
from flask import jsonify
from pymongo import MongoClient

from bson.json_util import dumps, loads

class User():
    def __init__(self, email, password, firstName, lastName, phone, cart, imagePath):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.cart = cart
        self.imagePath = imagePath


def get_database():
    
    CONNECTION_STRING = "mongodb+srv://zcohn:YSDjCfUcRl5XtDA9@cluster0.ajgse.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    db = client.get_database()
    return db['products'] # creates a db called products

def get_new_database():
    CONNECTION_STRING = "mongodb+srv://zcohn:YSDjCfUcRl5XtDA9@cluster0.ajgse.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    db = client.get_database()
    return db['fixed_products'] # creates a db called fixed_products


def get_user_db():
    CONNECTION_STRING = "mongodb+srv://zcohn:YSDjCfUcRl5XtDA9@cluster0.ajgse.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database()
    return db['users']

def get_user_by_email(email):
    db = get_user_db()
    # get userObj from db
    userObj = db.find_one({'email': email})
    if userObj is None:
        return None
    else:
        user = User(userObj['email'], userObj['password'], userObj['firstName'], userObj['lastName'], userObj['phone'], userObj['cart'], userObj['imagePath'])
        return user
        
        

def get_all_users():
    db = get_user_db()
    return db.find()

def insert_user(user):
    user_content = {

        'email': user.email,
        'password': user.password,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'phone': user.phone,
        'cart': user.cart,
        'imagePath': user.imagePath,
    }
    db = get_user_db()
    db.insert_one(user_content)

def update_user(userObj):
    user = userObj
    user_content = {

        'email': user.email,
        'password': user.password,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'phone': user.phone,
        'cart': user.cart,
        'imagePath': user.imagePath,
    }
    db = get_user_db()
    db.update_one({'email': user.email}, {'$set': user_content})

def getAllProducts():
    db = get_database()
    return db.find()

# function to insert a new product
def insert_product(product):
    db = get_database()
    db.insert_one(product)

# function to insert multiple products
def insert_products(products):
    db = get_database()
    db.insert_many(products)

# function to insert a list of products into fixed_products
def insert_fixed_products(products):
    db = get_new_database()
    db.insert_many(products)

# function to get all products
def get_all_products():
    db = get_database()
    return db.find()

def makeIntoChunks(data):
    count = 0
    bigCount = 1
    segmented_dict = {}
    current_list = []
    for product in data:
        # if (bigCount < 10):
        if (count < 40):
            current_list.append(data[product])
            count += 1
            # check if product is last in data
            if (product == list(data.keys())[-1]):
                segmented_dict[bigCount] = current_list
                
                current_list = []
        elif (count == 40):
            current_list.append(data[product])
            segmented_dict[bigCount] = current_list
            if (product != list(data.keys())[-1]):
                bigCount += 1
            count = 0
            current_list = []
            
            # count = 0
        else:
            print("ERROR")
            current_list = []
            # count = 0

    return (bigCount, segmented_dict)


def update_product(id, product):
    db = get_database()

    db.update_one({'_id': id}, {'$set': product})

def search_by_term(term):
    db = get_database()
    result = db.aggregate([
    {
        '$search': {
            'index': 'default', 
            'text': {
                'query': term,
                'path': 'name'
            }
        }
    }
])
    dataDict = {}
    for i in result:
        try:
            dbID = i['_id']
            name = i['name']
            oldPrice = i['oldPrice']
            price = i['price']
            isClearanceItem = i['isClearanceItem']
            isInStock = i['isInStock']
            mainImage = i['mainImage']
            productId = i['productId']
            colorCode = i['colorCode']
            URL = i['URL']
            
            dataDict[productId] = {
                'id': str(dbID),
                'name': name,
                'oldPrice': oldPrice,
                'price': price,
                'isClearanceItem': isClearanceItem,
                'isInStock': isInStock,
                'mainImage': mainImage,
                'productId': productId,
                'colorCode': colorCode,
                'URL': URL
            }
        except:
            pass

    if len(dataDict) == 0:
        return jsonify(False)
    return makeIntoChunks(dataDict)


def search_by_term_color(colorCode, term):
    # search db for term in name and colorCode in colorCode
    db = get_database()
    # search db for all items with name containing term and colorCode containing colorCode
    result = db.aggregate([
    {
        '$search': {
            'index': 'default',
            'text': {
                'query': term,
                'path': 'name'
            }
        }
    },
    {
        '$match': {
            'colorCode': colorCode
        }
    }
])
    
    dataDict = {}
    for i in result:
        try:
            dbID = i['_id']
            name = i['name']
            oldPrice = i['oldPrice']
            price = i['price']
            isClearanceItem = i['isClearanceItem']
            isInStock = i['isInStock']
            mainImage = i['mainImage']
            productId = i['productId']
            colorCode = i['colorCode']
            URL = i['URL']
            
            dataDict[productId] = {
                'id': str(dbID),
                'name': name,
                'oldPrice': oldPrice,
                'price': price,
                'isClearanceItem': isClearanceItem,
                'isInStock': isInStock,
                'mainImage': mainImage,
                'productId': productId,
                'colorCode': colorCode,
                'URL': URL
            }
        except:
            pass

    if len(dataDict) == 0:
        return jsonify(False)
    return makeIntoChunks(dataDict)





# if this file is run as a script, do the following
if __name__ == "__main__":

    print(search_by_term_color('tan', 't-shirt'))