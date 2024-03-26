import dataextractor

def main():
    timestamp, geojson_data = dataextractor.extract_taxi_data()
    print(timestamp)

if __name__ == "__main__":
    main()