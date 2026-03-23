import logging
import pandas as pd
from google.cloud import bigquery
from config import GCP_PROJECT_ID, BQ_DATASET

log = logging.getLogger(__name__)

def conectar_bigquery():
    client = bigquery.Client(project=GCP_PROJECT_ID)
    log.info("Conectado a BigQuery")
    return client

def cargar_tabla(client, records, table_name, schema, date_cols=[], numeric_cols=[]):
    df = pd.DataFrame(records).drop(columns=['attributes'])

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    table_id = f"{GCP_PROJECT_ID}.{BQ_DATASET}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=schema
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    log.info(f"{table_name}: {len(df)} registros cargados")
    
    