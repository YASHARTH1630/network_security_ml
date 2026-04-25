from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
import os
import sys
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def predict(self ,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_predict)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
            