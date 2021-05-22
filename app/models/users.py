from ..exceptions import UserNotFoundException
from .posts import Post
import datetime
from .. import db

class User( db.Model ):

    id = db.Column( db.Integer, primary_key = True, autoincrement = True )
    uid = db.Column( db.String( 500 ), unique = True, nullable = False )

    name = db.Column( db.String( 100 ), nullable = False )
    bio = db.Column( db.String( 312 ), default = "Hi, There", nullable = True )
    
    show_pins = db.Column( db.Boolean, default = False, unique = False )
    show_timeline = db.Column( db.Boolean, default = True, unique = False )

    timeline = db.relationship( 'Post', backref = 'user', lazy = True )

    pins = db.relationship( 'Pin', backref = 'user', lazy = True )

    # this will require token
    @staticmethod
    def add_data( uid, name, bio = None ):

        _user = User( uid = uid, name = name )

        if bio is not None:
            _user.bio = bio

        db.session.add( _user )

        db.session.commit()

        return _user

    # this will not require token
    @staticmethod
    def fetch_data( uid, isolate = False ):

        _user = User.query.filter_by( uid = uid ).first()

        if not isolate:

            if _user.show_pins:

                _user.pins = Pin.query.filter_by( uid = uid ).all()

            if _user.show_timeline:

                _user.timeline = Post.query.filter_by( uid = uid ).all()

        return _user

    # this will require token
    @staticmethod
    def update_data( uid, name = None, bio = None ):
        _user = User.fetch_data( uid, isolate = True )
        if _user is None:
            raise UserNotFoundException( uid )
        
        if name is not None:
            _user.name = name
        if bio is not None:
            _user.bio = bio
        
        # db.session.add( _user )
        db.session.commit()

        return _user

    # this will require token
    @staticmethod
    def delete_data( uid ):
        _user = User.fetch_data( uid, isolate = True )

        if _user is None:
            raise UserNotFoundException( uid )

        db.session.delete( _user )

        db.session.commit()

        return _user


class Pin( db.Model ):

    id = db.Column( db.Integer, primary_key = True, autoincrement = True )

    uid = db.Column( db.String( 500 ), db.ForeignKey('user.uid'), nullable = False )

    pid = db.Column( db.Integer, db.ForeignKey('post.id'), nullable = False )

    date_pinned = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )

    def add_pin( uid: str, pid: int ) -> Post:
        _pin = Pin.query.filter_by( uid = uid, pid = pid ).first()
        if _pin is None:
            _pin = Pin( uid = uid, pid = pid )

            db.session.add( _pin )
            db.session.commit()

        return Post.query.get( pid )
    
    @staticmethod
    def remove_pin( uid, pid ):
        _pins = Pin.query.filter_by( uid = uid, pid = pid ).all()

        for _pin in _pins:
            db.session.delete( _pin )

        db.session.commit()

        return Post.query.get( pid )

    @staticmethod
    def fetch_pins( uid ):

        posts = db.session.query( Pin ).filter_by( uid = uid ).join( Post ).all()

        return posts