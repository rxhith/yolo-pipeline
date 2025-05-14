from agrix.cloud_storage.s3_operations import S3Operation
from agrix.entity.artifact_entity import DataIngestionConfig
from agrix.exception.exception import CustomException
import sys
from agrix.logger.logging import logging

class DataIngestion:
    def __init__(self, s3_operations: S3Operation,config: DataIngestionConfig):
        self.s3_operations = s3_operations
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