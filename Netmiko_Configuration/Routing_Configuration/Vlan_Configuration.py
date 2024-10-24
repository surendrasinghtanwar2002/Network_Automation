from components.common_function import Common_Function
from components.common_function import Common_Function
import os

class Routing_Configuration(Common_Function):
    def __init__(self):
        loggerh = os.path.join(os.getcwd(),"app.log")
        self.logger = Common_Function.custom_logger(logger_name="Netmiko_Logger",logger_file_path=loggerh)      ##Custom logger used in the function
        self.device_details = None

    def connection_to_devices(self):
        print("In this we will connect to the multiple devices")
        device_details = self.device_details_generator(device_details_file="device_details.csv")
        self.device_details= device_details
        print(f"This is the device details of the ------> {self.device_details}")
        netmiko_conenction_list = self.thread_pool_executor(iterable_items=self.device_details,function_name=self.connectiontonetmiko_device)
        if netmiko_conenction_list:
            self.logger.info("Function executed succesfully")
            print(f"This is the netmiko connection list {netmiko_conenction_list}")
            for connection in netmiko_conenction_list:
                output = connection.send_command('show run')        
                print(f"Command Executed on the host {connection.host} and output is:- \n{output}")
        else:
            self.logger.info("No thing performed herer")



if __name__ == "__main__":
    r1 = Routing_Configuration()
    r1.connection_to_devices()