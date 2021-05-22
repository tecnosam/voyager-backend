from app.exceptions import InvalidTokenException
from app.models.auth import Token
from flask_restful import Resource, marshal, reqparse, fields, marshal_with
from .posts import post_fields
from ..models.users import Pin

from flask import abort, request, Response


class Pins( Resource ):
    def get( self ):
        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        ip_address = request.remote_addr

        token = request.headers.get( 'token' )
        try:
            new_token = Token.validate_token( token, uid, ip_address, False )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( str(e), 403 ) )

        return Pin.fetch_pins( uid )
    
    def post( self ):

        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        pid = request.args.get( "pid" ) # post id

        ip_address = request.remote_addr

        token = request.headers.get( 'token' )
        try:
            new_token = Token.validate_token( token, uid, ip_address, False )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( str(e), 403 ) )
        
        return marshal( Pin.add_pin( uid, pid ), post_fields )
    
    def delete( self ):
        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        pid = request.args.get( "pid" ) # post id

        ip_address = request.remote_addr # users ip address

        # fetch and validate token
        token = request.headers.get( 'token' )
        try:
            new_token = Token.validate_token( token, uid, ip_address, False )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( str(e), 403 ) )
        # end of validate token

        return marshal( Pin.remove_pin( uid, pid ), post_fields )