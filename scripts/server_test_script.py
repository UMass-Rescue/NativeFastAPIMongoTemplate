import requests
from azure.storage.blob import BlobClient
from pydantic import BaseModel


class PredictionInputBlobKey(BaseModel):
    blob_key: str


account_url = "https://jagathrescue.blob.core.windows.net/596e-backend"
credential = ""  # Get this from blob admin
blob_container = "596e-backend"

blob_key = "test_key"
message = "secret message 1234"


def write_to_blob(
    blob_key: str,
    message: str,
):
    blob = BlobClient(
        account_url=account_url,
        container_name=blob_container,
        blob_name=blob_key,
        credential=credential,
    )

    blob.upload_blob(message, overwrite=True)


write_to_blob(blob_key, message)
body = PredictionInputBlobKey(blob_key=blob_key)
response = requests.post(
    "http://localhost:8000/predict_worker_example/", json=body.dict()
)
print(response.text)
