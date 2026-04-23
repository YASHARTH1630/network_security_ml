from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
import pandas as pd
import numpy as np
import k2_samp
from scipy.stats import ks_2samp
import os,sys
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=read_yaml_file(SCHEMA_FILE_PATH)   
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    @staticmethod ##this is a static method which will validate the data by comparing the distribution of the train and test data using KS test
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"Number of columns in the dataframe: {number_of_columns}")
           
            if len(dataframe.columns)==number_of_columns:
                logging.info(f"Number of columns in the dataframe is as expected: {number_of_columns}")
                return True
            else:
                logging.info(f"Number of columns in the dataframe is not as expected: {len(dataframe.columns)}")
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
  
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                ks_test = ks_2samp(d1, d2)
                drift_detected = ks_test.pvalue < threshold

                if drift_detected:
                    status = False

                report[column] = {
                    "p_value": float(ks_test.pvalue),
                    "drift_status": drift_detected
                }

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path, data=report)

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            ##read the train and test file
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            ##validate the columns in the train and test file
            status=self.validate_number_of_columns(train_dataframe)
            if not status: 
                error_message=f"Train dtframe doesn t contain all columns"
            status=self.detect_dataset_drift(base_df=train_dataframe,current_Df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False)
            ##create the data validation artifact
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e