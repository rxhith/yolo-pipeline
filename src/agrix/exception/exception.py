import sys


class CustomException(Exception):
    def __init__(self , error_message , error_details : sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()
        self.line_number =exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f'Error in file {self.file_name}, line {self.line_number}: {self.error_message}'

