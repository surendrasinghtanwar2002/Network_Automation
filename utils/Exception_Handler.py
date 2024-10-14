from netmiko import ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException,NetmikoBaseException
from paramiko import AuthenticationException,SSHException

def Netmiko_Exception_Handler(func:any):
	"""
	Netmiko_Exception_Handler Function is designed to handle all the Netmiko Exception as well Paramiko basic 
	exception.

	Args:
        method (function): The method to be wrapped and executed.

    Returns:
        function: The wrapped method with exception handling applied.
	"""
	@functools.wrapper(func)				
	def wrapper(*args,**kwargs):
		try:
			return func(*args,**kwargs)
		except NetmikoTimeoutException:
			print(f"Netmiko Timeout Exception have occured in {func.__name__}")
		except NetmikoAuthenticationException as autherror:
			print(f"Netmiko Authentication Exception have occured in {func.__name__}")
		except NetmikoBaseException as error:
			print(f"This is the netmiko all exception handler {error} in function {func.__name__}")
		except AuthenticationException as auth_error:
			print(f"This is the Paramiko Authentication exeception {auth_error} in function {func.__name__}")
		except SSHException:
			print(f"Ssh exception have occured due to network issue in function {func.__name__}")


def Regular_Exception_Handler(func:any):
	"""
	Regular Exception Handler is designed to handle all the regular exception of the function such as Typeerror, filenotfounderror, modulenotfounderror etc....

    Args:
        method (function): The method to be wrapped and executed.

    Returns:
        function: The wrapped method with exception handling applied.
	"""
	@functools.wrapper(func)
	def wrapper(*args,**kwargs):
		try:
			return func(*args,**kwargs)
		except ValueError as value:
			print(f"Value Error Exception occured in function {func.__name__}")
		except TypeError as type_error:
			print(f"Type Error have occured in function {func.__name__}")
		except ModuleNotFoundError as moduleerror:
			print(f"The Module not found exception occured in function {func.__name__}")
		except IOError as ioerror:
			print(f"The input output exception occured in function {func.__name__}")
		except FileExistsError as file_error;:
			print(f"The file exception have occured in function {func.__name__}")
		except OSError as oserror:
			print(f"The os exception have occured in function {func.__name__}")






			



