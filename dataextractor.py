import requests

def extract_taxi_data():
    url = "https://api.data.gov.sg/v1/transport/taxi-availability"
    response = requests.get(url)
    data = response.json()
    geojson_data = data['features'][0]
    timestamp = data['features'][0]['properties']['timestamp']
    return timestamp, geojson_data

def extract_taxi_data_timestamp(timestamp):
    #timestamp format = '2021-03-26T14:19:39+08:00'
    url = "https://api.data.gov.sg/v1/transport/taxi-availability"
    payload = {'date_time' : timestamp}
    response = requests.get(url, params = payload)
    data = response.json()
    geojson_data = data['features'][0]
    timestamp = data['features'][0]['properties']['timestamp']
    return timestamp, geojson_data


