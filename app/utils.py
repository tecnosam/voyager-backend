import base64
from .exceptions import InvalidTokenException
import os, sys
import time, random
import datetime
import hashlib

def encrypt( s ):
    return s

def decrypt( s ):
    return s

def generate_key( l = 8 ):
    s = ''.join( ( chr(random.randint( 49, 127 )) for _ in range( l ) ) )

    return s

def hash_data( s, key, algol = 'md5' ):
    hashed = hashlib.md5()
    hashed.update( s.encode() )
    hashed.update( key.encode() )

    return hashed.hexdigest()