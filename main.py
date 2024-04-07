import functions_framework

import dataharvester
import bigqueryingestor
import backdatedtimestamp 

def main():
    taxi_data = dataharvester.extract_taxi_data()
    bigqueryingestor.ingest_taxi_data(taxi_data)

# Register an HTTP function with the Functions Framework
@functions_framework.http
def get_taxi_availability_function(request):
  # Your code here
    main()
  # Return an HTTP response
    return 'OK'

def get_backdated_taxi_data(date_str):
    minute_intervals_str = backdatedtimestamp.get_datetime_intervals(date_str)
    for time_intervals in minute_intervals_str:
        taxi_data = dataharvester.extract_taxi_data_timestamp()
        bigqueryingestor.ingest_taxi_data(taxi_data)

if __name__ == "__main__":
    main()