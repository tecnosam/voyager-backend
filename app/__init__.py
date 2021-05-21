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

from .models.posts import *
from .models.users import *
from .models.auth import *

# db.create_all()

from .resources.authentication import Authenticator
from .resources.users import Users as UsersResource

api.add_resource( Authenticator, "/auth" )
api.add_resource( UsersResource, "/users/<int:uid>" )

api.init_app( app )