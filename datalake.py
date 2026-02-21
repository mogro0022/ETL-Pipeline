import json
import datetime
from azure.storage.blob import BlobServiceClient


def save_to_datalake(raw_data: list, series_id: str, connection_string: str) -> str:
    if not raw_data:
        return "No data to save."

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_client = blob_service_client.get_container_client("raw-data")

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    blob_name = f"{series_id}-{timestamp}.json"

    blob_client = container_client.get_blob_client(blob_name)

    json_string = json.dumps(raw_data)
    blob_client.upload_blob(json_string, overwrite=True)

    return blob_name
