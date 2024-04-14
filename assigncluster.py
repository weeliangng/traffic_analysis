import geopandas as gpd
from google.cloud import bigquery
import plotly.express as px
from sklearn.cluster import DBSCAN
import pandas as pd

def get_bigquery_taxi_data(date_str):
    dataset_name = 'taxi_availability'
    table_name = 'taxi_availability'
    project_id = 'traffic-analysis-418408'

    query = f"""
    SELECT *
    FROM `{project_id}.{dataset_name}.{table_name}`
    where date(timestamp, "Asia/Singapore") = "{date_str}"
    ORDER BY timestamp ASC
    """
    client = bigquery.Client()

    df = client.query(query).to_geodataframe()
    if df.empty:
        raise ValueError(f"No data available for the specified date: {date_str}")
    else: return df


def assign_cluster(date_str):
    try: 
        df = get_bigquery_taxi_data(date_str)
    except ValueError as e:
        print(e)
    df.timestamp = df.timestamp.dt.tz_convert('Asia/Singapore')

    df_exploded = df.explode(index_parts=False)
    df_exploded["longitude"], df_exploded["latitude"] = df_exploded.taxi_availability.x, df_exploded.taxi_availability.y

    for timestamp in df_exploded['timestamp'].unique():
        subset = df_exploded.loc[df_exploded.timestamp == timestamp].copy()
        coords = subset[['latitude', 'longitude']]
        dbscan = DBSCAN(eps=0.003, min_samples=5)
        subset['cluster'] = dbscan.fit_predict(coords)
        df_exploded.loc[df_exploded['timestamp'] == timestamp, 'cluster'] = subset['cluster']
    #df_exploded = df_exploded.loc[df_exploded.cluster != -1]
    #df_exploded["cluster"] = df_exploded["cluster"].map(str)

