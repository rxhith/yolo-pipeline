import os
import sys
import zipfile
import shutil
from pathlib import Path
from roboflow import Roboflow
from agrix.exception.exception import CustomException
from agrix.logger.logging import logging


class RoboflowOperation:
    def __init__(self):
        """Initialize Roboflow operations with API key"""
        self.api_key = 'ZYZPf5J2xQcg5nT8oExI'
        self.rf = Roboflow(api_key=self.api_key)

    def download_dataset(self, workspace: str, project_name: str, version: int, target_folder: Path, format="yolov8") -> None:
        """
        Downloads dataset from Roboflow, extracts it, and stores in target folder
        
        Args:
            workspace: Roboflow workspace name
            project_name: Roboflow project name
            version: Version number of the dataset
            target_folder: Path where to store the extracted dataset
            format: Format of the dataset (default is yolov8)
        """
        try:
            logging.info(f"Downloading Roboflow dataset from workspace: {workspace}, project: {project_name}, version: {version}")
            
            # Create temp directory for download
            temp_dir = os.path.join(os.getcwd(), "temp_download")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Download dataset
            project = self.rf.workspace(workspace).project(project_name)
            version_obj = project.version(version)
            
            # Download to the current directory (Roboflow API will handle this)
            # The API returns a Dataset object, not a path
            dataset = version_obj.download(format)
            
            # Get the dataset location - this is typically a property of the Dataset object
            # If the location isn't directly accessible, we need to look for the downloaded files
            logging.info(f"Dataset downloaded: {dataset}")
            
            # Look for the downloaded dataset in the current directory
            # Roboflow typically creates a directory like <project_name>-<version>-<format>
            possible_paths = []
            for item in os.listdir(os.getcwd()):
                item_path = os.path.join(os.getcwd(), item)
                if os.path.isdir(item_path) and (project_name in item or workspace in item):
                    possible_paths.append(item_path)
            
            if not possible_paths:
                # Try to get dataset path from dataset object if available
                try:
                    if hasattr(dataset, 'location'):
                        possible_paths.append(dataset.location)
                    elif hasattr(dataset, 'path'):
                        possible_paths.append(dataset.path)
                except:
                    pass
                    
            if not possible_paths:
                raise Exception("Could not find downloaded dataset directory")
                
            # Use the most recently created directory
            downloaded_path = max(possible_paths, key=os.path.getctime)
            logging.info(f"Identified dataset location: {downloaded_path}")
            
            # Move all contents from downloaded path to target folder
            if os.path.exists(downloaded_path):
                # Ensure target folder exists
                os.makedirs(target_folder, exist_ok=True)
                
                # Copy all contents from downloaded path to target folder
                for item in os.listdir(downloaded_path):
                    src_item = os.path.join(downloaded_path, item)
                    dst_item = os.path.join(target_folder, item)
                    
                    if os.path.isdir(src_item):
                        # If it's a directory, copy the entire directory
                        if os.path.exists(dst_item):
                            shutil.rmtree(dst_item)
                        shutil.copytree(src_item, dst_item)
                    else:
                        # If it's a file, copy the file
                        shutil.copy2(src_item, dst_item)
                
                # Clean up downloaded directory
                shutil.rmtree(downloaded_path)
                logging.info(f"Dataset moved successfully to {target_folder}")
            else:
                raise Exception(f"Downloaded path {downloaded_path} does not exist")
            
        except Exception as e:
            logging.error(f"Error during Roboflow dataset download: {str(e)}")
            raise CustomException(e, sys) 