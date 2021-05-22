from flask_restful import Resource, fields, marshal_with

from ..models.posts import Like

from ..models.auth import Token

from ..exceptions import InvalidTokenException

from flask import abort, Response, request

likes_fields = {
    "id": fields.Integer,
    "uid": fields.String,
    "pid": fields.Integer,
    "date_liked": fields.DateTime
}

class Likes(Resource):

    @marshal_with( likes_fields )
    def get( self, pid ):

        return Like.query.filter_by( pid = pid ).order_by(
            Like.date_liked.desc()
        ).all()
    
    @marshal_with( likes_fields )
    def post( self, pid ):

        uid = request.headers.get( "uid" )

        if uid is None:
            abort( 403 )

        token = request.headers.get( "token" )
        ip_address = request.remote_addr

        try:
            valid = Token.validate_token( token, uid, ip_address, False )
            if not valid[0]:
                abort( Response( valid[1], 403 ) )
        except InvalidTokenException:
            abort( Response( "token is invalid", 403 ) )

        return Like.like( uid, pid )

    @marshal_with( likes_fields )
    def delete( self, pid ):
        uid = request.headers.get( "uid" )
        _id = request.args['id']

        if uid is None:
            abort( 403 )

        token = request.headers.get( "token" )
        ip_address = request.remote_addr

        try:
            valid = Token.validate_token( token, uid, ip_address, False )
            if not valid[0]:
                abort( Response( valid[1], 403 ) )
        except InvalidTokenException:
            abort( Response( "token is invalid", 403 ) )

        return Like.unlike( uid, pid )