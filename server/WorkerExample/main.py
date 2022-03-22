from fastapi import FastAPI

from pydantic import BaseModel
from typing import Literal

import random

app = FastAPI()


class PredictionInputWorkerExample(BaseModel):
    input_string: str = ""


class PredictionOutputWorkerExample(BaseModel):
    output_string: Literal["good", "bad", "error"] = "error"


@app.post("/predict/", response_model=PredictionOutputWorkerExample)
def predict(body: PredictionInputWorkerExample):
    return {"output_string": random.choice(["good", "bad"])}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
