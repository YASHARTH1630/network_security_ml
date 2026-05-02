import os 
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import (
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
    TARGET_COLUMN
)
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import (
    read_yaml_file,
    write_yaml_file,
    save_numpy_array_data,
    save_object
)
class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig,
                 ):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def get_data_transformer_object(self)->Pipeline:
        try:
            logging.info("Creating data transformer object")
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)##here two stars is used to unpack the dictionary of parameters for KNN imputer
            scaler=StandardScaler()
            preprocessor=Pipeline(steps=[
                ("imputer",imputer),
                ("scaler",scaler)
            ])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Reading validated train and test data")
            train_df=self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=self.read_data(self.data_validation_artifact.valid_test_file_path)
            ##training df
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            
            ##testing df
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            preprocessor_object=self.get_data_transformer_object()
            logging.info("Imputing missing values in the validated train and test data")
            preprocessor_object.fit(input_feature_train_df)
            transformed_feature_train_arr=preprocessor_object.transform(input_feature_train_df)
            transformed_feature_test_arr=preprocessor_object.transform(input_feature_test_df)
            train_arr=np.c_[transformed_feature_train_arr,np.array(target_feature_train_df)]##we are concatenating the transformed input feature and target feature of the train data to create a numpy array which will be used by model trainer component to train the model
            test_arr=np.c_[transformed_feature_test_arr,np.array(target_feature_test_df)]
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path,obj=preprocessor_object)
            ##prepare artifacts
            data_transformation_artifact=DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path)
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        