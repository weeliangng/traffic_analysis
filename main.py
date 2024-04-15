import functions_framework

import dataharvester
import bigqueryingestor
import backdatedtimestamp
import assigncluster

# Register an HTTP function with the Functions Framework


@functions_framework.http
def get_previous_day_taxi_data(request):
  yesterday_string = backdatedtimestamp.yesterday_date_string()
  get_backdated_taxi_data(yesterday_string)
  # Return an HTTP response
  return 'OK'

@functions_framework.http
def label_previous_day_taxi_data(request):
  # Your code here
  yesterday_string = backdatedtimestamp.yesterday_date_string()
  assigncluster.assign_cluster(yesterday_string)
  # Return an HTTP response
  return 'OK'

def get_backdated_taxi_data(date_str):
  payload = dataharvester.extract_taxi_data_date(date_str)
  bigqueryingestor.ingest_taxi_data(payload)

def get_latest_taxi_data():
  taxi_data = dataharvester.extract_taxi_data()
  bigqueryingestor.ingest_taxi_data(taxi_data)

