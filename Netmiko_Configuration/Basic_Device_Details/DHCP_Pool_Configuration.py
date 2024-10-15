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

##Configuration commands
configuration_command = [
"ip dhcp pool DHCP",
"network 192.168.50.0 255.255.255.0",
"default-router 192.168.50.1",
"exit",
"ip dhcp excluded-address 192.168.50.2 192.168.50.40",
"do write"
]

##main function
def main():
	print("Main function")
	netmiko_session = connection_establishement(device_Details)
	command_output = send_config_command(netmiko_session,configuration_command)
	print(f"Ouput of the command -----> \n{command_output}\n <------")

##Calling the main function
if __name__ == "__main__":
	main()	