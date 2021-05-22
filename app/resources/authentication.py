from app.exceptions import UserExistsException
from ..models.auth import Auth

from flask_restful import Resource, reqparse

from flask import abort, request, Response

auth_args = reqparse.RequestParser()
auth_args.add_argument( "email", required = True, type = str, help="Users email" )
auth_args.add_argument( "pwd", required = True, type = str, help="Users password" )

class Authenticator( Resource ):

    def post( self ):

        payload = auth_args.parse_args()

        ip_address = request.remote_addr

        auth = Auth.authenticate( ip_address = ip_address, **payload )
        
        if not auth[0]:
            abort( Response( auth[1], 404 ) )
        
        return { "token": auth[1] }
    
    def put( self ):
        payload = auth_args.parse_args()
        try:
            return {"status": Auth.add_user( **payload ) is not None}
        except UserExistsException as e:
            abort( Response( str(e), 400 ) )

    def delete( self ):
        # this endpoint deletes token not authenticator
        pass