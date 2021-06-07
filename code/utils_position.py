import numpy as np 
import json  
from typing import Mapping
import math
import sys


def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    if not isinstance(km, np.ndarray):
        return float(km*1000)

    return km*1000

def interchanges_string_to_int(data):
        
    for offer in data['offer_ids']:
        data[offer]['num_interchanges'] = int(data[offer]['num_interchanges'])

    return data

def leg_coords_string_to_int(data):
        
    for key in data.keys():
        for secondkey in data[key]['triplegs']:
            # print(secondkey)
            # print('-- '*5)
            data[key][secondkey]['leg_stops'] = json.loads(data[key][secondkey]['leg_stops'])

    return data


def transformStringToNum (data): 

    offer_keys = data['output_offer_level']['offer_ids']

    for offer in offer_keys: 

        trip_legs  = data['output_tripleg_level'][offer]['triplegs']

        data['output_offer_level'][offer]['num_interchanges'] = \
            int(data['output_offer_level'][offer]['num_interchanges'])

        for leg in trip_legs:
            data['output_tripleg_level'][offer][leg]['leg_stops'] = \
                json.loads(data['output_tripleg_level'][offer][leg]['leg_stops'])
            try:
                data['output_tripleg_level'][offer][leg]['leg_track'] = \
                    json.loads(data['output_tripleg_level'][offer][leg]['leg_track'])
            except:
                pass
    return data

def zscore(offers: Mapping, flipped = False) -> Mapping:
    n          = 0
    sum        = 0.0
    sum_square = 0.0

    for o in offers:
        value = offers[o]
        if value is not None:
            n = n + 1
            sum = sum + value
            sum_square = sum_square + value*value

    z_scores = {}
    if n > 0:
        average = sum / n
        std = math.sqrt(sum_square / n - average * average)
        for o in offers:
            value = offers[o]
            if value is not None:
                if std == 0:
                    z_scores[o] = 0
                else:
                    if not flipped:
                        z_scores[o] = (value - average)/std
                    else:
                        z_scores[o] = 1 - (value - average) / std
    return z_scores


def minmaxscore(offers: Mapping, flipped = False) -> Mapping:

    min = sys.float_info.max
    max = sys.float_info.min
    n   = 0
    for o in offers:
        value = offers[o]
        if value is not None:
            n = n + 1
            if value > max:
                max = value
            if value < min:
                min = value

    minmax_scores = {}
    diff = max - min
    if (n > 0):
        for o in offers:
            value = offers[o]
            if value is not None:
                if(diff > 0):
                    if not flipped:
                        minmax_scores[o] = (value-min)/diff
                    else:
                        minmax_scores[o] = 1 - (value-min)/diff
                else:
                    minmax_scores[o] = 0.5
    return minmax_scores

def get_distance_from_path(data):
    ''' 
    leg level input. (leg_stops, leg_track)

    '''
    if data['leg_track'] is not None:
        temp_path  = data['leg_track']['coordinates']
        new_path = list(zip(temp_path[:-1], temp_path[1:]))
        new_path  = np.array(new_path).reshape(len(temp_path) - 1,4)
        tl = new_path.shape[0]
        new_path = new_path.reshape(tl, 4)
        return float((haversine_np(new_path[:,0], new_path[:,1], new_path[:,2], new_path[:,3]).sum()))

    else: 
        origin_lat, origin_lon = data['leg_stops']['coordinates'][0][0], \
                data['leg_stops']['coordinates'][0][1] 

        dest_lat, dest_lon = data['leg_stops']['coordinates'][1][0], \
            data['leg_stops']['coordinates'][1][1]

        return haversine_np(origin_lon, origin_lat, dest_lon, dest_lat)

def get_road_distance(data):
    temp_legs = data['triplegs'] #list of legs

    total_dist = 0 #counter 

    for leg in temp_legs: #iterate over legs. 
        one_leg  = data[leg]
        if one_leg['transportation_mode'] in ['car',  'taxi', 'bus']: #if leg in modes using road

            #take coords...
            # origin_lat, origin_lon = one_leg['leg_stops']['coordinates'][0][0], \
            #     one_leg['leg_stops']['coordinates'][0][1] 
            # dest_lat, dest_lon = one_leg['leg_stops']['coordinates'][1][0], \
            #     one_leg['leg_stops']['coordinates'][1][1]

            # total_dist += haversine_np(origin_lon, origin_lat, dest_lon, dest_lat)
            total_dist += get_distance_from_path(one_leg)
    return float(total_dist)



