from netmiko import ConnectHandler, redispatch, NetMikoTimeoutException, NetMikoAuthenticationException
from typing import Dict, Any
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import shutil

# Jump Server Details
jump_server_details = {
    "device_type": "terminal_server",
    "ip": "192.168.1.30",
    "username": "server",
    "port": "2222",
    "use_keys": True,  # Key-based authentication
    "key_file": "/Users/surendrasingh/.ssh/id_ed25519"  # Path to your private key
}

# Network Device Details
network_device_details = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.100",
        "username": "admin",
        "password": "hackerzone"
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.105",
        "username": "admin",
        "password": "hackerzone"
    },

]

# Jump Server Connection
def Jump_Server_Connection() -> Any:
    """
    Function to Connect to the Jump Server
    """
    try:
        print(f"Connecting to Jump Server {jump_server_details['ip']}".center(shutil.get_terminal_size().columns, "!"))
        netmiko_session = ConnectHandler(**jump_server_details)
        if netmiko_session:
            print(f"Connected to Jump Server {jump_server_details['ip']}".center(shutil.get_terminal_size().columns, "/"))
            host_prompt = netmiko_session.find_prompt()
            print(f"Jump on Host Prompt: {host_prompt}")
            return netmiko_session
        else:
            print(f"Connection to Jump Server {jump_server_details['ip']} failed.".center(shutil.get_terminal_size().columns, "/"))
            return False
    except NetMikoTimeoutException:
        print(f"Netmiko Timeout Exception occurred while connecting to Jump Server.")
    except NetMikoAuthenticationException:
        print(f"Netmiko Authentication Error: Check your credentials for Jump Server.")
    except Exception as e:
        print(f"Exception occurred while connecting to Jump Server: {e}")

# Remote Server Connection
def Remote_Server_Connection(netmiko_connection: object, device_details: Dict) -> Any:
    """
    Function to Connect to the End Devices
    """
    try:
        print(f"This is the netmiko object let me check for {device_details['ip']} {netmiko_connection}")
        # Start SSH Connection to Device
        netmiko_connection.write_channel(f"ssh {device_details['username']}@{device_details['ip']}\n")
        sleep(2)  # Short delay for SSH command to process
        channel_output = netmiko_connection.read_channel()
        print(f"Channel output after SSH command: {channel_output}")

        # Check for SSH key confirmation prompt
        if '(yes/no)?' in channel_output.lower():
            print(f"SSH confirmation prompt found for {device_details['ip']}. Sending 'yes'.")
            netmiko_connection.write_channel("yes\n")
            sleep(2)
            channel_output += netmiko_connection.read_channel()
            if "password:" in channel_output.lower():
                print(f"Password prompt found for {device_details['ip']}. Sending password.")
                netmiko_connection.write_channel(f"{device_details['password']}\n")
                sleep(4)  # Wait for the device to respond
                device_prompt = netmiko_connection.read_channel()
                print(f"Device prompt after sending password: {device_prompt}")

                # Check if the device prompt is valid
                if ">" in device_prompt or "#" in device_prompt:
                    print(f"Successfully connected to device {device_details['ip']}. Prompt: {device_prompt}")
                    redispatch(netmiko_connection, device_type="cisco_ios")
                    return netmiko_connection
                else:
                    print(f"Failed to get a valid prompt from {device_details['ip']}. Output: {device_prompt}")
                    return False
                
        elif "password:" in channel_output.lower():
                print(f"Password prompt found for {device_details['ip']}. Sending password.")
                netmiko_connection.write_channel(f"{device_details['password']}\n")
                sleep(4)  # Wait for the device to respond
                device_prompt = netmiko_connection.read_channel()
                print(f"Device prompt after sending password: {device_prompt}")

                # Check if the device prompt is valid
                if ">" in device_prompt or "#" in device_prompt:
                    print(f"Successfully connected to device {device_details['ip']}. Prompt: {device_prompt}")
                    redispatch(netmiko_connection, device_type="cisco_ios")
                    return netmiko_connection
                else:
                    print(f"Failed to get a valid prompt from {device_details['ip']}. Output: {device_prompt}")
                    return False
        else:
            print(f"No password prompt found for {device_details['ip']}. Output: {channel_output}")
            return False

    except NetMikoTimeoutException:
        print(f"Netmiko Timeout Exception occurred while connecting to {device_details['ip']}.")
        return False
    except NetMikoAuthenticationException:
        print(f"Netmiko Authentication Error for device {device_details['ip']}.")
        return False
    except Exception as e:
        print(f"Exception occurred while connecting to device {device_details['ip']}: {e}")
        return False

# Threading Module
def Threading_module(session_connection: object) -> list:
    """
    Function to create multiple threads for connecting to devices
    """
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(lambda device: Remote_Server_Connection(session_connection, device), network_device_details))
            return results  # Return the results list
    except Exception as e:
        print(f"Exception occurred while threading: {e}")
        return []

def main():
    connection = Jump_Server_Connection()
    if connection:
        connections = Threading_module(connection)
        print(f"The Netmiko Connection results: {connections}")
        for connection in connections:
            command_output = connection.send_command('show run')
            print(f"The output of the command ----> {command_output}")

# Main Function Calls Here
if __name__ == "__main__":
    main()
