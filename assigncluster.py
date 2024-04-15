from google.cloud import bigquery
from sklearn.cluster import DBSCAN


def get_bigquery_taxi_data(date_str):
    '''Takes date_str in the format of yyyy-mm-dd'''
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
    job = client.query(query)
    result = job.result()
    df = result.to_geodataframe()
    if df.empty:
        raise ValueError(f"No data available for the specified date: {date_str}")
    else: return df

def prepare_data(df):
    df.timestamp = df.timestamp.dt.tz_convert('Asia/Singapore')
    df_exploded = df.explode(index_parts=False)
    df_exploded["longitude"], df_exploded["latitude"] = df_exploded.taxi_availability.x, df_exploded.taxi_availability.y
    return df_exploded
    
def write_cluster_data(df):
    client = bigquery.Client()
    dataset_name = 'taxi_availability'
    table_name = 'taxi_availability_cluster'
    project_id = 'traffic-analysis-418408'
    table_id = "{0}.{1}.{2}".format(project_id, dataset_name, table_name)
    job_config = bigquery.LoadJobConfig(schema=[bigquery.SchemaField("timestamp", "TIMESTAMP"),
                                                bigquery.SchemaField("taxi_count","INTEGER"),
                                                bigquery.SchemaField("longitude", "FLOAT"),
                                                bigquery.SchemaField("latitude", "FLOAT"),
                                                bigquery.SchemaField("cluster", "INTEGER")])
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

def assign_cluster(date_str):
    '''Takes date_str in the format of yyyy-mm-dd'''
    try: 
        df = get_bigquery_taxi_data(date_str)
    except ValueError as e:
        raise (e)
    df_exploded = prepare_data(df)

    for timestamp in df_exploded['timestamp'].unique():
        subset = df_exploded.loc[df_exploded.timestamp == timestamp].copy()
        coords = subset[['latitude', 'longitude']]
        dbscan = DBSCAN(eps=0.003, min_samples=5)
        subset['cluster'] = dbscan.fit_predict(coords)
        df_exploded.loc[df_exploded['timestamp'] == timestamp, 'cluster'] = subset['cluster']
    #df_exploded = df_exploded.loc[df_exploded.cluster != -1]
    #df_exploded["cluster"] = df_exploded["cluster"].map(str)
    write_cluster_data(df_exploded[["timestamp", "taxi_count", "longitude", "latitude", "cluster"]])
    



