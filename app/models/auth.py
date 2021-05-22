import datetime
from .. import db

from ..exceptions import InvalidTokenException, UserExistsException
from ..utils import encrypt, decrypt, generate_key, hash_data

import sys, os, time
import sqlalchemy

class Auth( db.Model ):
    id = db.Column( db.String( 200 ), primary_key = True, nullable = False )

    email = db.Column( db.String( 200 ), unique = True, nullable = False )

    pwd = db.Column( db.String( 500 ), nullable = False ) # hexdigest of password

    # name of hashing algorithm used to hash password
    hash = db.Column( db.String( 10 ), default = "md5", nullable = False )
    
    key = db.Column( db.String( 20 ), nullable = False ) # pub key used to hash

    date_created = db.Column( db.DateTime(40), default = datetime.datetime.utcnow() )

    @staticmethod
    def add_user( email, pwd ):

        key = generate_key(  )

        _pwd = hash_data( pwd, key )

        _auth = Auth( email = email, pwd = _pwd, key = encrypt(key) )

        print( _auth.email )

        _auth.id = encrypt( f"user-{_auth.email}-{time.time()}" )
        try:
            db.session.add( _auth )
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise UserExistsException( email )

        return _auth

    @staticmethod
    def authenticate( email, pwd, ip_address ):
        _auth = Auth.query.filter_by( email = email ).first()
        if ( _auth is None ):
            return False, "Email not found"

        _pwd = hash_data( pwd, decrypt(_auth.key) )

        if ( _auth.pwd != _pwd ):
            return False, "Password is incorrect"

        token = Token.generate_token( _auth.id, ip_address )

        if token is None:
            return False, "Could not generate token. please try again later"
        
        return True, token

class Token( db.Model ):

    access_token = db.Column( db.String( 255 ), primary_key = True, nullable = False )

    access_type = db.Column( db.String( 40 ), default = "user_data_spec", nullable = False )

    last_used = db.Column( db.DateTime( 40 ), default = datetime.datetime.utcnow(), nullable = False )

    @staticmethod
    def dump_token( s, access_type = 'user_data_spec' ):
        
        # loads the token to the database
        s_hashed = hash_data( s, os.getenv( 'HASH_SECRET' ) )

        _token = Token( access_token = s_hashed, access_type = access_type )

        db.session.add( _token )
        db.session.commit()

        return _token

    @staticmethod
    def generate_token( uid, ip_address, expires = 3 ):

        data = f"token\t{uid}\t{ip_address}\t{time.time() + expires*86400}\trenewable"

        token = encrypt( data )

        if Token.dump_token( token ) is not None:
            return token
        
        return None

    @staticmethod
    def validate_token( token, uid, ip_address, refresh_now = True ):
        try:
            data = decrypt( token )
            print( "decrypted - ", data )
            data = data.split( "\t" )
            if len(data) < 5:
                raise InvalidTokenException( "Token is either corrupted or incomplete" )
        except Exception as e:
            raise InvalidTokenException( str( e ) )
        
        if data[2] != ip_address:
            print( "tokens ip: ", data )
            return False, "This device doesn't have a session."

        if data[1] != uid:
            return False, "You dont have permission to use this token"
        
        _token = Token.query.get( hash_data(token, os.getenv('HASH_SECRET')) )

        if _token is None:
            raise InvalidTokenException( "Token does not exist" )

        if float(data[3]) <= time.time():
            # deletes token and raises exception

            db.session.delete( _token )
            db.session.commit()

            raise InvalidTokenException( "Token has expired" )

        if (refresh_now and (data[4] == 'renewable')):

            new_token = Token.generate_token( data[1], ip_address )

            db.session.delete( _token )
            db.session.commit()

            return True, new_token
        else:
            _token.last_used = datetime.datetime.utcnow()
            db.session.commit()

        return True, data[1], token # status, uid and token