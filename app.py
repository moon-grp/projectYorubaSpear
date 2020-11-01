from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import json
import bcrypt
import datetime
import validators


app = Flask(__name__)

try:

    app.config["MONGO_URI"] = "mongodb+srv://emohex:oluoluolu@cluster0.geiph.mongodb.net/yorubaspear?retryWrites=true&w=majority"

    mongo = PyMongo(app)
except Exception as x:
    print("cannot connect to db")
    print(x)


@app.route("/user", methods=["POST"])
def signUp():
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

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))

        checkEmail = mongo.db.yorubaspear.find_one({"email": email})

        if checkEmail is None:
            insert = mongo.db.yorubaspear.insert({
                "email": email,
                "password": hashed,
                "date": datetime.datetime.utcnow()
            })

            res = jsonify("aboii, you dn create the account!!")

            return res, 200
        else:

            return "aboii, you dn create account already na!!", 409

    except Exception as x:
        print(x)


@app.route('/user', methods=["GET"])
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
        encPassword = getUser["password"]

        if bcrypt.checkpw(password.encode("utf-8"), encPassword):
            return "aboii, correct pass", 200
        else:
            return "aboii e no correct" , 400

        #return encPassword

    except Exception as x:
        print(x)


if __name__ == "__main__":
    app.run(debug=True)
