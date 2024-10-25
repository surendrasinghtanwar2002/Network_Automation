from components.exception_handler import NetmikoException_Handler,ThreadPoolExeceptionHandler,Regular_Exception_Handler
from concurrent.futures import ThreadPoolExecutor
from typing import Any,List,Tuple,Union,Callable,AnyStr
from assets.text_style import Text_Style
from assets.text_file import Text_File
from netmiko import ConnectHandler
import threading
import logging
import csv
import os

class Common_Function:
    def __init__(self):
        self.netmiko_sessions = None
        self.customlocker = threading.RLock()
        self.logging = self.custom_logger()
    
    @Regular_Exception_Handler
    def clear_screen(self):
        '''Method to clear the screen.'''
        os.system("cls" if os.name == "nt" else "clear")
    
    def custom_logger(self,logger_level=logging.INFO)->object:
        '''
        Method to create the custom logger and capture the logs in app.log file.
        '''
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
    
    @Regular_Exception_Handler
    def device_details_generator(self,device_details_file:str)->List:
        '''
        Method to read data from the csv and generate the device details.
        '''
        my_filter_device_list = []
        with open(device_details_file,mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                filter_row = {key:value for key,value in row.items() if value}          ##Used to filter the valid  value from the csv
                my_filter_device_list.append(filter_row)
            
        return my_filter_device_list

    def __remove_session(self,host:AnyStr)->None:
        '''
        Method to remove the session which is not in Priviledge Exec Mode
        '''
        self.netmiko_sessions = [session for session in self.netmiko_sessions if session.host == host]
        self.logging.info(f"Remove session which is not able to switch in Priviledge Exec Mode")
    
    @NetmikoException_Handler
    def __find_and_handle_prompt(self, session: object) -> None:
        '''
        Find Each and every device prompt and handle it.
        '''
        prompt_output = session.find_prompt()
        with self.customlocker:
            if prompt_output.endswith('>'):
                Text_Style.common_text(primary_text=f"{session.host}", secondary_text=Text_File.common_text['user_exec_mode'])
                try:
                    secret_key = session.secret
                    if secret_key:
                        session.enable()
                        prompt_output = session.find_prompt()  # Update prompt after trying to enable
                    else:
                        self.logging.error(f"{Text_File.error_text['no_secret_key']} {session.host}")
                        Text_Style.common_text(primary_text=f"{session.host}", secondary_text=Text_File.exception_text['noSecretKey'])
                        self.__remove_session(host=session.host)                ##Remove the session from the list
                        return (session.host, False)
                except ValueError as e:
                    self.logging.error(f"{Text_File.exception_text['failed_enable_mode']} {session.host}: {e}")
                    self.__remove_session(host=session.host)                ##Remove the session from the list
                    return (session.host, False)  # Explicitly return False on failure
                

            current_prompt = session.find_prompt()
            print(f"{session.host} with prompt {current_prompt}")
            if current_prompt.endswith('#'):
                Text_Style.common_text(primary_text=f"{session.host}", secondary_text=Text_File.common_text['Privileged_mode'])
                return (session.host, True)

        return (session.host, False)  # Return False if neither condition is met.



    @ThreadPoolExeceptionHandler
    def multi_device_prompt_manager(self)->List:
        '''
        Method to handle the prompt.
        '''
        device_prompts = self.threaded_device_connection_executor(iterable_items=self.netmiko_sessions,function_name=self.__find_and_handle_prompt)
        filter_devices = list(filter(lambda x: x[1],device_prompts))            ##This filter method will filter all the not enable devices.
        return filter_devices

    @NetmikoException_Handler
    def initiate_netmiko_session(self,device_details)->object:
        '''
        Method to make the netmiko session using ConnectHandler Method
        '''
        Text_Style.common_text(primary_text=Text_File.common_text['host_connecting'],secondary_text=device_details['ip'])
        print(f"This is the details which is used to connect the device {device_details}")          ##Just for the debug purpose
        session = ConnectHandler(**device_details)
        if session:
            Text_Style.common_text(primary_text=Text_File.common_text['connected_host'],secondary_text=session.host,secondary_text_color="green")
            return session
        else:
            return False
    
    @ThreadPoolExeceptionHandler
    def threaded_device_connection_executor(self,iterable_items:List,function_name=Callable[['str'],Any])->List:
        '''
        Thread Pool Executor to crate the multiple thred and connect with the device
        '''
        with ThreadPoolExecutor(max_workers=10) as executor:
            connections = executor.map(function_name,iterable_items)
            valid_connection = list(filter(lambda x: x != False and x != None,connections))      ##Filtering the valid connection only
            self.netmiko_sessions = valid_connection                ##Updating the netmiko session instance attributes
            return self.netmiko_sessions
    
