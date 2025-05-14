from agrix.pipelines.model_trainer_pipeline import ModelTrainingPipeline
from agrix.pipelines.model_pusher_pipeline import ModelPusherPipeline
from agrix.pipelines.data_ingestion_pipeline import DataIngestionPipeline

obj = DataIngestionPipeline()
obj.main()
obj = ModelTrainingPipeline()
obj.main()
obj1 = ModelPusherPipeline()
obj1.main()