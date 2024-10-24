from components.common_function import Common_Function
from components.common_function import Common_Function
import threading
import os

class Routing_Configuration(Common_Function):
    def __init__(self):
        self.logger = self.custom_logger()      ##Custom logger
        self.session_list = None
        self.locker = threading.RLock()            

    def __promot_validator(self,session)->None:
        output = session.find_prompt()
        with self.locker:
           print(f"Finding the prompt of the device {session.host} and prompt is {output}")
        if output.endswith('#'):
               print(f"Your are in priviledged mode {session.host}")
        elif output.endswith('>'):
               print(f"Your are in user execution mode {session.host}")
               print(f"We need to perform the another task")
               output = session.enable()
               print(f"this is the output of the enable prompt = {output}")
               output = session.find_prompt()
               print(f"This is the current prompt of the device {output}")
        else:
                print(f"You are not connected to the valid host")
        return True

    def prompt_validator_handler(self)->None:
        result = self.threaded_device_connection_executor(iterable_items=self.session_list,function_name=self.__promot_validator)
        print(result)
        
    def connection_to_devices(self)->None:
        self.clear_screen()
        device_details = self.device_details_generator(device_details_file="device_details.csv")
        netmiko_conenction_list = self.threaded_device_connection_executor(iterable_items=device_details,function_name=self.initiate_netmiko_session)
        self.session_list = netmiko_conenction_list
        print(self.session_list)
        self.prompt_validator_handler()


if __name__ == "__main__":
    r1 = Routing_Configuration()
    r1.connection_to_devices()