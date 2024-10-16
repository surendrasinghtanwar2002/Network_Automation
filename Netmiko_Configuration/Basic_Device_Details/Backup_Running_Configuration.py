from netmiko import ConnectHandler
from utils.Common_Methods import connection_establishement,send_command,send_config_command

## Device Details
device_details = {
	"device_type":"cisco_ios",
	"host":"192.168.1.100",
	"username":"admin",
	"password":"hackerzone"
}

def main():
	print("Calling the main function here")
	netmiko_session = connection_establishement(device_details)
	output = send_command(netmiko_session,"show run")

	## Write the output from the send command
	with open("Backup",'w') as file:
		file.write(output)
		print("Your file have been created")

if __name__ == "__main__":
	main()