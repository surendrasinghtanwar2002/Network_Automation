from components.exception_handler import NetmikoException_Handler,ThreadPoolExeceptionHandler,Regular_Exception_Handler
from typing import Any,List,Tuple,Union,Callable,AnyStr,Dict
from concurrent.futures import ThreadPoolExecutor
from jinja2 import Environment,FileSystemLoader
from assets.text_style import Text_Style
from assets.text_file import Text_File
from netmiko import ConnectHandler,NetmikoTimeoutException,NetmikoBaseException,NetmikoAuthenticationException,ConnectionException
from tabulate import tabulate
from datetime import datetime
import subprocess
import threading
import platform 
import logging
import csv
import os
import re

class Common_Function:
    def __init__(self):
        self.netmiko_sessions = None   ##This will be super method manage the state globally.
        self.customlocker = threading.RLock()
        self.logging = self.custom_logger()
    
    @Regular_Exception_Handler
    def clear_screen(self):
        '''Method to clear the screen.'''
        os.system("cls" if os.name == "nt" else "clear")
    
    @staticmethod
    def custom_logger(logger_level=logging.INFO)->object:
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
    def device_details_generator(self, device_details_file: str) -> List:
        my_filter_device_list = []

        with open(device_details_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                filter_row = {key: value for key, value in row.items() if value}
                my_filter_device_list.append(filter_row)

        devices = [device['ip'] for device in my_filter_device_list]
        filtered_devices = self.ping_to_device(device_ip=devices)

        filter_devices = [
            item for item in my_filter_device_list
            if item['ip'] in filtered_devices
        ]

        return filter_devices
    
    @Regular_Exception_Handler
    def display_device_info(self,device_details:List[Dict[str, str]])->None:
        '''
        Method to display device info in the tabular format.
        '''
        Text_Style.common_text(primary_text=Text_File.common_text["valid_device_details"], primary_text_color="green")
        device_header = ["Device_IP", "Device_Type", "Username", "Password", "Secret", "Port"]
        devices_list = []  # Contain the device details
        
        for device in device_details:
            devices_list.append([
                device['ip'],
                device['device_type'],
                device['username'],
                device['password'],
                device['secret'] if device['secret'] else None,
                device.get('port', None)  # Using .get() for safety
            ])
        
        print(tabulate(devices_list, headers=device_header, tablefmt='grid'))

    @NetmikoException_Handler
    def backup_device(self, netmiko_session: object):
        '''
        Method to backup the device before implementing any configuration to the device.
        '''
        current_absolute_path = os.path.dirname(os.path.abspath(__file__))
        device_backup_path = os.path.join(current_absolute_path, 'device_backup')
        
        os.makedirs(device_backup_path, exist_ok=True)      ##Check either folder exist or not
        
        # Format the filename with the host and current date/time
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{netmiko_session.host}_{current_datetime}.txt"
        file_path = os.path.join(device_backup_path, file_name)
        
        # Retrieve the device configuration
        device_running_configuration = netmiko_session.send_command("show run")
        
        # Write the configuration to the file in the backup directory
        with open(file_path, 'w') as file:
            file.write(f"Backup of the device: {netmiko_session.host}\n")
            file.write(f"{device_running_configuration}\n")
        
        # Check if the backup file exists at the specified path
        if os.path.exists(file_path):
            print(f"Backup was successful! File saved at {file_path}")
            return True
        else:
            print(f"Backup failed. File was not created at {file_path}")
            return True

    @Regular_Exception_Handler
    def __remove_session(self,host:AnyStr)->None:
        '''
        Method to remove the session which is not in Priviledge Exec Mode
        '''
        self.netmiko_sessions = [session for session in self.netmiko_sessions if session.host != host]
        self.logging.info(f"{Text_File.error_text['removing_invalid_session']} {host}")
    
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

    @Regular_Exception_Handler
    def ping_to_device(self, device_ip: Union[AnyStr, List]) -> Union[List, bool]:
        '''
        Function to ping the device(s) and validate if reachable.
        '''
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        valid_ip = []  # List to store reachable IPs
        
        if isinstance(device_ip, list):
            for device in device_ip:
                command = ['ping', param, '1', device]                
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if "Destination host unreachable" in result.stdout:
                    self.logging.error(f"Device is unreachable {device}")             ##error log
                elif result.returncode == 0:
                    valid_ip.append(device)
                else:
                    self.logging.error(f"Ping to {device} failed with return code {result.returncode}.")  ##error log

            return valid_ip  # Returns the list of reachable IPs        
        
        elif isinstance(device_ip, str):
            command = ['ping', param, '1', device_ip]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)           
            
            if "Destination host unreachable" in result.stdout:
                self.logging.error(f"Device is unreachable {device}")             ##error log
                return False 
            elif result.returncode == 0:
                return True  # Reachable
            else:
                self.logging.error(f"Ping to {device} failed with return code {result.returncode}.")  ##error log
                return False
        
        else:
            print("No valid IP(s) provided.") 
            return False

    @NetmikoException_Handler
    def run_command_validation(self, session: object, command_output: Union[AnyStr, List], command: AnyStr):
        '''
        Validate the command output to determine if the command is valid for the device.
        '''
        with self.customlocker: 
            if isinstance(command_output, list):            ##If the output is list
                return command_output
            
            elif isinstance(command_output, str):
                custom_pattern = r'^% .+:\s+"[^"]+"'  # Pattern to match invalid command output
                device_output = re.search(custom_pattern, command_output)
                
                if device_output:       ##If pattern Match 
                    self.logging.error(f"The command '{command}' is not valid on device '{session.host}'. Please check the command.") 
                    return False
                else:                   ## If pattern doesn;t Match
                    return f"The output of the command {command} host {session.host} is:\n{command_output}"
                                                                                                                              
    @ThreadPoolExeceptionHandler
    def multi_device_prompt_manager(self)->List:
        '''
        Method to handle the prompt.
        '''
        device_prompts = self.threaded_device_connection_executor(iterable_items=self.netmiko_sessions,function_name=self.__find_and_handle_prompt)
        filter_devices = list(filter(lambda x: x[1],device_prompts))            ##This filter method will filter all the not enable devices.
        return filter_devices
    
    @Regular_Exception_Handler
    def valid_device_filteration(self, device_session_list: List) -> None:
        '''
        Method to filter the valid devices from the list.
        '''
        valid_connection = list(filter(lambda x: x is not False, device_session_list))  # Filtering valid connections only
        self.netmiko_sessions = valid_connection       
    
    @Regular_Exception_Handler
    def display_menu(self,menu_items:List) ->None:
        '''
        Method to rener the display menu on the console.
        '''
        for no,items in enumerate(menu_items,start=1):
            Text_Style.common_text(primary_text=str(no),secondary_text=items['menu_name'])
    
    @Regular_Exception_Handler
    def file_path_specifier(self,file_path:str):
        '''
        Method to get the path of the file
        '''
        config_file_path = os.path.abspath(file_path)
        return config_file_path
    
    @Regular_Exception_Handler
    def check_user_choice(self,event_handler:List,default_handler:callable)->None:
        '''
        Method to check the user choice from the event handler
        '''
        c_start = 0
        c_end = 3
        while c_start < c_end:
            user_event_choice = input(Text_Style.common_text(primary_text=Text_File.common_text['user_choice_no'])).strip()
            if user_event_choice in self.event_handler:             ##Validate either user event is presented in the event handler or not
                self.event_handler.get(user_event_choice)()     
            else:
                Text_Style.ExceptionTextFormatter(primary_text=Text_File.error_text['menu_wrong_input'])
                c_start += 1            ##increasing the counter    
        self.default_handler()    

    def jinja_environment_specifier(template_name: str):
        '''
        Method to create the jinja environment and load the jinja template from the folder.
        '''
        current_absolute_path = os.path.dirname(os.path.abspath(__file__))      

        network_config_path = os.path.join(current_absolute_path, 'config_templates')

        env = Environment(loader=FileSystemLoader(network_config_path))

        template = env.get_template(template_name)

        return template         ##return the jinja template
    
    def initiate_netmiko_session(self,device_details)->object:
        '''
        Method to make the netmiko session using ConnectHandler Method
        '''
        Text_Style.common_text(primary_text=Text_File.common_text['host_connecting'],secondary_text=device_details['ip'])

        try:
            session = ConnectHandler(**device_details)
            if session:
                Text_Style.common_text(primary_text=Text_File.common_text['connected_host'],secondary_text=session.host,secondary_text_color="green")
                return session
            else:
                self.logging.error(f'{Text_File.error_text['connection_failed']} on host {device_details['ip']}')
        except NetmikoTimeoutException:
            self.logging.error(f'{Text_File.error_text['connection_failed']} on host {device_details['ip']}')
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Netmiko_Timeout_Exception"],
                secondary_text=__name__
            )
            return False
        except NetmikoBaseException:
            self.logging.error(f'{Text_File.error_text['connection_failed']} on host {device_details['ip']}')
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Netmiko_Base_Exception"],
                secondary_text=__name__
            )
            return False
        except NetmikoAuthenticationException:
            self.logging.error(f'{Text_File.error_text['connection_failed']} on host {device_details['ip']}')
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Netmiko_Authentication_exception"],
                secondary_text=__name__
            )
            return False
        except ConnectionException:
            self.logging.error(f'{Text_File.error_text['connection_failed']} on host {device_details['ip']}')
            Text_Style.common_text(
                primary_text=Text_File.exception_text["ssh_exception"],
                secondary_text=__name__
            )
            return False        
    
    @ThreadPoolExeceptionHandler
    def threaded_device_connection_executor(self,iterable_items:List,function_name=Callable[['str'],Any])->List:
        '''
        Thread Pool Executor to crate the multiple thred and connect with the device
        '''
        with ThreadPoolExecutor(max_workers=10) as executor:
            connections = executor.map(function_name,iterable_items) 
            sessions = list(netmiko_session for netmiko_session in connections)
            return sessions
