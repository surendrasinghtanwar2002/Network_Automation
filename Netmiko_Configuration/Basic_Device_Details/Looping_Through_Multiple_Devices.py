from utils.Common_Methods import connection_establishement,send_command,send_config_command

##Multiple_Device_Configuration
device_details = [
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
},
{
"device_type":"cisco_ios",
"host":"192.168.1.110",
"username":"admin",
"password":"hackerzone"
},
]

commands = ["show ip interface brief"]

def main():
	netmiko_session = connection_establishement(device_details)
	print(f"This is the netmiko_session output {netmiko_session}")
	output = send_command(netmiko_session,commands)
	print(f"Output of the command ------------->\n {output}\n <-------------")
if __name__ == "__main__":
	main()