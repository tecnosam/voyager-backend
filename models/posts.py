import datetime
from .. import db

class Post( db.Model ):

    id = db.Column( db.Integer, primary_key = True, auto_incremenet = True )
    uid = db.Column( db.String( 500 ), db.ForeignKey('user.id'), nullable = False )

    # media is boolean. the media path = {storagepath}/{id}-{uid}.{ext}
    # allowed extensions are mp4, png, jpg, jpeg
    media = db.Column( db.Boolean, unique = True, nullable = False )
    caption = db.Column( db.String( 500 ), nullable = True )

    # location of post = {latitude},{longitude}
    location = db.Column( db.String( 500 ), nullable = False )

    allow_comments = db.Column( db.Boolean, default = True, nullable = False )

    date_posted = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )

    likes = db.relationship( 'Like', backref = 'post', lazy = True )

    comments = db.relationship( 'Comment', backref = 'post', lazy = True )

    pins = db.relationship( 'Pin', backref = 'post', lazy = True )

class Like( db.Model ):

    id = db.Column( db.Integer, primary_key = True, auto_increment = True )

    uid = db.Column( db.String( 500 ), nullable = False )
    pid = db.Column( db.Integer, db.ForeignKey('post.id'), nullable = False )

    date_liked = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )

class Comment( db.Model ):

    id = db.Column( db.Integer, primary_key = True, auto_increment = True )

    uid = db.Column( db.String( 500 ), nullable = False )
    pid = db.Column( db.Integer, db.ForeignKey('post.id'), nullable = False )

    comment = db.Column( db.String( 200 ), nullable = False )

    date_liked = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )

