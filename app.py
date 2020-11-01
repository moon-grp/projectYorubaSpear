from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import json
import bcrypt
import datetime


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
       # name = {"name": "olumide", "age": "14"}
       # dbRes = mongo.db.yorubaspear.insert_one(name)

        data = request.json
        email = data["email"]
        password = data["password"]

        if not email:
            return "aboii, you no enter email na", 400
        if not password:
            return "aboii, you no enter password na", 400

        hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))

        insert = mongo.db.yorubaspear.insert({
            "email":email,
            "password":hashed,
            "date": datetime.datetime.utcnow()
        })

    except Exception as x:
        print(x)


if __name__ == "__main__":
    app.run(debug=True)
