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
configuration_command = ["ntp server 192.168.1.1"]

##Main function
def main():
 	netmiko_session = connection_establishement(device_Details)
 	command_output = send_config_command(netmiko_session,configuration_command)
 	print(f"This is the output of the config command ----> \n{command_output}\n <-------")

if __name__ == "__main__":
 	main()