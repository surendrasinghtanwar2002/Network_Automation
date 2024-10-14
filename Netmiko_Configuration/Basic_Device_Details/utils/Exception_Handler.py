from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException, NetmikoBaseException
from paramiko import AuthenticationException, SSHException
import functools

def Netmiko_Exception_Handler(func):
    """
    Netmiko_Exception_Handler Function is designed to handle all Netmiko exceptions as well as Paramiko basic 
    exceptions.

    Args:
        func (function): The function to be wrapped and executed.

    Returns:
        function: The wrapped function with exception handling applied.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NetmikoTimeoutException:
            print(f"Netmiko Timeout Exception occurred in {func.__name__}")
        except NetmikoAuthenticationException as autherror:
            print(f"Netmiko Authentication Exception occurred in {func.__name__}: {autherror}")
        except NetmikoBaseException as error:
            print(f"Netmiko Exception occurred in {func.__name__}: {error}")
        except AuthenticationException as auth_error:
            print(f"Paramiko Authentication Exception occurred in {func.__name__}: {auth_error}")
        except SSHException:
            print(f"SSH Exception occurred due to network issues in {func.__name__}")
        except Exception as e:
            print(f"An unexpected error occurred in {func.__name__}: {e}")
        return None
    return wrapper


def Regular_Exception_Handler(func):
    """
    Regular_Exception_Handler is designed to handle all common exceptions such as TypeError, FileNotFoundError, etc.

    Args:
        func (function): The function to be wrapped and executed.

    Returns:
        function: The wrapped function with exception handling applied.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as value_error:
            print(f"ValueError occurred in {func.__name__}: {value_error}")
        except TypeError as type_error:
            print(f"TypeError occurred in {func.__name__}: {type_error}")
        except ModuleNotFoundError as module_error:
            print(f"ModuleNotFoundError occurred in {func.__name__}: {module_error}")
        except IOError as io_error:
            print(f"IOError occurred in {func.__name__}: {io_error}")
        except FileExistsError as file_error:
            print(f"FileExistsError occurred in {func.__name__}: {file_error}")
        except OSError as os_error:
            print(f"OSError occurred in {func.__name__}: {os_error}")
        except Exception as e:
            print(f"An unexpected error occurred in {func.__name__}: {e}")
        return None
    return wrapper
