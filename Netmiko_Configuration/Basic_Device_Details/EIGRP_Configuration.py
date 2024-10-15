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

configuration_command = [
"router eigrp 100",
"no auto-summary",
"network 0.0.0.0 255.255.255.255",
"exit",
"do write"
]

def main():
	## Main function here
	netmiko_session = connection_establishement(device_Details)
	command_output = send_config_command(netmiko_session,configuration_command)
	print(f"Output of the command ------------> {command_output} <----------")

if __name__ == "__main__":
	main()