from ..exceptions import InvalidTokenException, UserNotFoundException
from ..models.auth import Token
from ..models.users import User

from flask_restful import Resource, reqparse, fields, marshal_with, marshal

from flask import abort, request, Response

user_fields = {
    'uid': fields.String,
    'name': fields.String,
    'bio': fields.String,
    # TODO:'pins': fields for pin
    # TODO:'timeline': fields for post
}

user_args = reqparse.RequestParser()
user_args.add_argument( 'name', type = str, help = "Your full name" )
user_args.add_argument( 'bio', default = "Hi there!", type = str, help="Users bio" )

class Users(Resource):
    
    @marshal_with( user_fields )
    def get( self, uid ):

        user = User.fetch_data( uid )

        if user is None:
            abort( Response( "Error: User not found", 404 ) )

        return user
    
    # @marshal_with( user_fields )
    def post( self, uid ):

        ip_address = request.remote_addr

        token = request.headers.get( 'token' )
        try:
            new_token = Token.validate_token( token, uid, ip_address )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( str(e), 403 ) )

        payload = user_args.parse_args( strict = True )

        _user = User.add_data( uid, **payload )

        return Response( 
            marshal( _user, user_fields ),
            headers={ 'new-token': new_token[1] }
        )

    def put( self, uid ):
        ip_address = request.remote_addr

        token = request.headers.get( 'token' )
        try:
            new_token = Token.validate_token( token, uid, ip_address )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( str(e), 403 ) )

        payload = user_args.parse_args( strict = True )

        _user = User.update_data( uid, **payload )

        return Response( 
            marshal( _user, user_fields ),
            headers={ 'new-token': new_token[1] }
        )
    
    def delete( self, uid ):
        ip_address = request.remote_addr

        token = request.headers.get( 'token' )

        try:
            new_token = Token.validate_token( token, uid, ip_address )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( str(e), 403 ) )

        try:
            _user = User.delete_data( uid )
        except UserNotFoundException as e:
            abort( Response( str(e), 404 ) )

        return Response( 
            marshal( _user, user_fields ),
            headers={ 'new-token': new_token[1] }
        )