import dataharvester
import bigqueryingestor

def main():
    timestamp, geojson_data = dataharvester.extract_taxi_data()
    bigqueryingestor.ingest_taxi_data(timestamp, geojson_data)

if __name__ == "__main__":
    main()