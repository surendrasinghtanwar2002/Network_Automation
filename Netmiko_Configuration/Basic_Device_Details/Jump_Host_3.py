from netmiko import ConnectHandler, redispatch, NetmikoTimeoutException, NetmikoAuthenticationException
from time import sleep

# Remote server details
remote_server_details = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.100",
    "username": 'admin',
    "password": "hackerzone"
}

# Jump Host Server details
jump_host_server_details = {
    "username": 'server',
    "ip": "192.168.1.30",
    "port": "2222",
    "device_type": "terminal_server",
    "password": "hackerzone",
}


def Jump_Host_Connection():
    """
    Function to connect to the jump host server
    """
    try:
        print("Connecting to the Jump Host Server...")
        netmiko_session = ConnectHandler(**jump_host_server_details)
        post_prompt = netmiko_session.find_prompt()
        print(f"Jump Host Prompt: {post_prompt}")
        return netmiko_session
    except NetmikoTimeoutException:
        print("Netmiko Timeout Exception occurred")
        return False
    except NetmikoAuthenticationException:
        print("Netmiko Authentication Exception occurred")
        return False
    except Exception as e:
        print(f"Exception occurred in the Jump Host Connection: {e}")
        return False


def Remote_Host_Connection(session):
    """
    Function to connect to the remote host from the jump host
    """
    try:
        if session:
            print(f"Connecting to the Remote Host {remote_server_details['ip']}...")
            session.write_channel(f"ssh {remote_server_details['username']}@{remote_server_details['ip']}\n")
            sleep(4)  # Delay for the SSH process to start
            
            output = session.read_channel()
            print(f"SSH Command Output: {output}")

            if "password" in output.lower():
                print("Password prompt detected.")
                session.write_channel(f"{remote_server_details['password']}\n")
                sleep(4)  # Wait for the authentication process to complete
                
                remote_host_prompt = session.read_channel()
                print(f"Remote host prompt after login: {remote_host_prompt}")

                if remote_host_prompt:
                    redispatch(session, device_type="cisco_ios")
                    output = session.send_command("show run")
                    print(f"Output of 'show run':\n{output}")
                else:
                    print("Unable to detect the remote host prompt.")
            else:
                print("Password prompt not detected in the output.")

        else:
            print("No session established to the jump host server.")
    except Exception as ssh_error:
        print(f"SSH Exception occurred while connecting to the remote host: {ssh_error}")


def main():
    try:
        # Connect to the Jump Host Server
        session = Jump_Host_Connection()
        # Connect to the Remote Host through the Jump Host
        Remote_Host_Connection(session)
    except Exception as e:
        print(f"Exception occurred in the main function: {e}")


if __name__ == "__main__":
    main()
