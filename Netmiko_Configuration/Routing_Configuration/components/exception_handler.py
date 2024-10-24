from netmiko import ConnectionException,NetmikoTimeoutException,NetmikoAuthenticationException,NetmikoBaseException
from assets.text_style import Text_Style
from assets.text_file import Text_File

def NetmikoException_Handler(method: any):
    """
    Handles all Netmiko and Paramiko exceptions.

    Arguments:
        method (function): The class method to wrap with exception handling.

    Returns:
        Any: The result of the method, or False if an exception occurs.
    """
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except NetmikoTimeoutException:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Netmiko_Timeout_Exception"],
                secondary_text=__name__
            )
            return False
        except NetmikoBaseException:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Netmiko_Base_Exception"],
                secondary_text=__name__
            )
            return False
        except NetmikoAuthenticationException:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Netmiko_Authentication_exception"],
                secondary_text=__name__
            )
            return False
        except ConnectionException:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["ssh_exception"],
                secondary_text=__name__
            )
            return False
        except TypeError:
            Text_Style.common_text(
                primary_text=Text_File.exception_text["Type_error"],
                secondary_text=__name__
            )
            return False
        except IOError as ioerror:
            Text_Style.ExceptionTextFormatter(primary_text=Text_File.exception_text["IOerror"],secondary_text=ioerror)
            
        except Exception as e:
            # Catch any other unexpected exceptions
            Text_Style.common_text(
                primary_text=Text_File.exception_text["general_exception"],
                secondary_text=str(e)
            )
            return False
        

    return wrapper
