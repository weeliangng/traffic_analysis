from google.cloud import bigquery
from google.oauth2 import service_account

def ingest_taxi_data(taxi_data):

    dataset_name = 'taxi_availability'
    table_name = 'taxi_availability'
    project_id = 'traffic-analysis-418408'

    #key_path = 'traffic-analysis-418408-05b85d3a4f63.json'

    #credentials = service_account.Credentials.from_service_account_file(key_path)

    #client = bigquery.Client(credentials=credentials)

    client = bigquery.Client()
    table_ref = client.dataset(dataset_name).table(table_name)

    table = client.get_table(table_ref)
    rows_to_insert = []
    for geometry in taxi_data['geometry_list']:
        rows_to_insert.append(
            {"timestamp": taxi_data['timestamp'], 
             "taxi_availability": geometry,
             "taxi_count": taxi_data['taxi_count'],
             "api_status": taxi_data['api_status']
             })


    errors = client.insert_rows_json(table, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))