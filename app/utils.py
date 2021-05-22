import os, sys
import hashlib
from cryptography.fernet import Fernet

from dotenv import load_dotenv

load_dotenv()

key = os.getenv( "FERNET_SECRET" )

def encrypt( s ):
    key = os.getenv( "FERNET_SECRET" )

    return Fernet( key ).encrypt( s.encode() ).decode()

def decrypt( s ):
    key = os.getenv( "FERNET_SECRET" )

    return Fernet( key ).decrypt( s.encode() ).decode()

def generate_key( l = 8 ):
    return Fernet.generate_key().decode()

def hash_data( s, key, algol = 'md5' ):
    hashed = hashlib.md5()
    hashed.update( s.encode() )
    hashed.update( key.encode() )

    return hashed.hexdigest()