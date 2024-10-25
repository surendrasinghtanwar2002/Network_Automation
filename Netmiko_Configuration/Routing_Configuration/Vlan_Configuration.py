from components.common_function import Common_Function
from components.common_function import Common_Function
import threading
from tabulate import tabulate
import os

class Routing_Configuration(Common_Function):
    def __init__(self):
        super().__init__()  # Correctly calling the parent class constructor      
     
    def funct():
        print("WE WILL CREATE THE FUNCTION HERE")

    def connection_to_devices(self)->None:
        self.clear_screen()
        device_details = self.device_details_generator(device_details_file="device_details.csv")
        netmiko_conenction_list = self.threaded_device_connection_executor(iterable_items=device_details,function_name=self.initiate_netmiko_session)

        print(f"This value is coming from the self.netmiko connection this is instance attributes Position 11 -------->\n {self.netmiko_sessions} <------------")

        output = self.multi_device_prompt_manager()
        print(f"This is the current netmiko session object after performing everything  Position 22 {self.netmiko_sessions}")
        self.logging.info(f"Valid device details{output}")
        print(f"This is the current netmiko session object after performing everything  Position 33 {self.netmiko_sessions}")
        header = ["Host","Privileged EXEC mode Status"]
        print(tabulate(output,header,tablefmt='grid'))

        
       


if __name__ == "__main__":
    r1 = Routing_Configuration()
    r1.connection_to_devices()