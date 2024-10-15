from utils.Common_Methods import connection_establishement,send_command,send_config_command

##device details
device_details = {
	"device_type": "cisco_ios",
	"host": "192.168.1.60",
	"username": "admin",
	"password": "hackerzone"
}

##Commands
commands = ["vlan 40",
"name Netmiko_Vlan",
"exit",
"vlan 50",
"name Netmiko_vlan 2",
"exit"
]

def main():
	netmiko_session = connection_establishement(device_details)
	command_output = send_config_command(netmiko_session,commands)
	print(f"This is your output ----------------->\n {command_output}\n <---------------")

if __name__ == "__main__":
	main()
