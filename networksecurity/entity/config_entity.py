from datetime import datetime
import os
from networksecurity.constant import training_pipeline
class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(os.getcwd(),self.artifact_name)
        self.timestamp:str=timestamp
        
class DataIngestionConfig: ##this is the configuration class for data ingestion component which will be used by data ingestion component to ingest the data and store it in the artifact directory
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(## this is the directory where the data will be ingested and stored
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        ) 
        self.feature_store_dir:str=os.path.join(## this is the directory where the feature store will be stored
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME
        )   
        self.training_file_path :str=os.path.join(## this is the file path where the training data will be stored
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path :str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio:float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        
        self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME## this is the collection name where the data will be ingested in the database
        self.database_name:str=training_pipeline.DATA_INGESTION_DATABASE_NAME## this is the database name where the data will be ingested in the database
class DataValidationConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir:str=os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir:str=os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path:str=os.path.join(
            self.valid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )
        self.valid_test_file_path:str=os.path.join(
            self.valid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )
        self.invalid_train_file_path:str=os.path.join(
            self.invalid_data_dir,
            training_pipeline.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path:str=os.path.join(
            self.invalid_data_dir,
            training_pipeline.TEST_FILE_NAME
        )
        self.drift_report_dir: str = os.path.join(
             self.data_validation_dir,
              training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR
        )
        self.drift_report_file_path:str=os.path.join(## this is the file path where the drift report will be stored(how the distribution of the train and test data is different)
            self.drift_report_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )
class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )
        self.transformed_train_file_path:str=os.path.join(## this is the file path where the transformed train data will be stored
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv","npy"))
        self.transformed_test_file_path:str=os.path.join(## this is the file path where the transformed train data will be stored
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv","npy"))
        self.transformed_object_file_path:str=os.path.join(## this is the file path where the transformed object will be stored(object is the preprocessor object which will be used to transform the data)
            self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_OBJECT_DIR,training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)