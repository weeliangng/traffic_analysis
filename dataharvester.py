import requests
import json
from shapely.geometry import shape
import backdatedtimestamp

def extract_taxi_data():
    url = "https://api.data.gov.sg/v1/transport/taxi-availability"
    response = requests.get(url)
    featurecollection = response.json()
    geometry_list = extract_geometry_from_collection(featurecollection)
    timestamp = featurecollection['features'][0]['properties']['timestamp']
    taxi_count = featurecollection['features'][0]['properties']['taxi_count']
    api_status = featurecollection['features'][0]['properties']['api_info']['status']
    return [{
        'timestamp': timestamp, 
        'taxi_count': taxi_count, 
        'geometry_list': geometry_list, 
        'api_status': api_status}]

def extract_taxi_data_timestamp(timestamp):
    #timestamp format = '2021-03-26T14:19:39+08:00'
    url = "https://api.data.gov.sg/v1/transport/taxi-availability"
    payload = {'date_time' : timestamp}
    response = requests.get(url, params = payload)
    featurecollection = response.json()
    geometry_list = extract_geometry_from_collection(featurecollection)
    timestamp = featurecollection['features'][0]['properties']['timestamp']
    taxi_count = featurecollection['features'][0]['properties']['taxi_count']
    api_status = featurecollection['features'][0]['properties']['api_info']['status']
    return [{
        'timestamp': timestamp, 
        'taxi_count': taxi_count, 
        'geometry_list': geometry_list, 
        'api_status': api_status}]

def extract_taxi_data_date(date_str):
    minute_intervals_str = backdatedtimestamp.get_datetime_intervals(date_str)
    payload = []
    for time_intervals in minute_intervals_str:
        taxi_data = extract_taxi_data_timestamp(time_intervals)
        payload += taxi_data
    return payload

def extract_geometry_from_collection(featurecollection):
    geometry_list = []
    for feature in featurecollection['features']:
        geometry_list.append(convert_feature_to_geometry(feature))
    return geometry_list

def convert_feature_to_geometry(feature):
    geometry = shape(feature['geometry'])
    wkt_data = geometry.wkt
    return wkt_data
