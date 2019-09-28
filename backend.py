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
API_KEY = open(os.getcwd() + '/clean_commuter.keypair', 'r').read()
GMAPS = GoogleMaps(API_KEY)


def get_directions(query):

    # start = query[0]
    # end = query[1]

    start = "Zürich Hauptbahnhof, Bahnhofpl., 8001 Zürich"
    end = "ETH Zürich Hauptgebäude, Rämistrasse 101, 8092 Zürich"

    response = dict()

    #for mode in ["driving", "walking", "bicycling", "transit"]:
    for mode in ["driving"]:

        directions = GMAPS.directions(start,
                                      end,
                                      mode=mode,
                                      departure_time=datetime.now())

        # Allocate dict
        response[mode] = dict()
        response[mode]['distance'] = {mode: 0, "walking": 0}
        response[mode]['duration'] = {mode: 0, "walking": 0}
        response[mode]['coordinates'] = []

        # Gather data (parse individual parts of the journey)
        for step in directions[0]['legs'][0]['steps']:

            # Parse the polyline into GPS coordinates
            response[mode]['coordinates'].extend(
                polyline.decode(step['polyline']['points']))

            # Update the distance and duration values
            response[mode]['duration'][
                step['travel_mode'].lower()] += step['duration']['value']
            response[mode]['distance'][
                step['travel_mode'].lower()] += step['distance']['value']

    return response


#%%
