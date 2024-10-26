from components.common_function import Common_Function
from components.exception_handler import NetmikoException_Handler,ThreadPoolExeceptionHandler,Regular_Exception_Handler
from assets.text_file import Text_File
from assets.text_style import Text_Style
from tabulate import tabulate
from typing import List

class Routing_Configuration(Common_Function):
    def __init__(self):
        super().__init__()  # Correctly calling the parent class constructor
    
    def funct(self):
        print("WE WILL CREATE THE FUNCTION HERE")

    def valid_device_filteration(self, device_session_list: List) -> None:
        '''
        Method to filter the valid devices from the list.
        '''
        valid_connection = list(filter(lambda x: x is not False, device_session_list))  # Filtering valid connections only
        self.netmiko_sessions = valid_connection

    @NetmikoException_Handler
    def send_command(self, session: object, command="show vlan"):
        '''
        Method to send a command to the device session.
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
                print(f"Output of the device {session.host}")
                Text_Style.common_text(primary_text=tabulate(vlan_data, headers=vlan_header, tablefmt='grid'))
            else:
                print(command_validation_output)  # If not a list, print the returned validation output directly
        else:
            print("Command execution failed or returned invalid output.")

    @Regular_Exception_Handler
    def connection_to_devices(self) -> None:
        '''
        Method to connect to devices and manage device prompts.
        '''
        valid_device_details = self.device_details_generator(device_details_file="device_details.csv")     
        self.clear_screen()  # Clear the screen
        self.display_device_info(valid_device_details)
       
        netmiko_connection_list = self.threaded_device_connection_executor(
            iterable_items=valid_device_details,
            function_name=self.initiate_netmiko_session
        )
        self.valid_device_filteration(netmiko_connection_list)  # Update with valid sessions only
        
        output = self.multi_device_prompt_manager()
        self.logging.info(f"{Text_File.common_text['valid_devices']}{output}")
        
        header = ["Host", "Privileged EXEC Mode Status"]
        print(tabulate(output, header, tablefmt='grid'))
        
        self.threaded_device_connection_executor(
            iterable_items=self.netmiko_sessions,
            function_name=self.send_command
        )
    

if __name__ == "__main__":
    r1 = Routing_Configuration()
    r1.connection_to_devices()
