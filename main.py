import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=dataingestionconfig)
        logging.info("Starting data ingestion")
        data_ingestion.initiate_data_ingestion()
        print("Data Ingestion completed successfully")
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
