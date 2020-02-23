#!/usr/bin/env python
# coding: utf-8
import numpy as np
from scipy.stats import rankdata


def compute_emissions(distance, infos, **kwargs):
    return distance * infos['emissionsProKM']


def compute_toxicity(distance, infos, **kwargs):
    return distance * infos['toxicityPerKM']


def compute_price(distance, duration, infos, step_transport, is_repeated):
    if distance == 0:  # can happen, e.g. walking 0m
        price = 0
    # To avoid counting the base price twice if first bus than tram
    elif ('priceKm' in infos and is_repeated):
        price = infos['priceKm'] * distance
    elif 'priceKm' in infos:
        # public transport: base price + price per km
        price = infos['base_price'] + infos['priceKm'] * distance
    else:  # then it is computed per minute
        price = infos['priceMin'] * duration
    return price


def compute_calories(duration, infos, **kwargs):
    return infos['caloriesPerMin'] * duration


def compute_duration(duration, step_transport, **kwargs):
    return duration


def compute_score(
    info_dic: dict, maps_dic: dict, weights: list = [1, 1, 1, 1, 1]
):
    """ 
    TODO: This methods needs some refactoring (see #5).
    Takes a dictionary containing the distances and durations for all means of
    transportation. Computes the emissions, calories and price using info_dic
    (researched information). Returns a dic with all factors for all means of
    transport available, and the total score weighted by weights.
    """
    # DEFINITIONS:
    CRITERIA = ['duration', 'emission', 'price', 'calories', 'toxicity']
    # dictionary to call methods
    method_dict = {
        'emission': compute_emissions,
        'toxicity': compute_toxicity,
        'price': compute_price,
        'calories': compute_calories,
        'duration': compute_duration
    }
    OUTPUT_TRANSPORT = [
        'driving', 'taxi', 'walking', 'bicycling', 'escooter', 'ebike',
        'transit'
    ]
    COLOURS = [
        [220, 20, 60], [255, 120, 71], [264, 184, 60], [173, 255, 47],
        [50, 205, 50]
    ]
    DEBUG = True

    ## WEIGHTS:
    if DEBUG:
        print("weights:", weights)
    assert len(weights) == len(
        CRITERIA
    ), "must be same number of weights as criteria"
    # Catch division by 0
    if np.sum(weights) == 0:
        weights = 5 * [1]
    # normalize weights
    norm_weights = weights / np.sum(weights)

    # AVAILABLE TRANSPORT
    # filter which transport is actually possible! (e.g. no car route)
    dict_exist = [
        bool(
            maps_dic.get(info_dic[transport]['maps_key'],
                         {}).get('distance', {})
        ) for transport in OUTPUT_TRANSPORT
    ]
    if DEBUG:
        print(
            "dict_exist", dict_exist,
            np.asarray(OUTPUT_TRANSPORT)[dict_exist]
        )
    OUTPUT_TRANSPORT = np.asarray(OUTPUT_TRANSPORT)[dict_exist]

    # define variable necessary to avoid counting the base price multiple
    # times when bus comes directly after tram
    base_price_once_transits = [
        'tram', 'bus', 'trolleybus', 'commuter_train', 'subway', 'metro_rail'
    ]

    ## Fill array by absolute values for criteria
    value_arr = np.zeros((len(OUTPUT_TRANSPORT), len(CRITERIA)))
    out_dict = dict()
    for i, transport in enumerate(OUTPUT_TRANSPORT):
        # corresponding key for GoogleMaps, eg transit for transport=tram
        maps_key = info_dic[transport]['maps_key']

        # dist_dic is e.g. {tram: 5, walking:0.5, bus: 3} = maps_dic['transit']
        dist_dic = maps_dic.get(maps_key, {}).get('distance', {})
        dur_dic = maps_dic.get(maps_key, {}).get('duration', {})

        # Define the dictionary where all information is written
        out_dict[transport] = dict()

        # add distance = sum of dists of dist_dic
        out_dict[transport]['distance'] = round(sum(dist_dic.values()), 2)

        # ITERATE OVER STEPS OF ROUTE:
        # step_key = tram, metro_rail, bus, cycling etc (Google Maps keys)
        # transport = one of OUTPUT_TRANSPORT
        # step_transport: can be all the ones of metadata.json
        prev_step = None
        for j, step_key in enumerate(sorted(dist_dic.keys())):
            if step_key == maps_key:  # maps_key of escooter is cycling
                # wenn key in dist dic 'cycling' ist dann ist das 'escooter'
                step_transport = transport
            else:  # step_key is now for example 'tram', maps_key is 'transit'
                step_transport = step_key
            # compute distance and duration
            dist = dist_dic[step_key] * 0.001  # distance of this step per KM
            dur = dur_dic[step_key] / 60  # duration of this step per MIN

            is_repeated = (
                prev_step in base_price_once_transits
                and step_key in base_price_once_transits
            )

            args = {
                'infos': info_dic[step_transport],
                'duration': dur,
                'distance': dist,
                'step_transport': step_transport,
                'is_repeated': is_repeated
            }

            for k, crit in enumerate(CRITERIA):
                crit_score = method_dict[crit](**args)

                value_arr[i, k] += crit_score

            if step_key != 'walking':
                prev_step = step_key

        # add absolute scores to output dict
        out_dict[transport] = {
            CRITERIA[j]: value_arr[i, j]
            for j in range(len(CRITERIA))
        }

        # add coordinates to output dict
        out_dict[transport]['coordinates'] = maps_dic.get(maps_key, {}).get(
            'coordinates', []
        )

    value_arr = np.around(value_arr, decimals=2)
    # normalize to 0-1:
    norm_value_arr = normalize_value_arr(value_arr)
    if DEBUG:
        print("absolute values (value_arr) *100:")
        print((np.round(value_arr, 2) * 100).astype(int))
        print(OUTPUT_TRANSPORT)
        for j, crit in enumerate(CRITERIA):
            print(crit, norm_value_arr[:, j])

    # Compute total score
    total_scores = total_weighted_score(norm_value_arr, norm_weights)
    # Min max normalize total score (otherwise all between 0.4 and 0.6)
    total_scores = (total_scores - min(total_scores)
                    ) / (max(total_scores) - min(total_scores))
    if DEBUG:
        print("total scores:", total_scores)
        print("colour indices for total scores:")
    ## Add normalized scores and colours to out_dict
    for i, transport in enumerate(OUTPUT_TRANSPORT):
        for j, crit in enumerate(CRITERIA):
            # add normalized scores to output
            out_dict[transport][crit + '_score'] = norm_value_arr[i, j]
            # add colours for normalized scores to output
            out_dict[transport][crit + '_col'] = COLOURS[int(
                round(norm_value_arr[i, j] * 4)
            )]

        out_dict[transport]['total_weighted_score'] = total_scores[i]
        out_dict[transport]['total_weighted_score_col'] = COLOURS[int(
            round(total_scores[i] * 4)
        )]
        if DEBUG:
            print(transport, int(round(total_scores[i] * 4)))
    # sort dictionary by scores
    sorted_out_dict = sort_dictionary(out_dict)
    if DEBUG:
        print("keys after sorting:", sorted_out_dict.keys())
    return sorted_out_dict


