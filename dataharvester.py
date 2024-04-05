import requests
import json
import geojson

def extract_taxi_data():
    url = "https://api.data.gov.sg/v1/transport/taxi-availability"
    response = requests.get(url)
    featurecollection = response.json()
    features = extract_features_from_collection(featurecollection)
    timestamp = featurecollection['features'][0]['properties']['timestamp']
    return timestamp, features

def extract_taxi_data_timestamp(timestamp):
    #timestamp format = '2021-03-26T14:19:39+08:00'
    url = "https://api.data.gov.sg/v1/transport/taxi-availability"
    payload = {'date_time' : timestamp}
    response = requests.get(url, params = payload)
    featurecollection = response.json()
    features = extract_features_from_collection(featurecollection)
    timestamp = featurecollection['features'][0]['properties']['timestamp']
    return timestamp, features

def extract_features_from_collection(featurecollection):
    features = []
    feature_properties = featurecollection['features'][0]['properties']
    for feature in featurecollection['features']:
        feature['properties'] = feature_properties
        print(type(feature))
        features.append(feature)
    return features
