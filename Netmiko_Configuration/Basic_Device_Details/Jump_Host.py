from netmiko import ConnectHandler, redispatch
import time

# Jump Server Details
jump_server_details = {
    "device_type": "terminal_server",
    "ip": "192.168.1.2",
    "username": "server",
    "global_delay_factor": 5,
    "use_keys": True,  # This indicates that key-based authentication will be used
    "key_file": "/Users/surendrasingh/.ssh/id_ed25519"  # Specify the path to your private key
}

# Target Server Details
target_server_details = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.100",
    "username": "admin",
    "password": "hackerzone"
}

# Function to connect to the target machine from the jump server
def jump_on_server(jump_server, target_server):
    try:
        print(f"Connecting to the Jump server {jump_server['ip']} with username {jump_server['username']}")
        netmiko_session = ConnectHandler(**jump_server)  # Connect to the jump server
        preprompt = netmiko_session.find_prompt()  # Getting the initial prompt
        print(f"This was the prompt before the SSH connection to the target device: {preprompt}")

        # Send SSH command to target device via the jump server
        netmiko_session.write_channel(f"ssh {target_server['username']}@{target_server['ip']}\r\n")
        time.sleep(1)
        output = netmiko_session.read_channel()

        # Check if the password prompt is shown
        if "password" in output.lower():
            print("We are passing the password to the jump server...")
            netmiko_session.write_channel(f"{target_server['password']}\r\n")
            redispatch(netmiko_session, device_type="cisco_ios")  # Switch context to the target device type
            print(f"Successfully connected to target device. Prompt: {netmiko_session.find_prompt()[:-1]}")
            return True
        else:
            print("Password prompt not found, something went wrong.")
            return netmiko_session

    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

# Main function to initiate the connection
def main():
    result = jump_on_server(jump_server=jump_server_details, target_server=target_server_details)
    print(f"Output from the jump server: {result}")

if __name__ == "__main__":
    main()

from netmiko import ConnectHandler

# Define your device connection details (excluding jump host details)
device = {
    'device_type': 'cisco_ios',  # Or any other type (e.g., juniper, arista)
    'host': '192.168.1.100',     # Target device IP address
    'username': 'admin',         # Target device username
    'password': 'cisco123',      # Target device password
    'use_keys': True,            # Use SSH keys instead of password if configured
    'allow_agent': False,        # Disable agent forwarding for key
    'ssh_config_file': '/Users/surendrasingh/.ssh/config',  # Specify the SSH config file
}

# Establish the connection using Netmiko
net_connect = ConnectHandler(**device)

# Send a command to the device
output = net_connect.send_command('show ip interface brief')

# Print the output from the device
print(output)

# Close the connection
net_connect.disconnect()