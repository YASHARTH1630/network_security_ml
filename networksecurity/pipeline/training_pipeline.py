import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.logging.logging import logging
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,TrainingPipelineConfig
)
class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion is completed")
            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_validation_config=data_validation_config,
                                           data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,
                                                 data_transformation_config=data_transformation_config)
            return data_transformation.initiate_data_transformation()
        except Exception as e:  
            raise NetworkSecurityException(e,sys) from e
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,
                                      data_transformation_artifact=data_transformation_artifact)    
            return model_trainer.initiate_model_trainer()   

        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e