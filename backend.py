#%%
import os
import sys
import flask
import json
import polyline
from googlemaps import Client as GoogleMaps
from datetime import datetime

#%%
# Setup Google API
API_KEY = open(os.getcwd() + '/gpc_api_key.keypair', 'r').read()
GMAPS = GoogleMaps(API_KEY)
now = datetime.now()


def get_directions(query):

    # start = query[0]
    # end = query[1]

    start = "Zürich Hauptbahnhof, Bahnhofpl., 8001 Zürich"
    end = "ETH Zürich Hauptgebäude, Rämistrasse 101, 8092 Zürich"

    response = dict()

    #for mode in ["driving", "walking", "bicycling", "transit"]:
    for mode in ["driving"]:

        response[mode] = dict()
        directions = GMAPS.directions(start,
                                      end,
                                      mode=mode,
                                      departure_time=now)

        response[mode]['distance'] = directions[0]['legs'][0]['distance'][
            'value']  # in meter
        response[mode]['duration'] = directions[0]['legs'][0]['duration'][
            'value']  # in seconds

        polys, locations = [], []

        for step in directions[0]['legs'][0]['steps']:
            polys.append(step['polyline']['points'])
            locations.extend(polyline.decode(polys[-1]))

        response[mode]['polylines'] = polys
        response[mode]['coordinates'] = locations

    return response
    #%%
