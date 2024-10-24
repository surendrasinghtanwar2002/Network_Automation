from components.common_function import Common_Function
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler

class Routing_Configuration:
    def __init__(self):
        self.device_details = Common_Function.device_details_generator('device_details.csv')        ##Contain the device details

    def show_Device_Details(self):
        print(self.device_details)
        print(f"Callign the thread pool executor function here")
        self.thread_pool_executor()

    def __connectiontonetmiko_device(self,device_details):
        print(f"Trying to Connect with the device {device_details['host']}")
        session = ConnectHandler(**device_details)
        if session:
            print(f"Connected to the deivce succesfully {device_details.host}")

    def thread_pool_executor(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            connections = executor.map(self.__connectiontonetmiko_device,self.device_details)
            valid_connection = list(filter(lambda x: x != False and x != None,connections))      ##Filtering the valid connection only
            print(f"This is the valid connection details {valid_connection}")



if __name__ == "__main__":
    r1 = Routing_Configuration()
    r1.show_Device_Details()