def get_num_of_stops(offerID ,data):
    
    return data[offerID]['num_interchanges']



def get_num_of_legs(data):
    return len(data['triplegs'])

def getCoorsOrigin(data):
    temp_legs = data['triplegs'] #list of legs
    # for leg in temp_legs: #iterate over legs. 
    #     one_leg  = data[leg]
    #     if one_leg['transportation_mode'] in ['car',  'taxi', 'bus']: #if leg in modes using road

            #take coords...
    one_leg  = data[temp_legs[0]]
    origin_lat, origin_lon = one_leg['leg_stops']['coordinates'][0][0], \
        one_leg['leg_stops']['coordinates'][0][1] 

    return {'lat':  origin_lat, 'lon' : origin_lon}

def getCoorsDestination(data):
    temp_legs = data['triplegs'] #list of legs
    # for leg in temp_legs: #iterate over legs. 
    #     one_leg  = data[leg]
    #     if one_leg['transportation_mode'] in ['car',  'taxi', 'bus']: #if leg in modes using road

            #take coords...
    one_leg  = data[temp_legs[-1]]
    dest_lat, dest_lon = one_leg['leg_stops']['coordinates'][1][0], \
                one_leg['leg_stops']['coordinates'][1][1]

    return {'lat':  dest_lat, 'lon' : dest_lon}

def getTotalLenght(data):
    temp_legs = data['triplegs'] #list of legs

    total_dist = 0 #counter 

    for leg in temp_legs: #iterate over legs. 
        one_leg  = data[leg]
        #take coords...
        # origin_lat, origin_lon = one_leg['leg_stops']['coordinates'][0][0], \
        #     one_leg['leg_stops']['coordinates'][0][1] 
        # dest_lat, dest_lon = one_leg['leg_stops']['coordinates'][1][0], \
        #     one_leg['leg_stops']['coordinates'][1][1]

        # total_dist += haversine_np(origin_lon, origin_lat, dest_lon, dest_lat)

        total_dist += get_distance_from_path(one_leg)

    return float(total_dist)



def positionCollect(data, SCORES = "minmax_scores"):
    '''
    For each offer returns the congestion level (1:High - 5: Low) that trip will face: 

    The offers without car will automatically take the value 6

    ''' 
    data = transformStringToNum(data)
    req, offer_rew = data['output_tripleg_level'], data['output_offer_level']
    # requests_dict = {}
    offer_keys = list(req.keys())
    #print(offer_keys)

    road_dist, ratio_dist, total_stops, total_legs, origin, destination = {}, {}, {}, {}, {}, {}
    for one_offer in  offer_keys:
        temp_offer = req[one_offer] 

        # origin - destination distance road/air 
        road_dist[one_offer] =  get_road_distance(temp_offer)

        #car-bus-taxi/totalDistance ratio 
        ratio_dist[one_offer] =  road_dist[one_offer]/getTotalLenght(temp_offer)

        #num of stops 
        total_stops[one_offer] = get_num_of_stops(one_offer, offer_rew)

        #num_of_legs
        total_legs[one_offer] = get_num_of_legs(temp_offer)

        #lat-lon origin

        #lat-lon destination
        destination[one_offer] = getCoorsDestination(temp_offer)

    if SCORES == "minmax_scores":

        road_dist_norm = minmaxscore(road_dist)
        
        total_stops_norm = minmaxscore(total_stops)

        total_legs_norm = minmaxscore(total_legs)

        ratio_dist_norm = minmaxscore(ratio_dist)

    else:

        road_dist_norm = zscore(road_dist)
        
        total_stops_norm = zscore(total_stops)

        total_legs_norm = zscore(total_legs)

        ratio_dist_norm = zscore(ratio_dist)

    return {"road_dist" : road_dist, "ratio_dist": ratio_dist,  "total_stops"  : total_stops,"total_legs": total_legs,\
         "origin": origin, "destination" : destination , "road_dist_norm" : road_dist_norm , \
            "total_stops_norm" : total_stops_norm,  "total_legs_norm" : total_legs_norm, "ratio_dist_norm": ratio_dist_norm} 
