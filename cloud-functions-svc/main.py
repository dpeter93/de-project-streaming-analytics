import functions_framework
from google.cloud import bigquery
from google.cloud import secretmanager
import requests
import json
import os

@functions_framework.http
def kafka(request):

    # BigQuery configuration
    project_id = 'de-project-streaming-analytics'
    dataset_id = 'crm_data'
    table_id = 'crm_raw'
    kafka_user = 'UPSTASH_KAFKA_REST_USERNAME'
    kafka_pass = 'UPSTASH_KAFKA_REST_PASSWORD'

    # Secrets
    secretmanager_client = secretmanager.SecretManagerServiceClient()
    kafka_user_request = {"name": f"projects/{project_id}/secrets/{kafka_user}/versions/latest"}
    response = secretmanager_client.access_secret_version(kafka_user_request)
    kafka_user = response.payload.data.decode("UTF-8")
    
    kafka_pass_request = {"name": f"projects/{project_id}/secrets/{kafka_pass}/versions/latest"}
    response = secretmanager_client.access_secret_version(kafka_pass_request)
    kafka_pass = response.payload.data.decode("UTF-8")

    # Create a BigQuery client
    bigquery_client = bigquery.Client(project=project_id)

    # Query the last offset from the table
    query = f"""
        SELECT offset 
        FROM `{project_id}.{dataset_id}.{table_id}`
        ORDER BY offset DESC
        LIMIT 1
    """

    query_job = bigquery_client.query(query)

    result = query_job.result()

    last_offset = [row for row in result][0]['offset']

    # Kafka HTTP Get request
    kafka_url = "https://apt-doberman-7724-eu2-rest-kafka.upstash.io/fetch"
    kafka_headers = {
        "Content-Type": "application/json"
    }
    auth = (f"{kafka_user}", f"{kafka_pass}")

    kakfa_data = {
        "topic": "events",
        "partition": 0,
        "offset": f"{last_offset + 1}",
        "timeout": 1000
    }

    get_response = requests.post(kafka_url, headers=kafka_headers, auth=auth, json=kakfa_data)

    message = get_response.json()

    # dbt HTTP Post request
    dbt_url = "https://dbt-svc-ddrqznk4ga-uc.a.run.app/dbt"

    dbt_svc_headers = {
        "Content-Type": "application/json"
    }

    dbt_svc_data = {
        "params": {
            "cli": "run"
        }
    }

    json_data = json.dumps(dbt_svc_data)

    # Upload data to BigQuery and run dbt
    if len(message) != 0:

        table = bigquery_client.get_table(f'{project_id}.{dataset_id}.{table_id}')

        bigquery_client.load_table_from_json(message, table)

        post_response = requests.post(dbt_url, headers=dbt_svc_headers, data=json_data)

        print("Upload is done to BigQuery.")
        print(post_response.json())

        return f"There were {len(message)} new message. \nNew message(s): {message} \nUpload is done to BigQuery.\n{post_response.json()}"
    else:
        print("There is no new message.")

        return "There is no new message."

