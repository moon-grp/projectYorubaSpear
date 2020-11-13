from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import json
import bcrypt
import datetime
import validators
from bson import json_util
from bson.json_util import dumps
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'cosmicthebaelessboy'  # Change this!
jwt = JWTManager(app)

try:

    app.config["MONGO_URI"] = "mongodb+srv://emohex:oluoluolu@cluster0.geiph.mongodb.net/yorubaspear?retryWrites=true&w=majority"

    app.config["MONGO_URI"] = "mongodb+srv://emohex:oluoluolu@cluster0.geiph.mongodb.net/wishlist?retryWrites=true&w=majority"

    mongo = PyMongo(app)
except Exception as x:
    print("cannot connect to db")
    print(x)


@app.route("/api/v1/signup", methods=["POST"])
def signUp():
    try:

        data = request.json
        name = data["name"]
        email = data["email"]
        password = data["password"]

        if not email:
            return "aboii, you no enter email na", 400
        if not password:
            return "aboii, you no enter password na", 400
        if not name:
            return "aboii, you no enter your name na", 400

        if validators.email(email) != True:
            return "aboii, enter vaild email na!!", 400

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))

        checkEmail = mongo.db.yorubaspear.find_one({"email": email})

        if checkEmail is None:
            insert = mongo.db.yorubaspear.insert({
                "email": email,
                "password": hashed,
                "name": name,
                "date": datetime.datetime.utcnow()
            })

            access_token = create_access_token(identity={"email": email})

            res = jsonify({
                "message": "aboii, you dn create account!!!",
                "token": access_token
            })

            return res, 200
        else:

            return "aboii, you dn create account already na!!", 409

    except Exception as x:
        print(x)


@app.route('/api/v1/signin', methods=["POST"])
def login():
    try:

        data = request.json
        email = data["email"]
        password = data["password"]

        if not email:
            return "aboii, you no enter email na", 400
        if not password:
            return "aboii, you no enter password na", 400

        if validators.email(email) != True:
            return "aboii, enter vaild email na!!", 400

        getUser = mongo.db.yorubaspear.find_one({"email": email})

        if getUser != None:
            encPassword = getUser["password"]

            if bcrypt.checkpw(password.encode("utf-8"), encPassword):

                access_token = create_access_token(identity={"email": email})

                res = jsonify({
                    "message": "aboii, you dn login dy aii",
                    "token": access_token
                })

                return res, 200
            else:
                return "aboii, password no correct ooo!!!", 400

        else:
            return "aboii, your email no dy record", 400

        # return encPassword

    except Exception as x:
        print(x)


@app.route('/api/v1/wishit', methods=["POST"])
@jwt_required
def wishIt():
    try:

        data = request.json

        wish = data["wish"]

        email = get_jwt_identity()

        print(email["email"])

        getEmail = email["email"]

        # check if email is in the collection for details

        checkEmail = mongo.db.yorubaspear.find_one({"email": getEmail})

        if checkEmail != None:
            insert = mongo.db.wishlist.insert({
                "email": getEmail,
                "wish": wish,
                "date": datetime.datetime.utcnow()
            })

            res = jsonify({
                "message": "aboii, you dn send your wish to the godsss!!!",

            })

            return res, 200
        else:
            return "aboii, email no dy record check am well!!!", 400

        return "yo", 200

    except Exception as x:
        print(x)


if __name__ == "__main__":
    app.run(debug=True)
