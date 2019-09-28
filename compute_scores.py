#!/usr/bin/env python
# coding: utf-8

import numpy as np
import json
from backend import get_directions


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


def compute_score(info_dic, maps_dic, weights=[1, 1, 1, 1]):
    norm_weights = weights / np.sum(weights)
    out_dic = {}
    # check: duration in minutes, distances in km
    nonempty_keys = []  # if no car route can be found, then it is empty
    value_arr = []  # np.zeros((len(info_dic.keys()), 4))
    for i, transport in enumerate(sorted(info_dic.keys())):
        out_dic[transport] = {}
        # print("\n TRANSPORT:", transport)
        maps_key = info_dic[transport][
            "maps_key"]  # current corresponding key, eg transit

        # dist_dic = maps_dic[maps_key]["distance"]
        # dur_dic = maps_dic[maps_key]["duration"]
        # print(maps_dic.keys(),maps_key, maps_dic[maps_key])
        dist_dic = maps_dic.get(maps_key, {}).get("distance", {})
        dur_dic = maps_dic.get(maps_key, {}).get("duration", {})

        if not dist_dic:
            # If there is no route, e.g. no public transport route is found:
            # Set scores and values to zeros
            for k in [
                    "emission", "calories", "price", "distance", "duration",
                    "total_weighted_score",
                    "duration_score", "emission_score", "price_score",
                    "calories_score", "duration_score", "emission_score",
                    "price_score", "calories_score", "toxicity", "toxicity_score"
            ]:
                out_dic[transport][k] = 0
            # Set colours to red (not available --> all red)
            for k in ["duration_col", "emission_col", "price_col", "calories_col", "toxicity_col", "total_weighted_score_col"]:
                out_dic[transport][k] = [245, 53, 53]
            out_dic[transport]["coordinates"] = []
            continue

        total_duration = round(sum(dur_dic.values()),
                               2)  # duration is sum of all durations
        total_distance = round(sum(dist_dic.values()), 2)

        # one list for each part of the way
        prices = []
        emissions = []
        calories = []
        toxicity = []
        for j, step_key in enumerate(sorted(dist_dic.keys())):  # distances
            # for each part of the way, compute the absolute amount of calories burnt,
            # the price and the absolute amount of emissions
            if step_key == maps_key:
                step_transport = transport  # wenn key in dist dic "cycling" ist dann ist das "escooter"
            else:
                step_transport = step_key
            # print("Step: ", step_transport)
            d = dist_dic[step_key] * 0.001  # distance of this step per KM
            m = dur_dic[step_key] / 60  # duration of this step per MIN
            infos = info_dic[step_transport]

            emissions.append(infos["emissionsProKM"] * d)  # emissions
            toxicity.append(infos["toxicityPerKM"] * d) # toxicity
            if "priceKm" in infos:
                p = infos["priceKm"] * d
            else:
                p = infos["priceMin"] * m
            prices.append(p)  # price
            calories.append(infos["caloriesPerMin"] * m)  # calories
            # print("e:", emissions, "p:", prices, "c:", calories)

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

    colours = [[220,20,60], [255,99,71], [224,180,76], [173,255,47], [50,205,50]]
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
    return out_dic


if __name__ == "__main__":
    with open("metadata.json", "r") as infile:
        metadata = json.load(infile)

    car_type=2
    metadata['driving']['emissionsProKM'] = metadata['driving'][
        'emissionsProKM'][car_type]
    metadata['driving']['toxicityPerKM'] = metadata['driving'][
            'toxicityPerKM'][car_type]
    maps_dic = get_directions((47.3857, 8.5668),(47.3495, 8.4920)) # (47.3649, 8.5469))  #
    # print(maps_dic)
    out_dic = compute_score(metadata, maps_dic, weights=[1, 1, 1, 1, 1])
    # out_dic = compute_score(dic, {"car":{"duration":5, "distance":1000}, "walk":{"duration":10, "distance":1100},
    #  "bike":{"duration":3, "distance":700}}, weights=[1,1,1,1])
    # print(out_dic)
    for key in out_dic.keys():
        # print(len(out_dic[key].keys()))
        # print(key, out_dic[key]["toxicity"])
        # print(key, out_dic[key]["total_weighted_score_col"])
        print(key, "total score: ", out_dic[key]["total_weighted_score"])

    with open("example_output.json", "w") as outfile:
        json.dump(out_dic, outfile)
