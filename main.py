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
    payload = dataharvester.extract_taxi_data_date(date_str)
    bigqueryingestor.ingest_taxi_data(payload)

if __name__ == "__main__":
    main()