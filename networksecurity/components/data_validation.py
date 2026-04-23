from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import os,sys
from networksecurity.utils.main_utils.utils import read_yaml_file
class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=read_yaml_file(SCHEMA_FILE_PATH)   
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
