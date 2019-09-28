#!/usr/bin/env python
# coding: utf-8

import numpy as np
import json

def compute_score(info_dic, out_dic, weights = [1,1,1,1], transport_list=["car","bike", "walk"]):
    norm_weights = weights/np.sum(weights)

    # check: duration in minutes, distances in km
    value_arr = np.zeros((len(out_dic.keys()), 4))
    for i, transport in enumerate(sorted(out_dic.keys())):
        d = out_dic[transport]["distance"]*0.001 # distance
        m = out_dic[transport]["duration"] # duration
        infos = info_dic[transport]
        e = infos["emissionsProKM"]*d # emissions
        if "price_fahrt" in infos:
            p = infos["price_fahrt"] # price
        elif "priceKm" in infos:
            p = infos["priceKm"]*d
        else:
            p = infos["priceProMin"]*m
        c = infos["caloriesPerMin"]*m # calories
        value_arr[i] = [m,e,p,c]
        out_dic[transport] = {"emission": round(e,2), "calories":round(c,2), "price":round(p,2), "distance":round(d,2), "duration":round(m,2)}
    mins = np.amin(value_arr, axis=0)
    maxs = np.amax(value_arr, axis=0)
    norm_value_arr = 1-(value_arr-mins)/(maxs-mins) # normalize and invert at the same time, i.e. high score is good
    norm_value_arr[:,3] = 1-norm_value_arr[:,3] # calories needs to be inverted
    norm_value_arr = np.around(norm_value_arr, 2)

    colours = [[245, 53, 53], [255, 128,0], [255,255,0],[153,255,51], [0,153,0]]
    colour_scores = [1,3,5,7,9]
    for i, transport in enumerate(sorted(out_dic.keys())):
        for j, score_name in enumerate(["duration_score", "emission_score", "price_score", "calories_score"]):
            out_dic[transport][score_name] = norm_value_arr[i,j]
        for j, score_name in enumerate(["duration_col", "emission_col", "price_col", "calories_col"]):
            closest = np.argmin(np.abs(colour_scores-norm_value_arr[i,j]*10))
            out_dic[transport][score_name] = colours[closest]
        total_score = sum(norm_value_arr[i]*norm_weights)
        out_dic[transport]["total_weighted_score"] = total_score
        closest_total = np.argmin(np.abs(colour_scores-total_score*10))
        out_dic[transport]["total_weighted_score_col"] = colours[closest_total]
    return out_dic


if __name__=="__main__":
    with open("emission_infos.json", "r") as infile:
        dic = json.load(infile)
    out_dic = compute_score(dic, {"car":{"duration":5, "distance":1000}, "walk":{"duration":10, "distance":1100},
                              "bike":{"duration":3, "distance":700}}, weights=[1,1,1,1])
    print(out_dic)
