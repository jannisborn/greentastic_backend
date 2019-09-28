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


def get_directions(start, end):
    """
    Query distances API from Google Maps to compute route from start to end.

    Args:
        - START {string, dict, list tuple}. E.g. a string of a place or its GPS coordinates.
        - END {string, dict, list tuple}. E.g. a string of a place or its GPS coordinates.

    Returns:
        - DIRECTIONS {dict}.    Keys are transportation modes, values are:
                                    - distance: a dict consisting of modes and distances.
                                    - duration: a dict consisting of modes and distances.
                                    - coordinates: a list of GPS coordinates.
    """

    directions = dict()

    for mode in ["driving", "walking", "bicycling", "transit"]:
        routes = GMAPS.directions(start,
                                  end,
                                  mode=mode,
                                  departure_time=datetime.now())

        # Allocate dict
        directions[mode] = dict()
        directions[mode]['distance'] = {mode: 0, "walking": 0}
        directions[mode]['duration'] = {mode: 0, "walking": 0}
        directions[mode]['coordinates'] = []

        # Gather data (parse individual parts of the journey)
        for step in routes[0]['legs'][0]['steps']:

            # Parse the polyline into GPS coordinates
            directions[mode]['coordinates'].extend(
                polyline.decode(step['polyline']['points']))

            # Update the distance and duration values
            directions[mode]['duration'][
                step['travel_mode'].lower()] += step['duration']['value']
            directions[mode]['distance'][
                step['travel_mode'].lower()] += step['distance']['value']

    return directions
