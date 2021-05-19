import datetime
from .. import db

class User( db.Model ):

    id = db.Column( db.Integer, primary_key = True, auto_incremenet = True )
    uid = db.Column( db.String( 500 ), unique = True, nullable = False )

    name = db.Column( db.String( 100 ), nullable = False )
    username = db.Column( db.String( 20 ), unique = True, nullable = False )
    bio = db.Column( db.String( 312 ), default = "Hi, There", nullable = True )
    
    show_pins = db.Column( db.Boolean, default = False, unique = False )
    show_timeline = db.Column( db.Boolean, default = True, unique = False )

    timeline = db.relationship( 'Post', backref = 'user', lazy = True )

    pins = db.relationship( 'Pin', backref = 'user', lazy = True )

class Pin( db.Model ):

    id = db.Column( db.Integer, primary_key = True, auto_increment = True )

    uid = db.Column( db.String( 500 ), db.ForeignKey('user.uid'), nullable = False )

    pid = db.Column( db.Integer, db.ForeignKey('post.id'), nullable = False )

    date_liked = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )

class Auth( db.Model ):
    id = db.Column( db.Integer, primary_key = True, nullable = False )

    email = db.Column( db.String( 200 ), unique = True, nullable = False )

    pwd = db.Column( db.String( 500 ), nullable = False ) # hexdigest of password

    # name of hashing algorithm used to hash password
    hash = db.Column( db.String( 10 ), default = "md5", nullable = False )
    
    key = db.Column( db.String( 20 ), nullable = False ) # pub key used to hash

    date_created = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )