from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
@dataclass
class DataValidationArtifact: ##these are the output of data validation component which will be used by data transformation component
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str
@dataclass
class DataTransformationArtifact: 
    transformed_train_file_path:str ##preprocessed train data file path which will be used by model trainer component to train the model
    transformed_test_file_path:str
    transformed_object_file_path:str
@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    trained_metric_artifact:ClassificationMetricArtifact ##for calculated metric
    test_metric_artifact:ClassificationMetricArtifact