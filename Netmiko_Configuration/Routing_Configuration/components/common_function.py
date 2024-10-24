from components.exception_handler import NetmikoException_Handler
from concurrent.futures import ThreadPoolExecutor
from typing import Any,List,Tuple,Union,Callable
from netmiko import ConnectHandler
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
    
    def device_details_generator(self,device_details_file:str)->List:
        my_filter_device_list = []
        with open(device_details_file,mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                filter_row = {key:value for key,value in row.items() if value}
                my_filter_device_list.append(filter_row)
            
        return my_filter_device_list
    

    def connectiontonetmiko_device(self,device_details):
        print(f"Trying to Connect with the device")
        session = ConnectHandler(**device_details)
        if session:
            print(f"Connected to the deivce succesfully {session.host}")
            return session
    
    def thread_pool_executor(self,iterable_items:List,function_name=Callable[['str'],Any])->List:
        '''
        Thread Pool Executor to crate the multiple thred and connect with the device
        '''
        with ThreadPoolExecutor(max_workers=10) as executor:
            connections = executor.map(function_name,iterable_items)
            valid_connection = list(filter(lambda x: x != False and x != None,connections))      ##Filtering the valid connection only
            return valid_connection
    

    ###dont remove this line we will remove after our work will be executed
##logger_path = os.path.join(os.getcwd(),"app.log")
##mylogger = custom_logger(logger_name="Netmiko_Logger",logger_file_path=logger_path)