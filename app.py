import sys
import os
import certifi
from curl_cffi import Request

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
ca=certifi.where()
from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)
import pymongo
import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File, UploadFile
from uvicorn import run as app_run
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from networksecurity.utils.main_utils.utils import load_object
client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")
@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")
@app.get("/train")
async def train_route():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()
        return JSONResponse(content={"message":"Training pipeline executed successfully"})
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
@app.get("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df=pd.read_csv(file.file)
        preprocessor=load_object("final_model/preprocessor.pkl")
        model=load_object("final_model/model.pkl")
        network_model=NetworkModel(preprocessor=preprocessor,model=model)
        print(df.iloc[0])
        y_pred=network_model.predict(df)
        df.to_csv("prediction_output/output.csv", index=False)
        df["prediction_column"]=y_pred
        table_html=df.to_html(classes="table table-striped")
        return templates.TemplateResponse("prediction.html", {"request": request, "table_html": table_html})
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)