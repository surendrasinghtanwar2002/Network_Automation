from utils.Common_Methods import connection_establishement,send_command,send_config_command
##device_details
device_Details = [{
	"device_type":"cisco_ios",
	"host":"192.168.1.110",
	"username":"admin",
	"password":"hackerzone"
},
{
	"device_type":"cisco_ios",
	"host":"192.168.1.100",
	"username":"admin",
	"password":"hackerzone"
},
{
	"device_type":"cisco_ios",
	"host":"192.168.1.105",
	"username":"admin",
	"password":"hackerzone"
}
]

##Configuration commands for the loopback interface
configuration_commands = [
"interface Loopback 0",
"ip address 192.168.100.1 255.255.255.255",
"exit",
"do write",
"do show ip interface brief"
]

##main function
def main():
	try:
		netmiko_session = connection_establishement(device_Details)
		command_output = send_config_command(netmiko_session,configuration_commands)
		print(f"This is the command_output ---->\n{command_output}\n <------ ")
	except Exception as e:
		print(f"This is the Exception of the function {e}")

##Calling the main function
if __name__ == "__main__":
	main()