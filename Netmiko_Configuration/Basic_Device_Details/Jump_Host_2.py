from netmiko import Netmiko,ConnectHandler, redispatch
from time import sleep

## Jump on host server details
jump_host = {
    "device_type": "terminal_server",
    "username": "server",
    "ip": "192.168.1.30",
    "port":"2222",
    "password": "hackerzone",
}

## Remote server details
remote_host = {
    "device_type": "cisco_ios",
    "username": "admin",
    "password": "hackerzone",
    "ip": "192.168.1.100",
}

## Connection Function
def Jump_on_Host_Connection():
    try:
        print("Connecting to the Jump Server......")
        netmiko_session = Netmiko(**jump_host)
        
        if netmiko_session:
            print("Connected to Jump Host Server")
            print("Jump Host Prompt".center(120, "*"))
            print(f"Jump Host Server Prompt ------> {netmiko_session.find_prompt()}")
            print("Connecting to the Remote Server.....")
            # Send SSH command with key exchange options
            netmiko_session.write_channel(f"ssh {remote_host["username"]}@{remote_host["ip"]}\n")
            sleep(4)  # Delay for 4 seconds
            
            output = netmiko_session.read_channel()
            if "Password" in output:
                print("Yes we have found the password prompt inside the buffer memory")
            else:
                print("No we are not able to find the password prompt inside the buffer memory")
            # Send the password for the remote host
            netmiko_session.write_channel(f"{remote_host['password']}\n")
            sleep(4)  # Delay to allow password prompt processing
            output = netmiko_session.read_channel()
            print(f"Remote server output after password: {output}")   
            redispatch(netmiko_session, device_type="cisco_ios")
            output = netmiko_session.send_command("show run")
            print(f'This is the output of the server ------> {output}')

        else:
            print("Connection not established to the Jump Host Server")

    except Exception as e:
        print(f"This is the exception of the function: {e}")

def main():
    Jump_on_Host_Connection()

if __name__ == "__main__":
    main()
