#!/usr/bin/env python
# coding: utf-8

import numpy as np
import json
from greentastic.api_requests import get_directions


def normalize_value_arr(value_arr):
    mins = np.amin(value_arr, axis=0)
    maxs = np.amax(value_arr, axis=0)
    norm_value_arr = 1 - (value_arr - mins) / (
        maxs - mins
    )  # normalize and invert at the same time, i.e. high score is good
    norm_value_arr[:,
                   3] = 1 - norm_value_arr[:,
                                           3]  # calories needs to be inverted
    norm_value_arr = np.around(norm_value_arr, 2)
    return norm_value_arr


def compute_score(info_dic, maps_dic, weights=[1, 1, 1, 1, 1]):
    """
    Takes a dictionary maps_dic containing the distances and durations for all means of transportation
    Computes the emissions, calories and price using info_dic (researched information)
    returns a dic with all factors for all means of transport available, and the total score weighted by weights
    """
    # define base_price_once_transits to avoid counting the base price multiple times when bus comes directly after tram
    base_price_once_transits = ["tram", "bus", "trolleybus", "commuter_train", "subway", "metro_rail"]
    prev_step = None # previous step --> if prev_step=bus and step_key = tram then don't take base price again

    norm_weights = weights / np.sum(weights)
    out_dic = {}
    # check: duration in minutes, distances in km
    nonempty_keys = []  # if no car route can be found, then it is empty
    value_arr = []  # np.zeros((len(info_dic.keys()), 4))
    for i, transport in enumerate(['driving', 'taxi', 'walking', 'bicycling', 'escooter', 'ebike', 'transit']): # walk, escooter, ebike # sorted(info_dic.keys())
        # print("\n TRANSPORT:", transport)
        maps_key = info_dic[transport]["maps_key"]  # current corresponding key, eg transit

        # dist_dic is {tram: 5, walking:0.5, bus: 3} = maps_dic["transit"] wenn eigentlich transit ist aber dann weg aufgeteilt
        dist_dic = maps_dic.get(maps_key, {}).get("distance", {})
        dur_dic = maps_dic.get(maps_key, {}).get("duration", {})

        if not dist_dic: # happens if one option does not exist, e.g. this route is not possible by car
            continue

        # Define the dictionary where all information is written
        out_dic[transport] = {}

        # sum up all durations from dur_dic to get overall duration
        total_duration = round(sum(dur_dic.values()),2)
        total_distance = round(sum(dist_dic.values()), 2)

        # one list for each part of the way
        prices = []
        emissions = []
        calories = []
        toxicity = []
        for j, step_key in enumerate(sorted(dist_dic.keys())):  # step_key = one of transit, walking, cycling, driving
            # for each part of the way, compute the absolute amount of calories burnt,
            # the price and the absolute amount of emissions
            if step_key == maps_key: # step_key is now for example "tram", maps_key is "transit"
                step_transport = transport  # wenn key in dist dic "cycling" ist dann ist das "escooter"
            else:
                step_transport = step_key
            d = dist_dic[step_key] * 0.001  # distance of this step per KM
            m = dur_dic[step_key] / 60  # duration of this step per MIN
            infos = info_dic[step_transport]

            emissions.append(infos["emissionsProKM"] * d)  # emissions
            toxicity.append(infos["toxicityPerKM"] * d) # toxicity
            if d==0: # can happen, e.g. walking 0m 
                p=0
            # To avoid counting the base price twice if first bus than tram for example:
            elif "priceKm" in infos and prev_step in base_price_once_transits and step_key in base_price_once_transits:
                p = infos["priceKm"] * d
            elif "priceKm" in infos:
                p = infos["base_price"] + infos["priceKm"] * d # public transport: base price + price per km
            else: # then it is computed per minute
                p = infos["priceMin"] * m

            if maps_key=="transit":
                print(step_key, d, p)
            prices.append(p)  # price
            calories.append(infos["caloriesPerMin"] * m)  # calories
            # print("e:", emissions, "p:", prices, "c:", calories)
            prev_step = step_key

        total_toxicity = round(sum(toxicity), 2)
        total_emissions = round(sum(emissions), 2)
        total_calories = round(sum(calories), 2)
        total_price = round(sum(prices), 2)

        nonempty_keys.append(transport)
        value_arr.append(
            [total_duration, total_emissions, total_price, total_calories, total_toxicity])

        out_dic[transport] = {
            "emission": total_emissions,
            "calories": total_calories,
            "price": total_price,
            "distance": total_distance,
            "duration": total_duration,
            "toxicity": total_toxicity
        }
        out_dic[transport]["coordinates"] = maps_dic.get(maps_key,{}).get("coordinates",[])

    value_arr = np.asarray(value_arr)
    norm_value_arr = normalize_value_arr(value_arr)
    # print(np.around(norm_value_arr,2))

    colours = [[220,20,60], [255,120,71], [264,184,60], [173,255,47], [50,205,50]]
    colour_scores = [1, 3, 5, 7, 9]
    for i, transport in enumerate(nonempty_keys):
        for j, score_name in enumerate([
                "duration_score", "emission_score", "price_score",
                "calories_score", "toxicity_score"
        ]):
            out_dic[transport][score_name] = norm_value_arr[i, j]
        for j, score_name in enumerate(
            ["duration_col", "emission_col", "price_col", "calories_col", "toxicity_col"]):
            closest = np.argmin(
                np.abs(colour_scores - norm_value_arr[i, j] * 10))
            out_dic[transport][score_name] = colours[closest]
        total_score = sum(norm_value_arr[i] * norm_weights)
        out_dic[transport]["total_weighted_score"] = total_score
        closest_total = np.argmin(np.abs(colour_scores - total_score * 10))
        out_dic[transport]["total_weighted_score_col"] = colours[closest_total]

    sorted_keys = sorted(out_dic.keys())
    scores = [out_dic[k]["total_weighted_score"] for k in sorted_keys]
    order = np.flip(np.argsort(scores), axis=0)
    sorted_out_dic = {}
    for o in order:
        sorted_out_dic[sorted_keys[o]] = out_dic[sorted_keys[o]]
    return sorted_out_dic
