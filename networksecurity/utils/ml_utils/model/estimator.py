from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logging import logging
import os
import sys

class NetworkModel: ##this class is used to save the preprocessor and model together in one file and use it for prediction
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
    def predict(self ,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
            