from agrix.constants.training_pipeline import *
from agrix.utils.common import read_yaml,create_directories
from pathlib import Path
from agrix.entity.artifact_entity import (DataIngestionConfig , TrainingConfig , TrainingParamsConfig, MlflowConfig)
from agrix.exception.exception import CustomException
import sys

class ConfigurationManager:
    def __init__(self, config_file = CONFIG_FILE_PATH , params_file = PARAMS_FILE_PATH):
        self.config_file = read_yaml(config_file)
        self.params_file = read_yaml(params_file)
        create_directories([self.config_file.artifacts_root])

    try:
        def get_data_ingestion_config(self) -> DataIngestionConfig:
            data_config = self.config_file.data_ingestion
            create_directories([data_config.root_dir])
            data_ingestion_config = DataIngestionConfig(
                root_dir = data_config.root_dir,
                s3_bucket_name = data_config.bucket_name,
                s3_folder_name = data_config.bucket_folder_name,
            )

            return data_ingestion_config
        def get_training_config(self)-> TrainingConfig:
            train_config = self.config_file.model_training
            create_directories([train_config.root_dir])

            training_config = TrainingConfig(
                root_dir= train_config.root_dir,
                 data_yaml_file_path = train_config.training_data_yaml_dir,
                 yolo_pretrained_model_name= train_config.yolo_pretrained_weight_name,
                 model_path = train_config.trained_model_path,
                 onnx_model_path = train_config.onnx_model_path,
                 )
            return training_config
        
        def get_training_params(self)-> TrainingParamsConfig:
            params = self.params_file.params
            train_params = TrainingParamsConfig(

                nepochs= params.nepochs,
                batch_size= params.batch_size,
                imgsz = params.imgsz,
                lr0 = params.lr0,
                lrf = params.lrf,
                momentum = params.momentum,
                weight_decay = params.weight_decay,
                device = 0,
                warmup_epochs = params.warmup_epochs,
                warmup_momentum = params.warmup_momentum,
                warmup_bias_lr = params.warmup_bias_lr,
                hsv_h = params.hsv_h,
                hsv_s = params.hsv_s,
                hsv_v = params.hsv_v,
                degrees = params.degrees,
                translate = params.translate,
                scale = params.scale,
                shear = params.shear,
                perspective = params.perspective,
                flipud = params.flipud,
                fliplr = params.fliplr,
                mosaic = params.mosaic,
                mixup = params.mixup,
                copy_paste = params.copy_paste,
            )
            return train_params
        
        
        def get_mlflow_config(self)-> MlflowConfig:
            mlflow = self.config_file.mlflow_config
            mlflow_config = MlflowConfig(
                tracking_uri = mlflow.tracking_uri,
                experiment_name = mlflow.experiment_name,
                tracking_username = mlflow.tracking_username,
                tracking_password = mlflow.tracking_password
            )
            return mlflow_config
        
    except Exception as e:
        raise CustomException(e, sys)
