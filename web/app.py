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

def IsAdm(password):
    return password==os.getenv("ADM_PASS")

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

class Tokens(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        admin_pw = postedData["admin_pw"]
        

        if not IsAdm(admin_pw):
            return RetReq(304,"Nao autorizado")
        if not UserExist(username):
            return RetReq(301,"Usuario inexistente")

        tokens = users.find_one({"username":username})["tokens"]



        return RetReq(200,{"username":username,"tokens":tokens});

    def patch(self):
        postedData = request.get_json()

        username = postedData["username"]
        admin_pw = postedData["admin_pw"]
        tokens = postedData["tokens"]
        

        if not IsAdm(admin_pw):
            return RetReq(304,"Nao autorizado")
        if not UserExist(username):
            return RetReq(301,"Usuario inexistente")

        users.update_one({"username":username},{
            "$set":{"tokens":tokens}
            })

        return RetReq(200,"Tokens do usuario atualizado");

api.add_resource(Register,'/register')
api.add_resource(Tokens,'/tokens')

if __name__=="__main__":
    app.run(host='0.0.0.0')