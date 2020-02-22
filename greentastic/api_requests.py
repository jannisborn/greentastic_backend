import os
from datetime import datetime
from typing import Union

import polyline
from googlemaps import Client as GoogleMaps

# Setup Google API
API_KEY = open(os.getcwd() + '/greentastic.keypair', 'r').read()
GMAPS = GoogleMaps(API_KEY)


def get_directions(
    start: Union[str, dict, list, tuple], end: Union[str, dict, list, tuple]
) -> dict:
    """
    Query distances API from Google Maps to compute route from start to end.

    Args:
        - START (Union[string, dict, list tuple]) - E.g. a string of a place or
        its GPS coordinates.
        - END (Union[string, dict, list tuple]). E.g. a string of a place or
        its GPS coordinates.

    Returns:
        - DIRECTIONS (dict) - Keys are transportation modes, values are:
            - distance: a dict consisting of modes and distances.
            - duration: a dict consisting of modes and distances.
            - coordinates: a list of GPS coordinates.
    """

    directions = dict()

    for mode in ['driving', 'walking', 'bicycling', 'transit']:
        routes = GMAPS.directions(
            start, end, mode=mode, departure_time=datetime.now()
        )

        # Skip this transportation type if no route is available
        if len(routes) == 0: continue

        # Allocate dict
        directions[mode] = dict()
        directions[mode]['distance'] = dict()
        directions[mode]['duration'] = dict()
        directions[mode]['coordinates'] = []

        # Gather data (parse individual parts of the journey)
        for step in routes[0]['legs'][0]['steps']:

            # Parse the polyline into GPS coordinates
            directions[mode]['coordinates'].extend(
                polyline.decode(step['polyline']['points'])
            )

            # Update the distance and duration values
            # travel_mode defaults to what is given in step directly, but the
            # nesting is necessary to separate transit modes (Bus, Tram etc.)
            travel_mode = step.get('transit_details', {}).get('line', {}).get(
                'vehicle', {}
            ).get('type', step['travel_mode']).lower()

            directions[mode]['duration'].update({
                travel_mode: (
                    directions[mode]['duration'].get(travel_mode, 0) +
                    step['duration']['value']
                )
            })  # yapf: disable
            directions[mode]['distance'].update({
                travel_mode: (
                    directions[mode]['distance'].get(travel_mode, 0) +
                    step['distance']['value']
                )
            })  # yapf: disable

    return directions


def get_autocomplete(
    query: str, location: Union[str, dict, list, tuple], radius: int = 50000
) -> list:
    """
    Receives a query for GoogleMaps Places API and returns a sorted list of
    best destinations.

    Args:
        - QUERY (string).  The possibly incomplete target location.
        - LOCATION (Union[string, dict, list, or tuple]). The user location,
            ideally a list of two GPS coordinates.
        - RADIUS (int, optional). The radius in meter used to restrict the
            search proposals. Defaults to 50km.
    Returns:
        - SUGGESTIONS (list). A sorted list of best destinations.
    """

    places = GMAPS.places_autocomplete(query, radius=radius, location=location)
    suggestions = [place.get('description', ) for place in places]
    return suggestions
