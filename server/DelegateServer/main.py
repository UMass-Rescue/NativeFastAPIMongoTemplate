from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Literal

import requests
import os

from azure.storage.blob import BlobClient
from pymongo import MongoClient

worker_example_hostname = os.getenv("WORKER_EXAMPLE_HOSTNAME", "worker_example")
worker_example_port = os.getenv("WORKER_EXAMPLE_PORT", "8001")
blob_account_url = os.getenv("BLOB_ACCOUNT_URL")
blob_credential = os.getenv("BLOB_CREDENTIAL")
blob_container = os.getenv("BLOB_CONTAINER")
mongo_hostname = os.getenv("MONGO_HOSTNAME", "mongo")
mongo_port = os.getenv("MONGO_PORT", "27018")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = MongoClient(mongo_hostname, int(mongo_port))
db = client.test_database


class PredictionInputBlobKey(BaseModel):
    blob_key: str


class PredictionInputWorkerExample(BaseModel):
    input_string: str = ""


class PredictionOutputWorkerExample(BaseModel):
    output_string: Literal["good", "bad", "error"] = "error"


def read_blob_to_string(blob_key: str):
    blob = BlobClient(
        account_url=blob_account_url,
        container_name=blob_container,
        blob_name=blob_key,
        credential=blob_credential,
    )
    return blob.download_blob().readall().decode("utf-8")


@app.post("/predict_worker_example/", response_model=PredictionOutputWorkerExample)
def predict_worker_example(body: PredictionInputBlobKey):
    try:
        input_string = read_blob_to_string(body.blob_key)
        new_input = PredictionInputWorkerExample(input_string=input_string)
        response = requests.post(
            f"http://{worker_example_hostname}:{worker_example_port}/predict/",
            json=new_input.dict(),
        )
        db.results.insert_one(response.json())
        return response.json()
    except Exception as e:
        print(f"Worker example not found {e}")
        return {"output_string": "error"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
