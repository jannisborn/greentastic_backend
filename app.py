from flask import Flask
from flask import jsonify, request
import numpy as np
import json
from compute_scores import compute_score
from backend import get_directions, get_autocomplete

app = Flask(__name__)


@app.route('/query_directions', methods=['GET'])  # api/get_messages
def query_directions():
    weight_str = str(request.args.get('weights'))
    weighting = [int(i) for i in weight_str.split(",")] # expects 'weights=1,1,1,1'
    print("WEIGHTS", weighting)

    source = str(request.args.get('source'))
    destination = str(request.args.get('destination')) # 'dest_coordinates=bern straße xy'
    # source = (47.3857, 8.5668)
    # destination = (47.3649, 8.5469)

    googlemapsdic = get_directions(source, destination)
    # print(googlemapsdic)
    ## Hrd coded duration and distances dictionary
    # googlemapsdic = {
    #     "car": {
    #         "duration": 5,
    #         "distance": 1000
    #     },
    #     "walk": {
    #         "duration": 10,
    #         "distance": 1100
    #     },
    #     "bike": {
    #         "duration": 3,
    #         "distance": 700
    #     }
    # }


    # Load metadata from json file
    with open("metadata.json", "r") as infile:
        metadata = json.load(infile)

    # Compute scores from google maps data
    out_dic = compute_score(metadata, googlemapsdic, weights=weighting)
    return jsonify(out_dic)  # return json file


@app.route('/query_autocomplete', methods=['GET'])  # api/get_messages
def query_autocomplete():
    """
    This method interfaces the SWIFT request to get the autocompleted search queries with the
    Google Maps API.
    """

    # TODO: What data types are these?
    search_string = str(request.args.get('seach_string'))
    user_location = request.args.get('user_location')

    return get_autocomplete(search_string, user_location)



if __name__ == '__main__':
    app.run(debug=True)
