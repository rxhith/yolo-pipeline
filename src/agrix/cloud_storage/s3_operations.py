import os
import sys
import boto3
import concurrent.futures
import tqdm
from agrix.exception.exception import CustomException
from agrix.logger.logging import logging


class S3Operation:
    def __init__(self):
        """Initialize S3 operations with boto3 client instead of shell commands"""
        import multiprocessing
        self.s3_client = boto3.client('s3')
        # Set max workers based on CPU count
        # Use CPU count * 2 for I/O bound operations
        self.max_workers = min(32, multiprocessing.cpu_count() * 2)  # Cap at 32 to avoid overwhelming resources

    def sync_folder_to_s3(self, folder: str, bucket_name: str, bucket_folder_name: str) -> None:
        try:
            # Use the aws CLI sync command with progress bar
            # The --no-progress flag is removed to show progress
            command = f"aws s3 sync {folder} s3://{bucket_name}/{bucket_folder_name}/"
            os.system(command)
            logging.info("sync completed successfully")

        except Exception as e:
            raise CustomException(e, sys)

    def sync_folder_from_s3(self, bucket_name: str, bucket_folder_name: str, target_folder: str) -> None:
        try:
            # Check if target folder exists, create if it doesn't
            os.makedirs(target_folder, exist_ok=True)
            
            # List objects in the S3 bucket that need to be downloaded
            objects_to_download = []
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name, Prefix=bucket_folder_name)
            
            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        # Skip the directory itself
                        if obj['Key'] == bucket_folder_name or obj['Key'].endswith('/'):
                            continue
                        
                        # Get relative path
                        relative_path = obj['Key'][len(bucket_folder_name):].lstrip('/')
                        local_file_path = os.path.join(target_folder, relative_path)
                        
                        # Make sure the directory exists
                        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                        
                        objects_to_download.append((obj['Key'], local_file_path))
            
            # If no objects found, log and return
            if not objects_to_download:
                logging.info(f"No objects found in s3://{bucket_name}/{bucket_folder_name}")
                return
                
            # Use parallel downloads with progress bar
            print(f"Downloading {len(objects_to_download)} files from s3://{bucket_name}/{bucket_folder_name}")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Create a progress bar
                with tqdm.tqdm(total=len(objects_to_download), unit='file') as progress_bar:
                    futures = {}
                    
                    # Submit all download tasks
                    for s3_key, local_path in objects_to_download:
                        future = executor.submit(
                            self.s3_client.download_file, 
                            bucket_name, 
                            s3_key, 
                            local_path
                        )
                        futures[future] = s3_key
                    
                    # Process completed downloads and update progress bar
                    for future in concurrent.futures.as_completed(futures):
                        s3_key = futures[future]
                        try:
                            future.result()
                            # Update progress bar
                            progress_bar.update(1)
                        except Exception as e:
                            logging.error(f"Failed to download {s3_key}: {str(e)}")
                            raise CustomException(e, sys)
            
            logging.info("sync completed successfully")

        except Exception as e:
            raise CustomException(e, sys)