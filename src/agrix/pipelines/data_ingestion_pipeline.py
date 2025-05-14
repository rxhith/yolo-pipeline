from agrix.components.data_ingestion import DataIngestion
from agrix.entity.config_entity import ConfigurationManager
from agrix.cloud_storage.s3_operations import S3Operation
from agrix.cloud_storage.roboflow_operations import RoboflowOperation
from agrix.exception.exception import CustomException
from agrix.logger.logging import logging
import sys

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logging.info("Data Ingestion Pipeline Started")
            config_manager = ConfigurationManager()
            data_ingestion_config = config_manager.get_data_ingestion_config()
            
            roboflow_operation = RoboflowOperation()
            data_ingestion = DataIngestion(roboflow_operation,data_ingestion_config)
            data_ingestion.download_roboflow_data(workspace='new-workspace-mzjwd',project_name='kseb',version=1)
        except Exception as e:
            raise CustomException(e , sys)


if __name__ == "__main__":
    try:
        pipeline = DataIngestionPipeline()
        pipeline.main()
        logging.info(f"{STAGE_NAME} completed successfully")
    except Exception as e:
        raise CustomException(e , sys)