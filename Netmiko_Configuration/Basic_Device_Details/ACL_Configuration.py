from utils.Common_Methods import connection_establishement,send_command,send_config_command

##device_details
device_Details = {
	"device_type":"cisco_ios",
	"host":"192.168.1.110",
	"username":"admin",
	"password":"hackerzone"
}
##Commands list
commands = [
"access-list 100 deny ip 10.0.0.2 0.0.0.0 192.168.0.1 0.0.0.0",
"access-list 100 permit ip any any",
"interface Ethernet0/2",
"no shut",
"description activated by netmiko script",
"ip access-group 100 in",
"exit",
"do write"
]

def main():
	netmiko_session = connection_establishement(device_Details)
	command_output = send_config_command(netmiko_session,commands)

	print(f"This is the output of the command ------> \n{command_output}\n <--------")

if __name__ == "__main__":
	main()