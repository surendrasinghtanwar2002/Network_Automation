from netmiko import ConnectHandler, ConnectionException,NetmikoTimeoutException,NetmikoAuthenticationException,NetmikoBaseException
from concurrent.futures import ThreadPoolExecutor,BrokenExecutor,TimeoutError,CancelledError
from typing import List,Tuple,Dict,Union,Callable,Any
from datetime import datetime
from getpass import getpass
from time import sleep
from sys import exit
import functools
import logging
import shutil
import re
import os

## Device_Details ##
device_Details = [
    {
        "Device Type": "ios",
        "Device Address": "192.168.1.125",
        "Region": "Data Center",
        "Device_Role": "Router"
    },
    {
        "Device Type": "ios",
        "Device Address": "192.168.1.120",
        "Region": "Data Center",
        "Device_Role": "Router"
    },
    {
        "Device Type": "ios",
        "Device Address": "192.168.1.110",
        "Region": "Data Center",
        "Device_Role": "Router"
    },
    {
        "Device Type": "ios",
        "Device Address": "192.168.1.115",
        "Region": "Data Center",
        "Device_Role": "Router"
    },
]

router_configuration_commands = ["router eigrp 100","no auto-summary","network 0.0.0.0","exit","do write"]

##All_Text
all_text = {
    "keyboard_error":"Keyboard Interuption occured due to key pressed.",
    "value_error":"Value error occured in",
    "type_error":"Incompatible types are mixed in an operation in",
    "undeclared_variable":"Using an undeclared variable in",
    "connection_exception":"Netmiko Connection Exception occured in",
    'netmiko_timeout':"Netmiko Timeout Exception Occured in",
    "netmiko_auth_error":"Netmiko Authentication Error in",
    "netmiko_common_exception":"Netmiko Common or base exception occured in",
    "import_error":"Import Error found in",
    "file_not_found":"Your given file path is not presented",
    "os_error":"Os Error Occured in",
    'username':"Enter your Username:- ",
    "password":"Enter your Password:- ",
    "invalid_auth_data":"Please Enter valid username and password",
    "limit_exceed":' You have reached your limit we are closing the session ',
    "exit_script":" Thank you for using the script ",
    "priviledge_mode":" We are in Priviledge Mode ",
    "device_Router":"Device is Router",
    "not_device_Router":"Device is not Router",
    "backup_device":"Backup Created Succesfully of device",
}

def custom_logger(logger_name:str,logger_file_path:str,logger_level=logging.INFO)->object:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(logger_file_path)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger_path = os.path.join(os.getcwd(),"app.log")
mylogger = custom_logger(logger_name="Netmiko_Logger",logger_file_path=logger_path)


def exceptionhandler(func)->None:
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except KeyboardInterrupt:
            mylogger.error(all_text['keyboard_error'])
        except ValueError as value:
            mylogger.error(f"{all_text['value_error']} {func.__name__} {value}")
        except TypeError as typerror:
            mylogger.error(f"{all_text['type_error']} {func.__name__} {typerror}")
        except NameError as namerror:
            mylogger.error(f"{all_text['undeclared_variable']} {func.__name__} {namerror}")
        except ImportError as error:
            mylogger.error(f"{all_text['import_error']} {func.__name__} {error}")
        except FileNotFoundError as filefounderror:
            mylogger.error(f'{all_text['file_not_found']} {filefounderror} in {func.__name__} ')
        except OSError as oserror:
            mylogger.error(f'{all_text['os_error']} {func.__name__} {oserror}')
        except ConnectionException as connection_error:
            mylogger.critical(f"{all_text['connection_exception']} {func.__name__} {connection_error}")
        except NetmikoTimeoutException as timeout:
            mylogger.error(f"{all_text['netmiko_timeout']} {func.__name__} {timeout}")
        except NetmikoAuthenticationException as autherror:
            mylogger.error(f"{all_text['netmiko_auth_error']} {func.__name__} {autherror}")
        except NetmikoBaseException as base_error:
            mylogger.error(f"{all_text['netmiko_common_exception']} {func.__name__} {base_error}")
             
    return wrapper


@exceptionhandler
def clearscreen():
    os.system("cls" if os.name == "nt" else "clear")

@exceptionhandler
def backup_device(session:object,command="show run"):
    backup_data = session.send_command(command)
    current_datatime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    filename = f"Backup {session.host} {current_datatime}.txt"
    with open(filename,"w+") as backup:
        backup.write(backup_data)
        return True

