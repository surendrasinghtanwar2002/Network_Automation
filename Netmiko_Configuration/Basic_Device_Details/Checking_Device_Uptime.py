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

def main():
	netmiko_session = connection_establishement(device_Details)
	output = send_command(netmiko_session,"show version | include uptime")
	print(f"Device is active from the \n{output}")

if __name__ == "__main__":
	main()
