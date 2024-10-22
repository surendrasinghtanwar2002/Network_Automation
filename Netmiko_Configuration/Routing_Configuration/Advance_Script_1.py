from netmiko import ConnectHandler,NetmikoAuthenticationException,NetmikoTimeoutException,NetmikoBaseException
from concurrent.futures import ThreadPoolExecutor,BrokenExecutor,TimeoutError,CancelledError
from typing import AnyStr,List,Tuple
from getpass import getpass
from sys import exit
import functools
import shutil
import os

##device details
device_details = [
    {
        "Device Type":"cisco_ios",
        "Device Address":"192.168.1.100",
        "Location":"Data Center",
        "Device_Role":"Router",
    },
    {
        "Device Type":"iosxr",
        "Device Address":"192.168.1.105",
        "Location":"Data Center",
        "Device_Role":"Router",
    },
    {
        "Device Type":"iosxr",
        "Device Address":"192.168.1.110",
        "Location":"Data Center",
        "Device_Role":"Router",
    },
    {
        "Device Type":"cisco_ios",
        "Device Address":"192.168.1.110",
        "Location":"Data Center",
        "Device_Role":"Switch",
    }
    ]

def common_exception_handler(func):
    """
    A decorator to handle common exceptions for the wrapped function.

    Args:
        func (callable): The function to be wrapped and monitored for exceptions.

    Returns:
        callable: The wrapper function that handles exceptions.
    
    This decorator catches specific exceptions and prints relevant error messages 
    while preserving the original function's name for easier debugging.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as value:
            print(f"ValueError occurred in {func.__name__}: {value}")
        except OSError as os_error:
            print(f"OSError occurred in {func.__name__}: {os_error}")
        except EOFError:
            print(f"EOFError: End of input encountered in {func.__name__}. Please try again.")
        except KeyboardInterrupt:
            print(f"Keyboard Interrupt occurred due to user input in {func.__name__}")
        except NetmikoAuthenticationException:
            print(f"Netmiko Authentication Exception occurred due to wrong authentication details in {func.__name__}")
        except NetmikoTimeoutException:
            print(f"Netmiko Timeout Exception occurred in {func.__name__}")
        except NetmikoBaseException as e:
            print(f"Netmiko error occurred in {func.__name__}: {e}")
        except TimeoutError:
            print(f"The operation timed out in {func.__name__}")
        except BrokenExecutor:
            print(f"The thread executor is broken in {func.__name__}")
        except RuntimeError:
            print(f"Runtime error occurred in {func.__name__}")
        except CancelledError:
            print(f"Cancelled error occurred in {func.__name__}")
        except Exception as e:
            print(f"An unexpected error occurred in {func.__name__}: {e}")

    return wrapper

@common_exception_handler
def clear_screen() -> None:
    """
    Clears the terminal screen.

    This function uses the appropriate command for the operating system 
    (Windows or Unix-based) to clear the console output.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

@common_exception_handler
def device_detail_generator(user: str, passw: str) -> List:
    """
    Generates a list of device details for connecting to network devices.

    Args:
        user (str): The username for device authentication.
        passw (str): The password for device authentication.

    Returns:
        List: A list of dictionaries containing device details, including 
              device type, IP address, username, and password.
    """
    
    devices = []  # Used for storing the devices list
    for device in device_details:
        if device['Device Type'] == 'cisco_ios':
            devices.append({
                "device_type": device['Device Type'],
                "ip": device['Device Address'],
                "username": user,
                "password": passw
            })
        elif device['Device Type'] == 'iosxr':
            devices.append({
                "device_type": device['Device Type'],
                "ip": device['Device Address'],
                "username": user,
                "password": passw
            })
    
    return devices

@common_exception_handler
def user_auth() -> Tuple:
    """
    Prompts the user to input a username and password for device authentication.

    Returns:
        tuple: A tuple containing the username and password if both are provided; 
               otherwise, exits after three attempts.
    """
    c_starter = 0
    c_end = 3
    while c_starter < c_end:
        username = input("Enter Username:- ").strip()
        password = getpass(prompt="Enter Password:- ").strip()
        if username and password:
            return username, password
        else:
            print("Please Enter proper details")
            c_starter += 1
    exit(" Limit Exceed Closing the connection ".center(shutil.get_terminal_size().columns, "!"))


@common_exception_handler
def initialize_device_session(device)->object:
    """
    Creates a Netmiko session to the specified device.

    Args:
        device (dict): Device connection details.

    Returns:
        Netmiko.Session or bool: The session object if successful; otherwise, False.
    """
    netmiko_session = ConnectHandler(**device)
    if netmiko_session:
        return netmiko_session
    else:
        return False

@common_exception_handler
def Thread_Executor(devices:List):
    '''
    Creates multiple threads to establish Netmiko sessions for a list of devices.

    Args:
        devices (List): A list of device parameters for connection.

    Returns:
        Iterator: An iterator of results from the device session initialization.
    '''
    print("In this we will create multiple thread for the netmiko session")
    with ThreadPoolExecutor(max_workers=5) as executor:
        result = executor.map(initialize_device_session,devices)
        valid_connection = list(filter(lambda x: x != False, result))       ##Filtering the false object from the list
        return valid_connection

def main():
       username,password = user_auth()
       device_list = device_detail_generator(user=username,passw=password)  
       print(f"Device List is there {device_list}")
       result = Thread_Executor(devices=device_list)
       print(f"This is the valid thread pool executor for the function {result}")
       

if __name__ == "__main__":
    main()