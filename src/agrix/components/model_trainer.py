import os
import sys
from agrix.logger.logging import logging
from agrix.exception.exception import CustomException
from agrix.entity.artifact_entity import (TrainingConfig, TrainingParamsConfig, MlflowConfig)
from pathlib import Path
from ultralytics import YOLO


class ModelTrainer:
    def __init__(
            self,
            traininig_config: TrainingConfig,
            training_params_config: TrainingParamsConfig,
            mlflow_config: MlflowConfig,
    ):
        self.traininig_config = traininig_config
        self.training_params_config = training_params_config
        self.mlflow_config = mlflow_config

    def initiate_model_trainer(self):
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            os.environ["MLFLOW_TRACKING_URI"] = self.mlflow_config.tracking_uri
            os.environ["MLFLOW_EXPERIMENT_NAME"] = self.mlflow_config.experiment_name
            os.environ["MLFLOW_TRACKING_USERNAME"] = self.mlflow_config.tracking_username
            os.environ["MLFLOW_TRACKING_PASSWORD"] = self.mlflow_config.tracking_password
            data_yaml_path = os.path.join(os.path.dirname(__file__), str(self.traininig_config.data_yaml_file_path))

            logging.info("Training started at: %s" % data_yaml_path)
            model = YOLO(self.traininig_config.yolo_pretrained_model_name, task='train')
            
            try:
                model.train(
                    data=data_yaml_path,
                    epochs=self.training_params_config.nepochs,
                    batch=self.training_params_config.batch_size,
                    imgsz=self.training_params_config.imgsz,
                    name='results',
                    project='agrix_model',
                )
                
                logging.info("Training completed")
                
                # Export model only if training completed successfully
                model_path = Path("agrix_model/results/weights/best.pt")
                destination_path = os.path.join(self.traininig_config.root_dir, "best.pt")
                os.system(f"cp {model_path} {destination_path}")
                logging.info("model exporting started")
                model = YOLO(self.traininig_config.model_path, task='detect')
                model.export(format='onnx', task='detect')
                
            except Exception as e:
                logging.error(f"Error during model training: {e}")
                raise e
            finally:
                # Clean up regardless of training success or failure
                logging.info("Cleaning up temporary directories")
                os.system(f"rm -rf agrix_model")
                os.system(f"rm -rf runs")

        except Exception as e:
            raise CustomException(e, sys)