# UTILS


def normalize_value_arr(value_arr: np.array) -> np.array:
    """
    Normalize the feature scores saved in a np.array.

    Args:
        VALUE_ARR (np.array) - array of shape num_transports x 5 with the five
            scores for each transportation means.
            NOTE: The features are assumed to be ordered:
                [duration, emission, price, calories, toxicity]
    Returns:
        NORM_VALUE_ARR (np.array) - normalized array of the same shape, where
            the scores for each of the five features sum to 1.
    """
    # TODO: Log or not Log?
    value_arr = np.log(value_arr + 1)
    # min max normalization
    mins = np.amin(value_arr, axis=0)
    maxs = np.amax(value_arr, axis=0)
    # invert, i.e. low duration / low emissions is bettter than high
    norm_value_arr = 1 - (value_arr - mins) / (maxs - mins)
    # For calories this does not hold, so flip it back
    norm_value_arr[:, 3] = 1 - norm_value_arr[:, 3]
    norm_value_arr = np.around(norm_value_arr, 2)
    return norm_value_arr


def sort_dictionary(out_dict):
    sorted_out_dict = {
        k: v
        for k, v in sorted(
            out_dict.items(),
            key=lambda item: item[1]['total_weighted_score'],
            reverse=True
        )
    }
    return sorted_out_dict


def total_weighted_score(norm_value_arr, norm_weights):
    # OLD VERSION: sum(norm_value_arr[i] * norm_weights)
    # NEW: rank:
    rank_array = np.zeros(norm_value_arr.shape)
    for j in range(norm_value_arr.shape[1]):
        rank_array[:, j] = rankdata(norm_value_arr[:, j], method="average")
    max_rank = norm_value_arr.shape[0] + 1
    # TESTING
    return np.dot(rank_array / max_rank, norm_weights)
