from netmiko import ConnectHandler,NetMikoAuthenticationException,NetmikoTimeoutException,NetmikoBaseException,redispatch
from time import sleep,time
import datetime

##Jump Host Server Details
jump_host_details = {
	"device_type":"terminal_server",
	"ip":"192.168.1.30",
	"username":"server",
	"use_keys": True,  # Key-based authentication
    "key_file": "/Users/surendrasingh/.ssh/id_ed25519"  # Path to your private key
}

##Remote Server Details
remote_server_Details = [["Main_Building","ios","Router","192.168.1.100"],["Main_Building","iosxr","Switch","192.168.1.105"],["Main_Building","ios","Router","192.168.1.110"],["Data_Center","iosxr","Router","192.168.1.115"]]

def generate_device_details() -> object:
    '''
    Function to generate the device details
    '''
    try:
        network_Device = []
        for device in remote_server_Details:
            if device[1] == "ios":  # Specific for IOS version
                network_Device.append(
                    {
                        'device_type': "cisco_ios",
                        'username': "admin",
                        'password': "hackerzone",
                        'ip': device[3]
                    }
                )
            elif device[1] == "iosxr":
                network_Device.append(
                    {
                        'device_type': "cisco_iosxr",
                        'username': "admin",
                        'password': "hackerzone",
                        'ip': device[3]
                    }
                )
        return network_Device
    except Exception as e:
        print(f"An error occurred in the function {__name__}: {e}")

		

def Device_Remote_Connection(devices,host_session)->object:	
	'''
	Function to make the device remote connection and redispatch the function
	'''
	try:
		for device in devices:
			print(f"Connecting to the host....-> {device['ip']}")
			host_session.write_channel(f"ssh {device['username']}@{device['ip']}\r\n")
			sleep(5)		##5 Second delay for Password Prompt
			channel_output = host_session.read_channel()

			##Checking either prompt contain the permission for the ssh        (Condition 1)
			if '(yes/no)?' in channel_output.lower():
				host_session.write_channel("yes\r\n")
				sleep(4)		##4 Second Delay for password prompt
				password_prompt = host_session.read_channel()
				if "Password:" in password_prompt:
					print("Password prompt Required for the connection")
					host_session.write_channel(f"{device['password']}\r\n")
					sleep(4) 	##4 second delay for the device prompt
					device_prompt = host_session.read_channel()
					if ">" in device_prompt or "#" in device_prompt:
						print("Device prompt found .......")
						redispatch(host_session,device_type=device['device_type'])				##Redispatching device type from the terminal_server to the specific device_type
						start_time = datetime.now()
						command_output = host_session.send_command("show run")
						print(f"Command Excecuted on the host {device['ip']}\n Output:- {command_output}")
						host_session.disconnect()
						end_time = datetime.now()
						print(f"Total time Taken to execute the command on the host {device['ip']} is {end_time-start_time}")
				else:
					print("Password prompt not found........")

			##Checking either prompt contain the password prompt for the ssh		(Condition 2)		
			elif 'Password:' in password_prompt:
				print("Password prompt Required for the connection")
				host_session.write_channel(f"{device['password']}\r\n")
				sleep(4) 	##4 second delay for the device prompt
				device_prompt = host_session.read_channel()
				if ">" in device_prompt or "#" in device_prompt:
					print("Device prompt found .......")
					redispatch(host_session,device_type=device['device_type'])				##Redispatching device type from the terminal_server to the specific device_type
					start_time = datetime.now()
					command_output = host_session.send_command("show run")
					print(f"Command Excecuted on the host {device['ip']}\n Output:- {command_output}")
					host_session.disconnect()
					end_time = datetime.now()
					print(f"Total time Taken to execute the command on the host {device['ip']} is {end_time-start_time}")

				else:
					print("No device prompt found")
			##(Condition 3)
			else:
				print("No prompt occured in the connection \n Closing all connection..........")
				host_session.write_channel(f"exit\r\n")
				if host_session.remote_conn.transport.is_active():   ##Paramiko method to check either connection is still alive or not
					print("Connection is still activate not able to close the host_session")
				else:
					print("Connection to the jump host server is disconnected")

	except Exception as e:
		print(f"Common Exception occured in the function {e}")

def Jump_Host_Connection()->object:
	'''
	Function to connect to the jump host server first and then connect to the another networking device
	'''
	try:
		print(f"Connecting to the host:- {jump_host_details["ip"]}......")
		host_session = ConnectHandler(**jump_host_details)
		if host_session:
			print(f"Connected to the host:- {jump_host_details["ip"]}.....")
			host_prompt = host_session.find_prompt()
			print(f"Trying to find the prompt of the host....")
			if host_prompt:
				print(f"Found the prompt of the host server")
				return host_session
			else:
				print(f"Not able to found the prompt......")
				return False
		else:
			print(f"Not able to Connect to the host.......")
			return False
	except NetMikoAuthenticationException:
		print(f"NetMikoAuthenticationException exception have occured in the function {__name__}")
	except NetmikoTimeoutException:
		print(f"Timout Exception occured in the function {__name__}")
	except NetmikoBaseException:
		print(f"Netmiko anonymous exception occured in the function {__name__}")
	except Exception as e:
		print(f"Netmiko Common Exception occurred in the function {__name__}")

def main()->None:
	jump_host_session = Jump_Host_Connection()
	if jump_host_session:
		device_Details = generate_device_details()
		print(f"Device Details ----------> {device_Details} <-----------")
		if device_Details:
			result = Device_Remote_Connection(devices= device_Details,host_session=jump_host_session)
			print(f"Result of the device Remote Connection .... {result}.......")
		else:
			print("Device Details is not generated properly")
	else:
		print("Not able to connect with the jump host.......")

if __name__ == '__main__':
	main()

