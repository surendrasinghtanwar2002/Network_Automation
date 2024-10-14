from netmiko import ConnectHandler
from utils.Exception_Handler import Netmiko_Exception_Handler
import sys

##Device Details for the connection
device_details = {
	'username' :"admin",
	'password' : "hackerzone",
	'host' : "192.168.1.100",
	'device_type' : "cisco_ios"
}
## Function for making the connection

##Send Command Function
@Netmiko_Exception_Handler
def send_command(session:object)->str:
	try:
		outcome = session.send_command("show run")
		return outcome
	except Exception as error:
		print(f"This is the exception of the send_command Function {error}")

##Main Function
def main():
	result = connection(details=device_details)
	print(f"----------------------> Netmiko Object {result} <------------------")
	if result:
		command_output = send_command(session=result)
		print("Command executed succesfuly")
		print(f"----------------> {command_output} <-----------")
	else:
		print("Command not executed succesfuly")
		sys.exit("Clossing the script")

##Calling the main function
if __name__ == "__main__":
	main()

