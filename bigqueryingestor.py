from google.cloud import bigquery

dataset_name = 'traffic-analysis'
table_name = 'taxi_availability'
project_id = 'traffic-analysis-418408'

client = bigquery.Client()
table_ref = client.dataset(dataset_name).table(table_name)

table = client.get_table(table_ref)