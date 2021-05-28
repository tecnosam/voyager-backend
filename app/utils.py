import os, sys
import hashlib
from cryptography.fernet import Fernet

from math import radians, cos, sin, asin, sqrt

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


def haversine( coordsA, coordsB = {'lat': 0, 'long': 0} ) -> int:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)

    by default, between the center of the earh and anypoint
    """
    # convert decimal degrees to radians

    if type( coordsA ) == dict:
        [lat1, lon1] = [coordsA['lat'], coordsA['long']]
    elif type( coordsA ) == str:
        [lat1, lon1] = coordsA.split(",")
    elif type( coordsA ) == list:
        [lat1, lon1] = coordsA
    
    if type( coordsB ) == dict:
        [lat2, lon2] = [coordsB['lat'], coordsB['long']]
    elif type( coordsB ) == str:
        [lat2, lon2] = coordsB.split(",")
    elif type( coordsB ) == list:
        [lat2, lon2] = coordsB

    lon1, lat1, lon2, lat2 = map(lambda x: radians( float(x) ), [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r