from typing import Any,List,Tuple,Union
import logging
import csv
import os


class Common_Function:
    def __init__(self):
        pass
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")
    
    @staticmethod
    def custom_logger(logger_name:str,logger_file_path:str,logger_level=logging.INFO)->object:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logger_level)
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(logger_file_path)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger
    
    @staticmethod
    def device_details_generator(device_details_file:str)->List:
        my_filter_device_list = []
        with open(device_details_file,mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                filter_row = {key:value for key,value in row.items() if value}
                my_filter_device_list.append(filter_row)
            
        return my_filter_device_list
    

    ###dont remove this line we will remove after our work will be executed
##logger_path = os.path.join(os.getcwd(),"app.log")
##mylogger = custom_logger(logger_name="Netmiko_Logger",logger_file_path=logger_path)