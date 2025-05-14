from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir : Path
    s3_bucket_name : str
    s3_folder_name : str

@dataclass(frozen=True)
class TrainingConfig:
    root_dir : Path
    data_yaml_file_path : Path
    yolo_pretrained_model_name: str
    model_path : Path
    onnx_model_path : Path

@dataclass(frozen=True)
class TrainingParamsConfig:
    nepochs : int
    batch_size : int
    imgsz : int
    lr0: float
    lrf: float
    momentum: float
    weight_decay: float
    warmup_epochs: float
    warmup_momentum: float
    warmup_bias_lr: float
    hsv_h: float
    hsv_s: float
    hsv_v: float
    degrees: float
    translate: float 
    scale: float  
    shear: float  
    perspective: float
    flipud: float
    fliplr: float
    mosaic: float   
    mixup:  float  
    copy_paste: float
    device : int

@dataclass(frozen=True)
class MlflowConfig:
     tracking_uri : str
     experiment_name : str
     tracking_username : str
     tracking_password : str