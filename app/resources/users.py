from ..exceptions import InvalidTokenException, UserNotFoundException, UserNotSetupException
from ..models.auth import Token
from ..models.users import User

from flask_restful import Resource, reqparse, fields, marshal_with, marshal

from flask import abort, request, Response

from .posts import post_fields
from .pins import pins_field

user_fields = {
    'uid': fields.String,
    'name': fields.String,
    'bio': fields.String,
    'pins': fields.Nested(pins_field),
    'timeline': fields.Nested(post_fields)
}

user_args = reqparse.RequestParser()
user_args.add_argument( 'name', required = True, type = str, help = "Your full name" )
user_args.add_argument( 'bio', default = "Hi there!", type = str, help="Users bio" )

edit_user_args = reqparse.RequestParser()
edit_user_args.add_argument( 'name', type = str, help = "Your full name" )
edit_user_args.add_argument( 'bio', default = "Hi there!", type = str, help="Users bio" )
edit_user_args.add_argument( 'show_pins', type = int, help="Show pins in page" )
edit_user_args.add_argument( 'show_timeline', type = int, help="Show timeline in page" )

class Users(Resource):

    @marshal_with( user_fields )
    def get( self ):

        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        try:
            user = User.fetch_data( uid )
        except UserNotSetupException as e:
            abort( Response( str(e) + '\n', 404 ) )

        if user is None:
            abort( Response( "Error: User not found", 404 ) )

        return user

    @marshal_with( user_fields )
    def post( self ):

        ip_address = request.remote_addr
        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        token = request.headers.get( 'token' )
        try:
            new_token = Token.validate_token( token, uid, ip_address, False )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( new_token[1], 403 ) )

        payload = user_args.parse_args( strict = True )

        _user = User.add_data( uid, **payload )

        return _user

    def put( self ):
        ip_address = request.remote_addr

        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        token = request.headers.get( 'token' )
        try:
            new_token = Token.validate_token( token, uid, ip_address, False )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( "Invalid token", 403 ) )

        payload = edit_user_args.parse_args( strict = True )

        try:
            _user = User.update_data( uid, **payload )
        except UserNotFoundException as e:
            abort( Response( str(e), 404 ) )

        return Response( 
            marshal( _user, user_fields ),
            headers={ 'new-token': new_token[1] }
        )
    
    def delete( self ):
        return {"message": "This enpoint is currently unavailable"}
        ip_address = request.remote_addr
        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        token = request.headers.get( 'token' )

        try:
            new_token = Token.validate_token( token, uid, ip_address, False )
        except InvalidTokenException as e:
            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( new_token[1], 403 ) )

        try:
            _user = User.delete_data( uid )
        except UserNotFoundException as e:
            abort( Response( str(e), 404 ) )

        return Response( 
            marshal( _user, user_fields ),
            headers={ 'new-token': new_token[1] }
        )