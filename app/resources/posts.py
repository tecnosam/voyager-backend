from ..exceptions import InvalidTokenException, PostNotFoundException, UserNotFoundException
from ..models.auth import Token
from flask_restful import Resource, reqparse, fields, marshal_with
from flask import abort, Response, request
from .. import db
from ..models.posts import Comment, Like, Post
from ..utils import haversine

from .likes import likes_fields
from .comments import comment_fields

post_fields = {
    "id": fields.Integer,
    "uid": fields.String,
    "media": fields.Boolean,
    "caption": fields.String,
    "location": fields.String,
    "allow_comments": fields.Boolean,
    "date_posted": fields.DateTime,
    "likes": fields.Nested(likes_fields),
    "comments": fields.Nested(comment_fields)
}

post_args = reqparse.RequestParser()
# post_args.add_argument( "uid", type = str, required = True, help = "UID of user" )
post_args.add_argument( "location", type = str, required = True, help = "lat,long coord of post" )
post_args.add_argument( "media", type = int, help = "is there a media file (1/0)" )
post_args.add_argument( "caption", type = str, help = "Post caption" )
post_args.add_argument( "allow_comments", default = 1, type = int, help = "Allow users to add comments" )

edit_post_args = reqparse.RequestParser()
# edit_post_args.add_argument( "uid", type = str, required = True, help="User ID is missing" )
edit_post_args.add_argument( "pid", type = str, required = True, help="Post ID is missing" )
edit_post_args.add_argument( "caption", type = str, help="Post caption" )
edit_post_args.add_argument( "allow_comments", type = int, help = "Allow users to add comments" )

class Posts( Resource ):
    
    @marshal_with( post_fields )
    def get( self ):
        posts = db.session.query( Post ).outerjoin( 
            Like.query.filter_by( pid = Post.id ),
            Comment.query.filter_by( pid = Post.id ) 
        )

        if 'dfa' in request.args:
            dfa = float(request.args[ 'dfa' ])
            posts = posts.filter( (Post.location - dfa) <= 20 )

        return posts.all()

    @marshal_with( post_fields )
    def post( self ):
        # modify to calculate the distance from the equator and store in location
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
        
        payload['location'] = haversine( payload['location'] )
        
        if 'allow_comments' in payload:
            print( payload['allow_comments'] )

            if payload['allow_comments'] is not None:

                payload['allow_comments'] = payload['allow_comments'] == 1
            
            else:

                payload.pop( 'allow_comments' )
        
        if 'media' in payload:
            if payload['media'] is not None:

                payload['media'] = payload[ 'media' ] == 1
            
            else:

                payload.pop( 'media' )


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
