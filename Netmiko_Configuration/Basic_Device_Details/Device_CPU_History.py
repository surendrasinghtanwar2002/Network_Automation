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
configuration_command = ["terminal length 0","show processes cpu history"]


##Main function
def main():
	netmiko_session = connection_establishement(device_Details)
	command_output = send_command(netmiko_session,configuration_command)
	print(f"This is the output -------> \n{command_output}\n <---------")

##Calling the main function
if __name__ == "__main__":
	main()