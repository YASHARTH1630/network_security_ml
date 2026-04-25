from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
from networksecurity.entity.config_entity import DataIngestionConfig
import os,sys
import pandas as pd
import numpy as np
import pymongo
from sklearn.model_selection import train_test_split
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20}")
            self.data_ingestion_config=data_ingestion_config ##This is the object of DataIngestionConfig class which we will use to access all the variables defined in that class
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def export_collection_as_dataframe(self):
        """This function is used to export the collection from MongoDB as a dataframe"""
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name] ##This is how we access the collection in MongoDB using pymongo
            dataframe=pd.DataFrame(list(collection.find()))
            if"_id" in dataframe.columns:
                dataframe.drop("_id",axis=1,inplace=True) ##This is how we drop the _id column from the dataframe
            dataframe.replace({"na":np.nan},inplace=True) ##This is how we replace the "na" values with np.nan in the dataframe
            logging.info(f"Dataframe created with columns: {dataframe.columns}")
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        """This function is used to export the dataframe into the feature store directory"""
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_dir
            os.makedirs(os.path.dirname(feature_store_file_path),exist_ok=True) ##This is how we create the feature store directory if it does not exist
            dataframe.to_csv(feature_store_file_path,index=False) ##This is how we save the dataframe as a csv file in the feature store directory
            logging.info(f"Dataframe exported to feature store file: {feature_store_file_path}")
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
            dataframe,
            test_size=self.data_ingestion_config.train_test_split_ratio,
            random_state=42
        )

            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path

            os.makedirs(os.path.dirname(train_file_path), exist_ok=True)  # 🔥 FIX

            train_set.to_csv(train_file_path, index=False)
            test_set.to_csv(test_file_path, index=False)
            logging.info(f"Data split into train and test sets. Train file: {train_file_path}, Test file: {test_file_path}")

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    def initiate_data_ingestion(self):
        try:
           dataframe=self.export_collection_as_dataframe()
           self.export_data_into_feature_store(dataframe)
           self.split_data_as_train_test(dataframe)
           data_ingestion_artifact=DataIngestionArtifact(
               trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path
           )
           return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
           
           
         