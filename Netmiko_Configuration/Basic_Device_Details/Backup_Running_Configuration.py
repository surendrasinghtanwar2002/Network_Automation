from netmiko import ConnectHandler
from utils.Exception_Handler import Netmiko_Exception_Handler,Regular_Exception_Handler
from utils.Common_Methods import connection_establishement,send_command
import sys

##Device Details for the connection
device_details = {
	'username' :"admin",
	'password' : "hackerzone",
	'host' : "192.168.1.100",
	'device_type' : "cisco_ios"
}
##Main Function
def main():
	netmiko_session = connection_establishement(**device_details)
	command_output = send_command(netmiko_session,"show run")
	print(f"---------------------> {command_output} <------------------------")

##Calling the main function
if __name__ == "__main__":
	main()

