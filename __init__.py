from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import sys, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv( "DB_URL" )

api = Api( app )
db = SQLAlchemy( app )