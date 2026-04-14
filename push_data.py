import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(f"MongoDB URL: {MONGO_DB_URL}")
import certifi
ca=certifi.where()
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def csv_to_json(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(inplace=True, drop=True)
            records=list(df.T.to_dict().values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def insert_data_to_mongodb(self, records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.client=pymongo.MongoClient(MONGO_DB_URL)
            self.db=self.client[self.database]
            self.col=self.db[self.collection]
            self.col.insert_many(self.records)
            return "Data inserted successfully"
        except Exception as e:
            raise NetworkSecurityException(e, sys)
if __name__=="__main__":
    FILE_PATH="notebook/Phishing_Legitimate_full.csv"
    DATABASE="NetworkSecurity"
    COLLECTION="Phishing_Legitimate_full"
    networkobject=NetworkDataExtract()
    records=networkobject.csv_to_json(FILE_PATH)
    no_of_records=networkobject.insert_data_to_mongodb(records,DATABASE,COLLECTION)
    print(no_of_records)