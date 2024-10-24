from components.exception_handler import NetmikoException_Handler,ThreadPoolExeceptionHandler
from concurrent.futures import ThreadPoolExecutor
from typing import Any,List,Tuple,Union,Callable
from assets.text_style import Text_Style
from assets.text_file import Text_File
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
    def custom_logger(logger_level=logging.INFO)->object:
        logger = logging.getLogger('Netmiko_Logger')
        logger.setLevel(logger_level)
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(os.path.join(os.getcwd(),"app.log"))
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
                filter_row = {key:value for key,value in row.items() if value}          ##Used to filter the valid  value from the csv
                my_filter_device_list.append(filter_row)
            
        return my_filter_device_list
    

    def initiate_netmiko_session(self,device_details):
        Text_Style.common_text(primary_text=Text_File.common_text['host_connecting'],secondary_text=device_details['ip'])
        print(f"This is the details which is used to connect the device {device_details}")          ##Just for the debug purpose
        session = ConnectHandler(**device_details)
        if session:
            Text_Style.common_text(primary_text=Text_File.common_text['connected_host'],secondary_text=session.host,secondary_text_color="green")
            return session
    
    @ThreadPoolExeceptionHandler
    def threaded_device_connection_executor(self,iterable_items:List,function_name=Callable[['str'],Any])->List:
        '''
        Thread Pool Executor to crate the multiple thred and connect with the device
        '''
        with ThreadPoolExecutor(max_workers=10) as executor:
            connections = executor.map(function_name,iterable_items)
            valid_connection = list(filter(lambda x: x != False and x != None,connections))      ##Filtering the valid connection only
            return valid_connection
    

    ###dont remove this line we will remove after our work will be executed
##logger_path = 
##mylogger = custom_logger(logger_name="Netmiko_Logger",logger_file_path=logger_path)