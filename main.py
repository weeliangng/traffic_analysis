import functions_framework

import backdatedtimestamp
import assigncluster
import main_local

# Register an HTTP function with the Functions Framework


@functions_framework.http
def get_previous_day_taxi_data(request):
  yesterday_string = backdatedtimestamp.yesterday_date_string()
  main_local.get_backdated_taxi_data(yesterday_string)
  # Return an HTTP response
  return 'OK'

@functions_framework.http
def label_previous_day_taxi_data(request):
  # Your code here
  yesterday_string = backdatedtimestamp.yesterday_date_string()
  assigncluster.assign_cluster(yesterday_string)
  # Return an HTTP response
  return 'OK'

