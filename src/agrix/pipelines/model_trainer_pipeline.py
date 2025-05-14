from agrix.entity.config_entity import ConfigurationManager
from agrix.components.model_trainer import ModelTrainer , MlflowConfig
from agrix.logger.logging import logging
from agrix.exception.exception import CustomException

class ModelTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        training_config = config.get_training_config()
        training_params = config.get_training_params()
        mlflow_config = config.get_mlflow_config()
        
        
        model_trainer = ModelTrainer(training_config , training_params, mlflow_config)

        model_trainer.initiate_model_trainer()


if __name__ == "__main__":
    obj = ModelTrainingPipeline()
    obj.main() 