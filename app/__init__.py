from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import sys, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get( "DB_URL" )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# print( "db - ", os.getenv( "DB_URL" ) )

api = Api( app )
db = SQLAlchemy( app )

from .models.posts import *
from .models.users import *
from .models.auth import *

# db.create_all()

from .resources.authentication import Authenticator
from .resources.users import Users as UsersResource
from .resources.posts import Posts as PostsResource

api.add_resource( Authenticator, "/auth" )
api.add_resource( UsersResource, "/users/<int:uid>" )
api.add_resource( PostsResource, "/posts" )

api.init_app( app )