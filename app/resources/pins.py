from typing import Type
from app.exceptions import InvalidTokenException
from app.models.auth import Token
from flask_restful import Resource, marshal, fields, marshal_with
from .posts import post_fields
from ..models.users import Pin

from flask import abort, request, Response


pins_field = {
    "id": fields.Integer,
    "pid": fields.Integer,
    "post": fields.Nested(post_fields),
    "date_pinned": fields.DateTime
}

class Pins( Resource ):

    @marshal_with( pins_field )
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
            abort( Response( new_token[1], 403 ) )

        return Pin.fetch_pins( uid )
    
    def post( self ):

        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        try:
            pid = request.args.get( "pid" ) # post id
            if pid is None:
                raise TypeError
        except TypeError:
            abort( Response( "Post ID is missing", 403 ) )


        ip_address = request.remote_addr

        token = request.headers.get( 'token' )
        try:
            new_token = Token.validate_token( token, uid, ip_address, False )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( new_token[1], 403 ) )
        
        return marshal( Pin.add_pin( uid, pid ), post_fields )
    
    def delete( self ):
        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        try:
            pid = request.args.get( "pid" ) # post id
            if pid is None:
                raise TypeError
        except TypeError:
            abort( Response( "Post ID is missing", 403 ) )

        ip_address = request.remote_addr # users ip address

        # fetch and validate token
        token = request.headers.get( 'token' )
        try:
            new_token = Token.validate_token( token, uid, ip_address, False )
        except InvalidTokenException as e:

            abort( Response( str(e), 400 ) )

        if not ( new_token[0] ):
            abort( Response( new_token[1], 403 ) )
        # end of validate token

        return marshal( Pin.remove_pin( uid, pid ), post_fields )