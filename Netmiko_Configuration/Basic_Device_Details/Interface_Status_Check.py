from utils.Common_Methods import connection_establishement,send_command,send_config_command

##device_details
device_Details = {
	"device_type":"cisco_ios",
	"host":"192.168.1.60",
	"username":"admin",
	"password":"hackerzone"
}

def main():
	## Main function here
	netmiko_session = connection_establishement(device_Details)
	command_output = send_command(netmiko_session,"show interface status")
	print(f"Output of the command ------------> {command_output} <----------")


if __name__ == "__main__":
	main()