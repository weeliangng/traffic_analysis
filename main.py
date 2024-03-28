import dataharvester

def main():
    timestamp, geojson_data = dataharvester.extract_taxi_data()
    print(timestamp)

if __name__ == "__main__":
    main()