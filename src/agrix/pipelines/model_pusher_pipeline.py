from agrix.entity.config_entity import ConfigurationManager
from agrix.exception.exception import CustomException
from agrix.components.model_push_to_mlflow import ModelPusher
import sys


class ModelPusherPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            training_config = config.get_training_config()
            mlflow_config = config.get_mlflow_config()
            model_pusher = ModelPusher(mlflow_config,training_config)
            model_pusher.initiate_model_pusher()

        except Exception as e:
            raise CustomException(e, sys)
        

if __name__ == "__main__":
    obj = ModelPusherPipeline()
    obj.main()

