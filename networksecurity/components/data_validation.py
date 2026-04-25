import os
import sys
import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        try:
            logging.info(f"{'>>'*20} Data Validation Started {'<<'*20}")

            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

            # Load schema
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            print("SCHEMA PATH:", SCHEMA_FILE_PATH)
            print("SCHEMA DATA:", self._schema_config)
            if self._schema_config is None:
             raise Exception("Schema file is empty or not loaded properly")
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            expected_columns = len(self._schema_config["columns"])+1
            actual_columns = len(dataframe.columns)

            logging.info(f"Expected columns: {expected_columns}")
            logging.info(f"Actual columns: {actual_columns}")

            return expected_columns == actual_columns

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
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

            write_yaml_file(drift_report_file_path, report)

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            # File paths
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read data
            train_df = self.read_data(train_file_path)
            test_df = self.read_data(test_file_path)
            print(len(train_df.columns))
            print(train_df.columns)
            # Column validation
            if not self.validate_number_of_columns(train_df):
                raise Exception("Train dataframe does not match schema")

            if not self.validate_number_of_columns(test_df):
                raise Exception("Test dataframe does not match schema")

            # Drift detection
            drift_status = self.detect_dataset_drift(train_df, test_df)

            # Save valid data
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False)

            # Create artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data Validation Completed: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e