@exceptionhandler
def command_output_file(command_Data:str):
    with open("command_Execution_ouput.txt","w") as backup:
        backup.write(command_Data)
        return True

@exceptionhandler
def routing_protocol_configuration(session: object):    
    backup_status = backup_device(session)
    
    if backup_status:
        print(f"{all_text['backup_device']} {session.host}")
    else:
        print(f"Backup was not performed for {session.host}. Continuing with configuration...")
 
    
    final_output = " "
    command_output = session.send_config_set(router_configuration_commands)
    final_output += f"Command Executed on {session.host} and output is \n{command_output}"
    command_output_file(final_output)
        
    if "Error" in command_output:
        print(f"Error executing command '{router_configuration_commands}': {command_output}")
        return False

    print(final_output)
    return True
            

@exceptionhandler
def device_send_command(session:object,command="show version")->None:
    prompt_ouput = session.find_prompt()                
    if not prompt_ouput.endswith('#'):              ##Check either prompt is in privilege mode	or not
        prompt_permission = session.send_command('enable')
        if 'Password' in prompt_permission:
            final_prompt = session.send_comman('hackerzone')
        else:
             print(all_text['priviledge_mode'])
             return
        
    final_prompt = session.find_prompt()
    if final_prompt.endswith('#'):
        print(f"{all_text['priviledge_mode']}".center(shutil.get_terminal_size().columns, "^"))
        device_version_output = session.send_command(command)
        pattern = r'ROM:\s+[A-Z]\d{4}'

        matches = re.search(pattern,device_version_output)
        if matches != None:
            print(f"{all_text['device_Router']}:- {session.host} ".center(shutil.get_terminal_size().columns, "^"))
            command_result = routing_protocol_configuration(session)
            return command_result
            
        else:
            print(f"{all_text['not_device_Router']}:- {session.host}".center(shutil.get_terminal_size().columns, "!"))
            pass

@exceptionhandler
def device_validator(devices:List):
    print("Device Validation will work here")
    result = device_connection_worker(device_send_command,devices)
    return result


@exceptionhandler
def session_intialiser(device:Dict)-> Union[object | bool]:
    print(f" Connecting to the Host {device['ip']} ".center(shutil.get_terminal_size().columns, "~"))
    session = ConnectHandler(**device)
    if session:
        print(f" Succesfully connected to host {device['ip']} ".center(shutil.get_terminal_size().columns, "^"))
        return session
    else:
        print(f" Not able to connect with host {device['ip']} ".center(shutil.get_terminal_size().columns, "!"))
        return False

@exceptionhandler
def device_connection_worker(func_name: Callable[[str], Any],iterable_items:List)->List:
    with ThreadPoolExecutor(max_workers=10) as executor:
        connections = executor.map(func_name,iterable_items)
        valid_connection = list(filter(lambda x: x != False and x != None,connections))      ##Filtering the valid connection only
        return valid_connection

@exceptionhandler
def generate_device_info(user:str,passw:str)->List:
    device_list = []        ##Device List
    for device in device_Details:
        if device['Device Type'] == 'ios':
            device_list.append({
                "device_type":"cisco_ios",
                "ip":device['Device Address'],
                "username": user,
                "password":passw,
                })
        elif device['Device Type'] == 'iosxe':
                device_list.append({
                "device_type":"cisco_iosxe",
                "ip":device['Device Address'],
                "username": user,
                "password":passw,
                })
        elif device['Device Type'] == 'iosxr':
                device_list.append({
                "device_type":"cisco_iosxe",
                "ip":device['Device Address'],
                "username": user,
                "password":passw,
                })
    return device_list

@exceptionhandler
def user_Auth()->Tuple:

    start = 0
    end = 3
    while start < end:
        username = input(all_text['username'])
        password = getpass(all_text['password'])
        if username and password:
            return username,password
        else:
            start+=1
            print(all_text['invalid_auth_data'])
    print(all_text['limit_exceed'].center(shutil.get_terminal_size().columns, "!"))
    sleep(3)        ## 3 second delay
    clearscreen()
    exit(all_text['exit_script'].center(shutil.get_terminal_size().columns, "$"))


def main()->None:
    print("Main function will execute soon")
    clearscreen()
    username,password = user_Auth()
    device_list = generate_device_info(username,password)
    devices_session = device_connection_worker(session_intialiser,device_list)
    result = device_validator(devices_session)
    print(result)

if __name__ == "__main__":
    main()
