from utils.Common_Methods import connection_establishement,send_command,send_config_command

device_details = {
	"device_type": "cisco_ios",
	"host": "192.168.1.60",
	"username": "admin",
	"password": "hackerzone"
}
commands = [
"interface Ethernet0/1",
"ip address 192.168.50.1 255.255.255.0",
"no shut",
"description activated by netmiko script",
"exit",
"do write"
]
##Main Function
def main():
	netmiko_session = connection_establishement(device_details)
	command_output = send_config_command(netmiko_session,commands)
	print(f"---------------------> {command_output} <------------------------")

##Calling the main function
if __name__ == "__main__":
	main()