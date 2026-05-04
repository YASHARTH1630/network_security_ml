from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.classificationMetric import get_classification_score
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
import os
import mlflow
import dagshub
dagshub.init(repo_owner='YASHARTH1630', repo_name='network_security_ml', mlflow=True)
class ModelTrainer:
    def __init__(self, model_trainer_config, data_transformation_artifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def track_mlflow(self, best_model, classification_metric):##This function is used to track the mlflow metrics and model
        with mlflow.start_run():
            mlflow.log_metric("f1_score", classification_metric.f1_score)
            mlflow.log_metric("precision_score", classification_metric.precision_score)
            mlflow.log_metric("recall_score", classification_metric.recall_score)
            mlflow.sklearn.log_model(best_model, "model")

    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "Logistic Regression": LogisticRegression(),
                "AdaBoost": AdaBoostClassifier()
            }

            params = {
                "Decision Tree": {
                    'criterion': ['gini','entropy','log_loss'],
                    'splitter': ['best','random'],
                    'max_features': ['sqrt','log2']
                },
                "Random Forest": {
                    'criterion': ['gini','entropy','log_loss'],
                    'max_features': ['sqrt','log2'],
                    'n_estimators': [8,16,32,64,128]
                },
                "Gradient Boosting": {
                    'loss': ['log_loss','exponential'],
                    'learning_rate': [.01,.05,.001],
                    'n_estimators': [8,26,32,64,128,256]
                },
                "AdaBoost": {
                    'learning_rate': [.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression": {}
            }

            model_report = evaluate_models(
                X_train, y_train, X_test, y_test, models, params
            )

            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            # Train best model
            best_model.fit(X_train, y_train)

            # Train metrics
            y_train_pred = best_model.predict(X_train)
            train_metric = get_classification_score(y_train, y_train_pred)

            # Test metrics
            y_test_pred = best_model.predict(X_test)
            test_metric = get_classification_score(y_test, y_test_pred)

            self.track_mlflow(best_model, train_metric)##This is how we track the mlflow metrics and model for the training data
            self.track_mlflow(best_model, test_metric)##This is how we track the mlflow metrics and model for the test data

            preprocessor = load_object(
                self.data_transformation_artifact.transformed_object_file_path
            )

            network_model = NetworkModel(preprocessor, best_model)

            os.makedirs(os.path.dirname(
                self.model_trainer_config.trained_model_file_path), exist_ok=True)

            save_object(
                self.model_trainer_config.trained_model_file_path,
                network_model
            )
            save_object("final_model/model.pkl", best_model)
            return ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                trained_metric_artifact=train_metric,
                test_metric_artifact=test_metric
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self):
        try:
            train_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )

            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            return self.train_model(X_train, y_train, X_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys)