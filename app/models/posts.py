from app.exceptions import CommentNotFoundException, PostNotFoundException
import datetime
from .. import db

class Post( db.Model ):

    id = db.Column( db.Integer, primary_key = True, autoincrement = True )
    uid = db.Column( db.String( 500 ), db.ForeignKey('user.id'), nullable = False )

    # media is boolean. the media path = {storagepath}/{id}-{uid}.{ext}
    # allowed extensions are mp4, png, jpg, jpeg
    media = db.Column( db.Boolean, default = False, nullable = False )
    caption = db.Column( db.String( 500 ), nullable = True )

    # location of post = {latitude},{longitude}
    location = db.Column( db.String( 500 ), nullable = False )

    allow_comments = db.Column( db.Boolean, default = True, nullable = False )

    date_posted = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )

    likes = db.relationship( 'Like', backref = 'post', lazy = True )

    comments = db.relationship( 'Comment', backref = 'post', lazy = True )

    pins = db.relationship( 'Pin', backref = 'post', lazy = True )

    @staticmethod
    def add_post( uid, location, media = False, caption = None, allow_comments = True ):
        if (( not media ) and (caption is None)):
            return False, "Empty post"

        post = Post( uid = uid, location = location,
             media = media, caption = caption, allow_comments = allow_comments )
        db.session.add( post )
        db.session.commit()

        return post
    
    @staticmethod
    def edit_post( uid, pid, caption = None, allow_comments = None ):

        _post = Post.query.filter_by( uid = uid, id = pid ).first()

        if _post is None:
            raise PostNotFoundException( pid )
        
        if caption is not None:
            _post.caption = caption

        if allow_comments is not None:
            _post.allow_comments = allow_comments

        db.session.commit()

        return _post
    
    @staticmethod
    def delete_post( uid, pid ):
        _post = Post.query.filter_by( uid = uid, id = pid ).first()

        if _post is None:
            raise PostNotFoundException( pid )
        
        db.session.delete( _post )
        db.session.commit()

        return _post

class Like( db.Model ):

    id = db.Column( db.Integer, primary_key = True, autoincrement = True )

    uid = db.Column( db.String( 500 ), nullable = False )
    pid = db.Column( db.Integer, db.ForeignKey('post.id'), nullable = False )

    date_liked = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )

    @staticmethod
    def like( uid, pid ):
        _like = Like.query.filter_by( uid = uid, pid = pid ).first()

        if _like is None:
            _like = Like( uid = uid, pid = pid )

            db.session.add( _like )
            db.session.commit()

        return _like
    
    @staticmethod
    def unlike( uid, pid ):
        _like = Like.query.filter_by( uid = uid, pid = pid ).first()

        if _like is not None:
            db.session.delete( _like ) 
            db.session.commit()

        return _like

class Comment( db.Model ):

    id = db.Column( db.Integer, primary_key = True, autoincrement = True )

    uid = db.Column( db.String( 500 ), nullable = False )
    pid = db.Column( db.Integer, db.ForeignKey('post.id'), nullable = False )

    comment = db.Column( db.String( 200 ), nullable = False )

    date_commented = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )

    @staticmethod
    def add_comment( uid, pid, comment ):
        _comment = Comment( uid = uid, pid = pid, comment = comment )

        db.session.add( _comment )
        db.session.commit()

        return _comment
    
    @staticmethod
    def delete_comment( uid, pid, id ):
        _comment = Comment.query.filter_by( uid = uid, pid = pid, id = id ).first()
        if _comment is None:
            raise CommentNotFoundException( f"{id} by {uid}" )

        db.session.delete( _comment )
        db.session.commit()

        return _comment
