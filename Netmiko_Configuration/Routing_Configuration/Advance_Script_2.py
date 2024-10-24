from netmiko import ConnectHandler, ConnectionException,NetmikoTimeoutException,NetmikoAuthenticationException,NetmikoBaseException
from concurrent.futures import ThreadPoolExecutor,BrokenExecutor,TimeoutError,CancelledError
from typing import List,Tuple,Dict,Union,Callable,Any
from datetime import datetime
from getpass import getpass
from time import sleep
from sys import exit
import functools
import threading
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
    # {
    #     "Device Type": "ios",
    #     "Device Address": "192.168.1.115",
    #     "Region": "Data Center",
    #     "Device_Role": "Router"
    # },
]

router_configuration_commands = [
    ("router eigrp 100","no auto-summary","network 0.0.0.0","exit","do write"),
    ("router ospf 1","router-id 1.1.1.1","network 192.168.1.0 0.0.0.255","exit","do write")
    ]

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
    "device_Router":" Device is Router ",
    "not_device_Router":" Device is not Router ",
    "backup_device":"Backup Created Succesfully of device",
    "no_routing_protocol":"No routing protocol is configured on the device",
    "routing_protocol_choice":"Please Choose your Routing Protocol (1:-> EIGRP | 2:-> OSPF | 3:-> RIP):- ",
    "routing_user_choice":"Your choice is",
    "invalid_choice":"Please provide the proper input",
    "no_router_config":"No router configuration is being performed on the device due to invalid input",
    "no_config_command_exit":"No config commands are avilable in our database for: "
}

##Global variable 
counter_start = 0
counter_end = 3

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


##Threading lock object
print_lock = threading.RLock()


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
def command_output_file(command_Data:str)->bool:
    with open("command_Execution_ouput.txt","a") as backup:
        backup.write(command_Data)
        return True


def reset_counter()->None:
    '''
    This function allow to reset the counter
    '''
    global counter_start
    counter_start = 0 ## reseting the counter value
    return None

@exceptionhandler
def routing_protocol_filter(filter_data:str)->bool:
    for router_config in router_configuration_commands:
        for internal_config in router_config:
            if filter_data.lower() in internal_config:
                return internal_config
            else: 
                return False

@exceptionhandler
@exceptionhandler
def routing_protocol_validator(session: object) -> bool:
    '''
    Routing Protocol validator function for choosing the validation
    '''
    clearscreen()
    pattern = "Routing Protocol is"

    routing_protocol_output = session.send_command('show ip protocol')

    if pattern not in routing_protocol_output:
        with print_lock:  # Locking before printing
            print(f"{all_text['no_routing_protocol']}".center(shutil.get_terminal_size().columns, "^"))

        global counter_start
        global counter_end    
        while counter_start < counter_end:
            with print_lock:  # Locking before input prompt
                user_choice = int(input(all_text["routing_protocol_choice"]))
            
            if isinstance(user_choice, int):
                reset_counter()  # Reset counter function
                match user_choice:
                    case 1:
                        with print_lock:  # Locking before printing
                            print(f"{all_text['routing_user_choice']} EIGRP")
                        eigrp_configuration_commands = routing_protocol_filter("eigrp")
                        if eigrp_configuration_commands:
                            command_output = session.send_config_set(eigrp_configuration_commands)
                            return command_output
                        else:
                            with print_lock:  # Locking before printing
                                print(f"{all_text['no_config_command_exit']} EIGRP")
                            return False
                        
                    case 2:
                        with print_lock:  # Locking before printing
                            print(f"{all_text['routing_user_choice']} OSPF")
                        ospf_configuration_commands = routing_protocol_filter("ospf")
                        if ospf_configuration_commands:
                            command_output = session.send_config_set(ospf_configuration_commands)
                            return command_output
                        else:
                            with print_lock:  # Locking before printing
                                print(f"{all_text['no_config_command_exit']} OSPF")
                            return False
                        
                    case 3:
                        with print_lock:  # Locking before printing
                            print(f"{all_text['routing_user_choice']} RIP")
                        rip_configuration_command = routing_protocol_filter("rip")
                        if rip_configuration_command:  # Changed to `rip_configuration_command`
                            command_output = session.send_config_set(rip_configuration_command)
                            return command_output
                        else:
                            with print_lock:  # Locking before printing
                                print(f"{all_text['no_config_command_exit']} RIP")
                            return False
            else:
                counter_start += 1  # Increasing the counter value
                with print_lock:  # Locking before printing
                    print(all_text["invalid_choice"])

        mylogger.error("limit_exceed")
        exit(all_text['no_router_config'].center(shutil.get_terminal_size().columns, "^"))  # exiting the script
    
    else:
        with print_lock:  # Locking before printing
            print(f"Routing Configuration is Already done on the device {session.host} with routing protocol:\n {routing_protocol_output}")

        return True  # Adjusted return value


@exceptionhandler
def routing_protocol_configuration(session: object)->bool:    
    backup_status = backup_device(session)
    
    if backup_status: 
        print(f" {all_text['backup_device']} {session.host} ".center(shutil.get_terminal_size().columns, "^"))
    else:
        print(f"Backup was not performed for {session.host}. Continuing with configuration...")
 
    ## In this section we will check either either device has already configured the routing protocol or not
    final_output = " "
    result = routing_protocol_validator(session)
    if result:
        final_output += f"Command Executed on {session.host} and output is:\n{result}\n"
        print(final_output)
        command_output_file(final_output)
        return True
    else:
        return False    

        
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
        print(f"{all_text['priviledge_mode']} on host {session.host}".center(shutil.get_terminal_size().columns, "^"))
        device_version_output = session.send_command(command)
        pattern = r'ROM:\s+[A-Z]\d{4}'

        matches = re.search(pattern,device_version_output)
        if matches != None:
            print(f" {all_text['device_Router']}:- {session.host} ".center(shutil.get_terminal_size().columns, "^"))
            routing_protocol_configuration(session)  
              
        else:
            print(f" {all_text['not_device_Router']}:- {session.host} ".center(shutil.get_terminal_size().columns, "!"))
            pass
    clearscreen() 

@exceptionhandler
def device_validator(devices:List):
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
