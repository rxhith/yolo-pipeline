import logging
import os
from datetime import datetime

LOG_FILE = f'{datetime.now().strftime("%M_%d_%Y_%H_%M_%S")}'

log_path = os.path.join(os.getcwd(), 'logs')

os.makedirs(log_path,exist_ok=True)

LOG_FILEPATH = os.path.join(log_path,LOG_FILE)


logging.basicConfig(filename=LOG_FILEPATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
