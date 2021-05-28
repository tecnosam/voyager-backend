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

db.create_all()

from .resources.authentication import Authenticator
from .resources.users import Users as UsersResource
from .resources.posts import Posts as PostsResource
from .resources.pins import Pins as PinsResource
from .resources.comments import Comments as CommentsResource
from .resources.likes import Likes as LikesResource

api.add_resource( Authenticator, "/auth" )
api.add_resource( UsersResource, "/users" )
api.add_resource( PostsResource, "/posts" )
api.add_resource( PinsResource, "/pins" )
api.add_resource( CommentsResource, "/comments/<int:pid>" )
api.add_resource( LikesResource, "/likes/<int:pid>" )

api.init_app( app )