from agrix.cloud_storage.s3_operations import S3Operation
from agrix.cloud_storage.roboflow_operations import RoboflowOperation
from agrix.entity.artifact_entity import DataIngestionConfig
from agrix.exception.exception import CustomException
import sys
from agrix.logger.logging import logging

class DataIngestion:
    def __init__(self, roboflow_operations: RoboflowOperation, config: DataIngestionConfig):
        
        self.roboflow_operations = roboflow_operations
        self.config = config


    def sync_data(self):
        try:
            logging.info("sync folder from S3 started")
            self.s3_operations.sync_folder_from_s3(
            self.config.s3_bucket_name,
            self.config.s3_folder_name,
            self.config.root_dir
        )
            
        except Exception as e:
            raise CustomException(e ,sys)
            
    def download_roboflow_data(self, workspace: str, project_name: str, version: int, format="yolov8"):
        try:
            logging.info("Downloading data from Roboflow started")
            self.roboflow_operations.download_dataset(
                workspace=workspace,
                project_name=project_name,
                version=version,
                target_folder=self.config.root_dir,
                format=format
            )
            logging.info("Roboflow data download completed successfully")
            
        except Exception as e:
            raise CustomException(e, sys)