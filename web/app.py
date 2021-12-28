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

if __name__=="__main__":
    app.run(host='0.0.0.0')