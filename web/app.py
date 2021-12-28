from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json
import os
import dotenv

if not os.getenv('IS_PRODUCTION'):
    dotenv.load_dotenv(dotenv.find_dotenv())

db_url = os.getenv("DB_URL")

app = Flask(__name__)
api = Api(app)



client = MongoClient(db_url)
db = client.ImageRec
users = db["Users"]

def UserExist(username):
    if (users.count_documents({"username":username}) > 0):
        return True
    else:
        return False

def RetReq(statusCode,msg):
    retJson = {
        "status":statusCode,
        "msg":msg
    }
    return jsonify(retJson)

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            return RetReq(301,"Usuario ja existente")
        hashed_pw = bcrypt.hashpw(password.encode("utf8"),bcrypt.gensalt())

        users.insert_one({
            "username":username,
            "password":hashed_pw,
            "tokens":10
        })
        return RetReq(200,"Registrado com sucesso")

api.add_resource(Register,'/register')

if __name__=="__main__":
    app.run(host='0.0.0.0')