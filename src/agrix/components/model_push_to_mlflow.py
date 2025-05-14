import mlflow , mlflow.onnx
from agrix.entity.artifact_entity import (MlflowConfig , TrainingConfig)
from agrix.logger.logging import logging
from agrix.exception.exception import CustomException
import os , sys
from ultralytics import YOLO
import onnx


class ModelPusher:
    def __init__(self, mlflow_config: MlflowConfig , training_config: TrainingConfig):
        self.mlflow_config = mlflow_config
        self.training_config = training_config

    def initiate_model_pusher(self):
        logging.info("Entered initiate_model_pusher method of ModelPusher class")
        try:
            os.environ["MLFLOW_TRACKING_URI"] = self.mlflow_config.tracking_uri
            os.environ["MLFLOW_EXPERIMENT_NAME"] = self.mlflow_config.experiment_name
            os.environ["MLFLOW_TRACKING_USERNAME"] = self.mlflow_config.tracking_username
            os.environ["MLFLOW_TRACKING_PASSWORD"] = self.mlflow_config.tracking_password

            client = mlflow.tracking.MlflowClient()
            experiment_name = self.mlflow_config.experiment_name
            experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
            runs = client.search_runs(experiment_id , order_by=["attribute.end_time DESC"], max_results=1)
            if runs:
                last_run = runs[0]
                run_id = last_run.info.run_id
                model_path  = str(self.training_config.onnx_model_path)
                model_artifact_path = f'mlflow-artifacts://{run_id}/artifacts/onnx_model/best.onnx'
                mlflow.log_artifact(model_path , "onnx_model",run_id=run_id)
                mlflow.register_model(model_uri=model_artifact_path, name='cricket_model_yolov8x')
                
                logging.info(f"Model pushed successfully to experiment: {experiment_name}, run_id: {run_id}")
                os.system(f"rm -rf runs")
            else:
                logging.info("No runs found")

        except Exception as e:
            raise CustomException(e, sys)
