from app.exceptions import InvalidTokenException, PostNotFoundException, UserNotFoundException
from app.models.auth import Token
from flask_restful import Resource, reqparse, fields, marshal_with
from flask import abort, Response, request

from ..models.posts import Post

post_fields = {
    "id": fields.Integer,
    "uid": fields.String,
    "media": fields.Boolean,
    "caption": fields.String,
    "location": fields.String,
    "allow_comments": fields.Boolean,
    "date_posted": fields.DateTime,
    # "likes": likes_fields
    # "comments": comment_fields
}

post_args = reqparse.RequestParser()
# post_args.add_argument( "uid", type = str, required = True, help = "UID of user" )
post_args.add_argument( "location", type = str, required = True, help = "lat,long coord of post" )
post_args.add_argument( "media", type = int, help = "is there a media file (1/0)" )
post_args.add_argument( "caption", type = str, help = "Post caption" )
post_args.add_argument( "allow_comments", type = int, help = "Allow users to add comments" )

edit_post_args = reqparse.RequestParser()
# edit_post_args.add_argument( "uid", type = str, required = True, help="User ID is missing" )
edit_post_args.add_argument( "pid", type = str, required = True, help="Post ID is missing" )
edit_post_args.add_argument( "caption", type = str, help="Post caption" )
edit_post_args.add_argument( "allow_comments", type = int, help = "Allow users to add comments" )

class Posts( Resource ):
    
    @marshal_with( post_fields )
    def get( self ):
        posts = Post.query.all()
        # TODO: add comment count and likes count
        # TODO: add location filter

        return posts

    @marshal_with( post_fields )
    def post( self ):
        payload = post_args.parse_args(  )
        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        token = request.headers.get( "token" )
        print("token - ", token)

        ip_address = request.remote_addr

        try:
            valid = Token.validate_token( token, uid, ip_address, False )

            if not valid[0]:
                abort( Response( valid[1], 403 ) )

        except InvalidTokenException:

            abort( Response( "token is invalid", 403 ) )
        
        if 'allow_comments' in payload:
            print( payload['allow_comments'] )

            payload['allow_comments'] = payload['allow_comments'] == 1
        
        if 'media' in payload:

            payload['media'] = payload[ 'media' ] == 1

        _post = Post.add_post( uid = uid, **payload )

        # todo: if media is true upload media file to cdn

        return _post
    
    @marshal_with( post_fields )
    def put( self ):
        payload = edit_post_args.parse_args()
        uid = request.headers.get('uid')
        if uid is None:
            abort( 403 )

        token = request.headers.get( "token" )

        print( token )

        ip_address = request.remote_addr

        try:
            valid = Token.validate_token( token, uid, ip_address, False )
            if not valid[0]:
                abort( Response( valid[1], 403 ) )
        except InvalidTokenException:
            abort( Response( "token is invalid", 403 ) )

        try:
            return Post.edit_post( uid = uid, **payload )
        except PostNotFoundException as e:
            abort( Response( str(e), 404 ) )

    @marshal_with( post_fields )
    def delete( self ):
        pid = request.args['pid']
        uid = request.headers.get('uid')
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
            return Post.delete_post( uid = uid, pid = pid )
        except PostNotFoundException as e:
            abort( Response( str(e), 404 ) )
