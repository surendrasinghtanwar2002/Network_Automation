from components.common_function import Common_Function
from assets.text_file import Text_File
from components.common_function import Common_Function
from tabulate import tabulate
from typing import List,Union,AnyStr


class Routing_Configuration(Common_Function):
    def __init__(self):
        super().__init__()  # Correctly calling the parent class constructor      
     
    def funct():
        print("WE WILL CREATE THE FUNCTION HERE")

    def valid_device_filteration(self,device_session_list: List)->None:
        '''
        Method use to filter the  valid devices from the list
        '''
        valid_connection = list(filter(lambda x: x != False,device_session_list))      ##Filtering the valid connection only
        self.netmiko_sessions = valid_connection


            
    def connection_to_devices(self)->None:
        self.clear_screen()
        device_details = self.device_details_generator(device_details_file="device_details.csv")
        netmiko_conenction_list = self.threaded_device_connection_executor(iterable_items=device_details,function_name=self.initiate_netmiko_session)
        self.valid_device_filteration(netmiko_conenction_list)                      ##Filtering the valid connection and updating the current netmiko session                 
        output = self.multi_device_prompt_manager()
        self.logging.info(f"{Text_File.common_text['valid_devices']}{output}") 
        header = ["Host","Privileged EXEC mode Status"]
        print(tabulate(output,header,tablefmt='grid'))
        self.threaded_device_connection_executor(iterable_items=self.netmiko_sessions,function_name=self.send_command)
       


if __name__ == "__main__":
    r1 = Routing_Configuration()
    r1.connection_to_devices()