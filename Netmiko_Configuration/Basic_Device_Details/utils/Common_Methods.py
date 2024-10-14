from netmiko import ConnectHandler
from utils.Exception_Handler import Netmiko_Exception_Handler

def send_command(sessions: object | list, commands: str | list) -> str:
    """
    Function to send commands to one or more network sessions.
    If commands is a single string, it sends the command to the session(s).
    If commands is a list, it sends each command to the session(s).

    Args:
        sessions (object | list): A session object or a list of session objects.
        commands (str | list): A command or a list of commands to be sent.

    Returns:
        str: The combined output of the commands sent from all sessions.
    """
    final_output = ""  # This will store the entire final output in string format

    # Normalize sessions to be a list
    if isinstance(sessions, object):
        sessions = [sessions]  # Wrap single session in a list

    if not isinstance(sessions, list) or not all(isinstance(session, object) for session in sessions):
        return "Invalid session objects provided."

    if isinstance(commands, str):
        # Sending a single command to all sessions
        for session in sessions:
            try:
                output = session.send_command(commands)
                final_output += f"Output for command '{commands}' on {session.host}:\n{output}\n"
            except Exception as e:
                final_output += f"Error sending command '{commands}' on {session.host}: {e}\n"
    
    elif isinstance(commands, list):
        # Sending a list of commands to all sessions
        for session in sessions:
            for command in commands:
                try:
                    output = session.send_command(command)
                    final_output += f"Output for command '{command}' on {session.host}:\n{output}\n"
                except Exception as e:
                    final_output += f"Error sending command '{command}' on {session.host}: {e}\n"

    else:
        return "You have not provided valid command details. Please try again."
    
    return final_output

@Netmiko_Exception_Handler
def connection_establishement(device_details):
    """
    Function use to make the connection to the multiple devices using 
    a single function and return a object(Single Device) or a list of object (Multiple Device)
    """
    session_list = []
    if isinstance(device_details,dict):
        session = ConnectHandler(**device_details)
        return session
    elif isinstance(device_details,list):
        for device in device_details:
            session = ConnectHandler(**device)
            session_list.append(session)
        print("We are connected to each and every devices")
        return session_list