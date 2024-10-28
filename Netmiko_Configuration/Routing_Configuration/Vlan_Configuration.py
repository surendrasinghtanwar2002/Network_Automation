from components.common_function import Common_Function
from components.exception_handler import NetmikoException_Handler,ThreadPoolExeceptionHandler,Regular_Exception_Handler
from assets.text_file import Text_File
from components.get_network_menu_items import vlan_menu_items
from assets.text_style import Text_Style
from tabulate import tabulate
from typing import List
from sys import exit
import csv

class Routing_Configuration(Common_Function):
    def __init__(self):
        super().__init__()  # Correctly calling the parent class constructor
        self.vlan_menu_items = vlan_menu_items
        self.event_handler = {                          ##This will manage the event handler
            "1": self.display_vlan_information,
            "2": self.Modify_Vlan_Configuration,
            "3": self.vlan_health_status,         
        }

    def Modify_Vlan_Configuration(self):
        print("In this function we will create the vlan and delete the vlan")
    
    def vlan_health_status(self):
        print("In this we will check the vlan health and status")
    
    def default_function(self):         ##let see this function will be used in our script or not
        self.logging.error(f"{Text_File.error_text['limit_exceed']}in Class {__name__}") 
        exit(Text_Style.ExceptionTextFormatter(primary_text=Text_File.error_text['limit_exceed']))      ##If user have reached the limit script will be closed.

    @NetmikoException_Handler
    def display_vlan_information(self, session: object, command="show vlan"):
        '''
        Method to display_vlan_information.
        '''
        # Displaying command execution attempt
        Text_Style.common_text(primary_text=Text_File.common_text['command_execution_try'], secondary_text=session.host)
        
        # Sending command to the session
        output = session.send_command(command,use_textfsm=True)
           
        # Validating the command output
        command_validation_output = self.run_command_validation(session=session, command_output=output, command=command)
        
        if command_validation_output:
            # Prepare table headers and data
            vlan_header = ['Vlan_Id', 'Vlan_Name', 'Status', 'Interfaces']
            vlan_data = [ ]  # This list will hold VLAN data details    
            if isinstance(command_validation_output, list):
                for vlan in command_validation_output:
                    vlan_data.append([
                        vlan['vlan_id'],
                        vlan['vlan_name'],
                        vlan['status'],
                        vlan['interfaces']
                    ])
                Text_Style.common_text(primary_text=Text_File.common_text['device_output'],secondary_text={session.host})
                Text_Style.common_text(primary_text=tabulate(vlan_data, headers=vlan_header, tablefmt='grid'))
            else:
                Text_Style.common_text(primary_text=command_validation_output)  # If not a list, print the returned validation output directly
        else:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.error_text['command_failed'])
    
    def read_device_configuration(self):
        '''
        '''
        devices = []                ##Contain the device configuration details
        print("Load the vlan configuration details from the csv file")
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
        self.display_device_info(valid_device_details)
       
        netmiko_connection_list = self.threaded_device_connection_executor(
            iterable_items=valid_device_details,
            function_name=self.initiate_netmiko_session
        )
        self.valid_device_filteration(netmiko_connection_list)  # Update with valid sessions only
        
        output = self.multi_device_prompt_manager()
        self.logging.info(f"{Text_File.common_text['valid_devices']}{output}")
        
        self.clear_screen()  # Clear the screen
        header = ["Host", "Privileged EXEC Mode Status"]        
        Text_Style.common_text(primary_text=tabulate(output, header, tablefmt='grid'),primary_text_color="red")        ##print the valid host which are in priviledged exec mode.    
        self.display_menu(menu_items=self.vlan_menu_items)
        self.check_user_choice(event_handler=self.event_handler,default_function=self.default_function)         ##Checking user choice from the list.

        # self.threaded_device_connection_executor(
        #     iterable_items=self.netmiko_sessions,                 ## we will use after some use case
        #     function_name=self.send_command
        # )
    

if __name__ == "__main__":
    r1 = Routing_Configuration()
    r1.connection_to_devices()
