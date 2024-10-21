from netmiko import ConnectHandler,NetMikoAuthenticationException,NetmikoTimeoutException,NetmikoBaseException,redispatch
from time import sleep,time
from tabulate import tabulate
from typing import List,Any
import shutil
import datetime

##Jump Host Details
jump_host_Details = {
	"device_type": "terminal_server",
    "ip": "192.168.1.30",
    "username": "server",
    "port": "2222",
    "use_keys": True,  # Key-based authentication
    "key_file": "/Users/surendrasingh/.ssh/id_ed25519"  # Path to your private key
}

##Remote Device Details (Network Device Details)
remote_device_details = [
    {
        "location": "Main_Building",
        "device_type": "ios",
        "device_role": "Router",
        "ip_address": "192.168.1.100"
    },
    {
        "location": "Server Room",
        "device_type": "ios",
        "device_role": "Router",
        "ip_address": "192.168.1.105"
    },
    {
        "location": "Marketing Area",
        "device_type": "iosxr",
        "device_role": "Router",
        "ip_address": "192.168.1.110"
    },
    {
        "location": "Employee_Area",
        "device_type": "iosxr",
        "device_role": "Switch",
        "ip_address": "192.168.1.115"
    }
]
## Vlan Details for each device
vlans = {
    '10': 'MGMT',
    '20': 'DATA',
    '30': 'active_directory',
    '31': 'web_servers',
    '32': 'admin',
    '33': 'network'
    }

def device_details_generator():
	'''
	Function to generate the device details
	'''
	try:
		device_details = []
		for device in remote_device_details:
			if device['device_type'] == "ios":				## If device type is ios
				device_details.append({
					"device_type":"cisco_ios",
					"ip":device['ip_address'],
					"username":"admin",
					"password":"hackerzone",
					"device_location":device['location'],
					"device_role":device['device_role']
					})
			elif device['device_type'] == "iosxr":			## If device type is iosxr
				device_details.append({
					"device_type":"cisco_ios",
					"ip":device['ip_address'],
					"username":"admin",
					"password":"hackerzone",
					"device_location":device['location'],
					"device_role":device['device_role']
					})
		return device_details
	except Exception as e:
		print(f"Common Exception occured in {__name__}")

def create_vlan(session:object)->Any:
	'''
	Function to create the vlan
	'''
	try:
		vlan_details = session.send_command('show vlan',use_textfsm=True)
		current_vlan_details = {} ##Contain the current vlan details
		for vlan in vlan_details:
			current_vlan_details[vlan['vlan_id']] = vlan['vlan_name']


	except Exception as e:
		print(f"Common Exception occured in {__name__}")

def device_mode(session:object)->Any:
	''' Function to check device in config mode or not and switch to the config mode '''
	try:
		if session.check_config_mode():
			print("Device is Already in enable")
		else:
			print("Device is not in enable mode trying to Switch to configuration mode")
			if session.config_mode():
				print("Now we are in config mode")
	except Exception as e:
		print(f"Common Exception occured in the function {__name__}")

def Remote_Device_Connection(session:object,devices:List)->Any:
	'''
	Function allowo to connect with the remote devices
	'''
	try:
		for device in devices:
			print(f"Establishing connection to host {device['ip']} located in {device['device_location']} and device role is {device['device_role']}")
			session.write_channel(f"ssh {device['username']}@{device['ip']}\r\n")
			sleep(4) 	## 4 second delay
			ssh_connection_permission = session.read_channel()

			##First Condition to check either connection need the yes no permission
			if '(yes/no)?' in ssh_connection_permission.lower():
				session.write_channel(f"{device['password']}\r\n")
				sleep(4) ## 4 second delay
				password_prompt = session.read_channel()
				if "Password:" in password_prompt.strip():
					print(" Password prompt found ".center(shutil.get_terminal_size().columns, "*"))
					session.write_channel(f"{device['password']}\r\n")
					sleep(4) ## 4 second delay
					device_prompt = session.read_channel()
					if device_prompt.strip().endswith('>') or device_prompt.strip().endswith('#'):
						print(f" Connection to the host is succesful ".center(shutil.get_terminal_size().columns, "*"))
						redispatch(session,device_type="cisco_ios")								##Redispatch when session is established to the device succesful
						device_mode()
					else:
						print(f"Connection to the host is not succesful ".center(shutil.get_terminal_size().columns, "!"))
				else:
					print("Password prompt not found closing........")

			##Second Condition to check either connection need the yes no permission
			elif 'Password:' in ssh_connection_permission.strip():
				print(" Password prompt found ".center(shutil.get_terminal_size().columns, "*"))
				session.write_channel(f"{device['password']}\r\n")
				sleep(4) ## 4 second delay
				device_prompt = session.read_channel()
				if device_prompt.strip().endswith('>') or device_prompt.strip().endswith('#'):
					print(f" Connection to the host is succesful ".center(shutil.get_terminal_size().columns, "*"))

				else:
					print(f"Connection to the host is not succesful ".center(shutil.get_terminal_size().columns, "!"))

			##Third Condition to check either connection is not established to the device
			else:
				print("No prompt occured in the connection \n Closing all connection..........")
				session.write_channel(f"exit\r\n")
				if session.remote_conn.transport.is_active():   ##Paramiko method to check either connection is still alive or not
					print("Connection is still activate not able to close the host_session")
				else:
					print("Connection to the jump host server is disconnected")

	except Exception as e:
		print(f"Common Exception occured {e}")

def Jump_Host_Connection()->bool:
	'''
	Function allow to connect with the jump host server
	'''
	try:
		print(f"Connecting to the Jump Host Server {jump_host_Details['ip']}".center(shutil.get_terminal_size().columns,"#"))
		netmiko_session = ConnectHandler(**jump_host_Details)
		if netmiko_session:
			print(f"Connected to the Jump Host Server Succesfully {jump_host_Details['ip']}")
			sleep(4) ## 4 second delay after the succesful jump host connection
			jump_server_prompt = netmiko_session.find_prompt()
			print(f"Jump Host Server Prompt {jump_server_prompt}")
			return True
		else:
			print(f"Connection to Jump Host Server was not succesful please try again later")
			return False
	except NetMikoAuthenticationException:
		print(f"Authentication Error in {__name__}")
	except NetmikoTimeoutException:
		print(f"Netmiko Timeout Exception occured in {__name__} ")
	except NetmikoBaseException:
		print(f"Netmiko Base Exception occurred in {__name__}")
	except NetmikoBaseException:
		print(f"Netmiko Base Exception occurred in {__name__}")
	except Exception as e:
		print(f"Common Exception occured in {__name__}")

def main():
	jh_result = Jump_Host_Connection()
	if jh_result:
		print("We are succesfully made this connection to the jump host connection now trying to connect to the network device")
		device_details = device_details_generator()							##Device details Generator
		print(f"Device Details {device_details}")
		result = Remote_Device_Connection(session=jh_result,devices=device_details)
		print(f"Remote device Connection function result {result}")

	else:
		print("Not able to make the connection to the jump host connection")

if __name__ == "__main__":
	main()







