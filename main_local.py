import dataharvester
import bigqueryingestor
import assigncluster


def get_backdated_taxi_data(date_str):
  payload = dataharvester.extract_taxi_data_date(date_str)
  bigqueryingestor.ingest_taxi_data(payload)

def get_latest_taxi_data():
  taxi_data = dataharvester.extract_taxi_data()
  bigqueryingestor.ingest_taxi_data(taxi_data)

def main_local(date_str):
  get_backdated_taxi_data(date_str)
  assigncluster.assign_cluster(date_str)

