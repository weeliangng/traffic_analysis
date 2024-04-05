import functions_framework

import dataharvester
import bigqueryingestor

def main():
    timestamp, geojson_data = dataharvester.extract_taxi_data()
    bigqueryingestor.ingest_taxi_data(timestamp, geojson_data)

# Register an HTTP function with the Functions Framework
@functions_framework.http
def get_taxi_availability_function(request):
  # Your code here
    main()
  # Return an HTTP response
    return 'OK'


if __name__ == "__main__":
    main()