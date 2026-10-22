import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        if df.empty:
            return Response(
                content="Uploaded CSV is empty.",
                status_code=400
            )

        preprocessor = load_object("final_model/preprocessing.pkl")
        final_model = load_object("final_model/model.pkl")

        # Ensure that the loaded file contains a trained classifier,
        # not a NetworkModel wrapper or class.
        if isinstance(final_model, NetworkModel):
            raise ValueError(
                "model.pkl contains a NetworkModel wrapper. "
                "Run /train once to regenerate the model files."
            )

        # Remove target column if the uploaded CSV contains labels.
        if "Result" in df.columns:
            df = df.drop(columns=["Result"])

        # Match the exact feature order used during training.
        expected_columns = list(preprocessor.feature_names_in_)
        missing_columns = [
            col for col in expected_columns if col not in df.columns
        ]
        extra_columns = [
            col for col in df.columns if col not in expected_columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required feature columns: {missing_columns}"
            )

        if extra_columns:
            raise ValueError(
                f"Unexpected feature columns: {extra_columns}"
            )

        df = df[expected_columns]

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=final_model
        )

        y_pred = network_model.predict(df)

        result_df = df.copy()
        result_df["predicted_column"] = y_pred

        os.makedirs("prediction_output", exist_ok=True)
        result_df.to_csv(
            "prediction_output/output.csv",
            index=False
        )

        table_html = result_df.to_html(
            classes="table table-striped",
            index=False
        )

        return templates.TemplateResponse(
            request=request,
            name="table.html",
            context={
                "request": request,
                "table": table_html
            }
        )


    except Exception as e:
        logging.exception("Prediction failed")
        raise NetworkSecurityException(e, sys) from e


    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)