import os
import sys
import numpy as np
import pandas as pd
##THIS IS THE FILE WHERE WE WILL DEFINE ALL THE CONSTANTS RELATED TO TRAINING PIPELINE
print("🔥 LOADED TRAINING_PIPELINE.PY")
TARGET_COLUMN="CLASS_LABEL"
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="Phishing_Legitmate_full.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

SCHEMA_FILE_PATH = os.path.join(
    os.getcwd(),
    "data_schema",
    "schema.yaml"
)
DATA_INGESTION_DATABASE_NAME = "NetworkSecurity"
DATA_INGESTION_COLLECTION_NAME = "Phishing_Legitimate_full"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2
"""DATA VALIDATION RELATED CONSTANTS"""
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR:str="valid"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yaml"
DATA_VALIDATION_INVALID_DIR:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
"""DATA TRANSFORMATION RELATED CONSTANTS"""
DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR:str="transformed"
DATA_TRANSFORMATION_OBJECT_DIR:str="object"
PREPROCESSING_OBJECT_FILE_NAME:str="preprocessor.pkl"
##KKN IMPUTER RELATED CONSTANTS
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict={
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform",
}

