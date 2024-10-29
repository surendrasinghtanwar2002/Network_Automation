from components.exception_handler import NetmikoException_Handler,Regular_Exception_Handler
from components.common_function import Common_Function
from assets.text_file import Text_File
from components.get_network_menu_items import vlan_menu_items
from assets.text_style import Text_Style
from tabulate import tabulate
from typing import List
from sys import exit
from time import sleep
import csv
import os

class Routing_Configuration(Common_Function):
    def __init__(self):
        
        super().__init__()  # Correctly calling the parent class constructor
        self.vlan_menu_items = vlan_menu_items
        self.main_menu_event_handler = {                          ##This will manage the event handler
            "1": self.display_vlan_information,
            "2": self.Modify_Vlan_Configuration,
            "3": self.vlan_health_status,         
        }

    @NetmikoException_Handler
    def vlan_modification(self,netmiko_session:object,device_config_data:List):
        '''This method will pass the template with configuration command and execute task one by one.
        '''
        template = self.jinja_environment_specifier(template_name='vlan_config_template.txt')                  ##This method will create the jinja enviroment and load the template for the configuration.
        configuration_command = template.module.vlan_configuration(device_details=device_config_data)
        command_output = netmiko_session.send_config_set(configuration_command)
        print(f"This is the output of the command output ------------> {command_output} <---------")
        command_output += netmiko_session.save_config()     ##This will save the configuration
        self.device_config_output(config_output=command_output,host_details=netmiko_session.host)   ##This will store the config output
        

    @NetmikoException_Handler
    def device_configuration(self,session:object,device_config_data:List):
        '''
        Method which will configure the device with the specific configuration given in csv file
        '''

        backup_result = self.backup_device(netmiko_session=session)     ##backup the device before commiting any changes
        if backup_result():
            self.logging.info(f"Backup of the device {session.host} is Succesfull")
        else:
            self.logging.error(f"Backup of the host {session.host} is Unsuccesfull")

        for device_config in device_config_data:
           if device_config['device_ip'] in session.host:
              print(f"Yes device_config has some changes for the host {session.host}")
              
              device_vlan_info = session.send_command("show vlan",use_textfsm=True)        ##Command sending to the device
              
            #  "This method have given the current vlan information of the device"
              current_vlan_id = [vlan['vlan_id'] for vlan in device_vlan_info]

             ##This will check the configuration vlan details with the existing device and filter those vlan which are already presented
              if device_config['create_vlan']:                  
                  device_config['create_vlan']=list(filter(lambda x: x not in current_vlan_id,device_config['create_vlan']))
            
            ##This will check the configuration vlan details with the existing device and filter those vlan which are not presneted
              if device_config['delete_vlan']:
                  device_config['delete_vlan'] = list(filter(lambda x: x in current_vlan_id,device_config['create_vlan']))

              self.vlan_modification(netmiko_session=session,device_config_data=device_config)      ##Calling the vlan modification method and passing filtered device data.
           else:
              print(f"No there is no config for the host {session.host}")    

    def Modify_Vlan_Configuration(self):
        '''
        Method to modify the vlan configuration
        '''
        device_config_data = self.read_device_configuration()           ##Method will extract all information from the csv
        print(f"This is the device configuration data --------------> \n{device_config_data} <--------------")          ## this data is list
        # 

        ##This method will call the thread and call the validate_vlan_changes before implementing anything on the device
        configuration_details  = self.threaded_device_connection_executor(iterable_items=self.netmiko_sessions,function_name=self.device_configuration)
        print(f"This will give the output of the configuration details of the function------------> {configuration_details} <-------------")
    
    
    def vlan_health_status(self):
        print("In this we will check the vlan health and status")
    
    def default_function(self):         ##let see this function will be used in our script or not
        self.logging.error(f"{Text_File.error_text['limit_exceed']}in Class {__name__}") 
        exit(Text_Style.ExceptionTextFormatter(primary_text=Text_File.error_text['limit_exceed']))      ##If user have reached the limit script will be closed.

    def display_vlan_information(self, session: object, command="show vlan"):
        '''
        Method to display_vlan_information.
        '''
        print(f"This is the data received in the display vlan information -----> {session} <-----------")
        # Displaying command execution attempt
        Text_Style.common_text(primary_text=Text_File.common_text['command_execution_try'], secondary_text= [item.host for item in session] if isinstance(session, list) else [session.host])
        
        # Sending command to the session
        output = [netmikosession.send_command(command,use_textfsm=True) for netmikosession in session] if isinstance(session,list) else session.send_command(command,use_textfsm=True)

        # Validating the command output
        command_validation_output = self.run_command_validation(session=session, command_output=output, command=command)
        
        print(f"This the output of the command validation output ------> {command_validation_output} <-------------")
        # if command_validation_output:
        #     # Prepare table headers and data
        #     vlan_header = ['Vlan_Id', 'Vlan_Name', 'Status', 'Interfaces']
        #     vlan_data = [ ]  # This list will hold VLAN data details    
        #     if isinstance(command_validation_output, list):
        #         for vlan in command_validation_output:
        #             vlan_data.append([
        #                 vlan['vlan_id'],
        #                 vlan['vlan_name'],
        #                 vlan['status'],
        #                 vlan['interfaces']
        #             ])
        #         Text_Style.common_text(primary_text=Text_File.common_text['device_output'],secondary_text={session.host})
        #         Text_Style.common_text(primary_text=tabulate(vlan_data, headers=vlan_header, tablefmt='grid'))
        #     else:
        #         Text_Style.common_text(primary_text=command_validation_output)  # If not a list, print the returned validation output directly
        # else:
        #     Text_Style.ExceptionTextFormatter(primary_text=Text_File.error_text['command_failed'])
    
    @Regular_Exception_Handler
    def read_device_configuration(self):
        '''
        This method will load the vlan_configuration details from the csv file.
        '''
        devices = []                ##Contain the device configuration details
        file_path = self.file_path_specifier(file_path="components/common_function.py")         ##file Path Specifier
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                filter_row = {key: value for key, value in row.items() if value}

                if 'create_vlan' in filter_row:
                    row['create_vlan'] = [int(vlan.strip()) for vlan in filter_row['create_vlan'].split(',') if vlan.strip().isdigit()]
                else:
                    row['create_vlan'] = []

                if 'delete_vlan' in filter_row:
                    row['delete_vlan'] = [int(vlan.strip()) for vlan in filter_row['delete_vlan'].split(',') if vlan.strip().isdigit()]
                else:
                    row['delete_vlan'] = []

                devices.append(row)

        return devices
    
    @Regular_Exception_Handler
    def connection_to_devices(self) -> None:
        '''
        Method to connect to devices and manage device prompts.
        '''
        valid_device_details = self.device_details_generator(device_details_file="device_details.csv")     
       
        netmiko_connection_list = self.threaded_device_connection_executor(
            iterable_items=valid_device_details,
            function_name=self.initiate_netmiko_session
        )
        self.valid_device_filteration(netmiko_connection_list)  # Update with valid sessions only
        
        output = self.multi_device_prompt_manager()
        self.logging.info(f"{Text_File.common_text['valid_devices']}{output}")
        print(f"Wait Extracting data from the given file......")
        sleep(2)            ## 2 second delay 
        self.clear_screen()  # Clear the screen
        self.display_device_info(valid_device_details)
        print(f"\n")
        Text_Style.common_text(primary_text=Text_File.common_text["valid_privileged_device"], primary_text_color="hot_pink3")
        header = ["Host", "Privileged EXEC Mode Status"]        
        Text_Style.common_text(primary_text=tabulate(output, header, tablefmt='grid'),primary_text_color="hot_pink3")        ##print the valid host which are in priviledged exec mode.    
        self.display_menu(menu_items=self.vlan_menu_items)
        self.check_user_choice(event_handler=self.main_menu_event_handler,default_handler=self.default_function)         ##Checking user choice from the list.

if __name__ == "__main__":
    r1 = Routing_Configuration()
    r1.connection_to_devices()
