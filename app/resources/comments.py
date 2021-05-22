from flask_restful import Resource, fields, marshal_with, reqparse

from ..models.posts import Comment

from ..models.auth import Token

from ..exceptions import CommentNotFoundException, InvalidTokenException

from flask import abort, Response, request

comment_fields = {
    "id": fields.Integer,
    "uid": fields.String,
    "pid": fields.Boolean,
    "comment": fields.String,
    "date_commented": fields.DateTime
}

# comment_parser = reqparse.RequestParser()
# comment_parser.add_argument( "comment", type = str, required = True, help = "Your comment" )

class Comments(Resource):

    @marshal_with( comment_fields )
    def get( self, pid ):

        return Comment.query.filter_by( pid = pid ).order_by(
            Comment.date_commented.desc()
        ).all()
    
    @marshal_with( comment_fields )
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
        
        try:
            comment = request.form['comment']
        except KeyError:
            abort( Response( "You forgot the comment", 400 ) )

        return Comment.add_comment( uid, pid, comment )

    @marshal_with( comment_fields )
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
        
        try:
            return Comment.delete_comment( uid, pid, _id )
        except CommentNotFoundException as e:
            abort( Response( str(e), 404 ) )