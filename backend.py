#%%
import os
import sys
import flask
import json
from googlemaps import Client as GoogleMaps

#%%
# Setup Google API
API_KEY = open(os.getcwd() + '/gpc_api_key.keypair', 'r').read()
GMAPS = GoogleMaps(API_KEY)