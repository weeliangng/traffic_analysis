from google.cloud import bigquery
#from google.oauth2 import service_account

def ingest_taxi_data(payload):

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
    for taxi_data in payload:
        for geometry in taxi_data['geometry_list']:
            rows_to_insert.append(
                {"timestamp": taxi_data['timestamp'], 
                "taxi_availability": geometry,
                "taxi_count": taxi_data['taxi_count'],
                "api_status": taxi_data['api_status']
                })
    batch_size = 120
    for i in range(0, len(rows_to_insert), batch_size):
        batch = rows_to_insert[i:i + batch_size]
        errors = client.insert_rows_json(table, batch, timeout = 1000)
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))