import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
import os,sys
import numpy as np
import pandas as pd
import dill
import pickle

    


def read_yaml_file(file_path):
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
def write_yaml_file(file_path: str, data: dict, replace: bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as yaml_file:
            yaml.dump(data,yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
def save_object(file_path:str,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
def load_object(file_path:str)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file :{file_path}is not exist")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
def load_numpy_array_data(file_path:str)-> np.array:
    """load numpy_array data form file 
    file path :str location  of file to load
    return np.array data loaded"""
    try:
        with open(fiel_path,"rb") as file_obj:
           return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e 
        
    