import inspect
import re


class GlobalLogger:
    """
    Singleton logger class for logging messages.

    Attributes:
        _instance (GlobalLogger): Singleton instance of the GlobalLogger class.
        __messages_dict (dict): Dictionary to store log messages.

    Methods:
        __new__: Creates a new instance of the GlobalLogger class if it doesn't exist.
        __init__: Initializes the GlobalLogger instance.
        __my_file_name: Retrieves the name of the calling module.
        get_file_name: Retrieves the name of the module associated with the logger.
        message: Logs a message associated with the calling module.
        __getitem__: Retrieves the log messages associated with a specific module.
        __get_log_level: Retrieves the log level of the logger.
        log: Logs a message with the specified log level.
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the GlobalLogger class if it doesn't exist.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            GlobalLogger: The singleton instance of the GlobalLogger class.
        """
        if not cls._instance:
            cls._instance = super(GlobalLogger, cls).__new__(cls, *args, **kwargs)
            cls._instance.__messages_dict = {}
        return cls._instance
    
    
    def __init__(self)->None:
        """
        Initializes the GlobalLogger instance.

        Returns:
            None
        """
        self.__file_name:str = self.__my_file_name()
        self.__log_level:str = "LOG"
        if self.get_file_name() not in self.__messages_dict:
            self.__messages_dict:dict[str, list[str]] = {self.get_file_name(): []}
        
    
    def __my_file_name(self)->str:
        """
        Retrieves the name of the calling module.

        Returns:
            str: The name of the calling module.
        """
        module_name:str = inspect.currentframe().f_globals['__file__']
        file_name:str = re.search(r"(\w+).py", module_name)
        return file_name.group(1)
    
    
    def get_file_name(self)->str:
        """
        Retrieves the name of the module associated with the logger.

        Returns:
            str: The name of the module associated with the logger.

        Example:
            ... in salat.py
            >>> logger = GlobalLogger()
            >>> logger.get_file_name()
            'salat'
        """
        return self.__file_name

    
    def message(self, msg:str)->None:
        """
        Logs a message associated with the calling module.

        Args:
            msg (str): The message to log.

        Returns:
            None

        Example:
            >>> logger = GlobalLogger()
            >>> logger.message("No onions!")
        """
        self.__messages_dict[self.get_file_name()].append(msg)

    
    def __getitem__(self, key:str)->str:
        """
        Retrieves the log messages associated with a specific module.

        Args:
            key (str): The name of the module.

        Returns:
            str: The log messages associated with the specified module.

        Example:
            ... in salat.py
            >>> logger = GlobalLogger()
            >>> logger["salat"]
            '[salat] - ['This in an info message.', 'This is an error message.', 'This message also shows as an error.', 'No onions!']'
        """
        return f"[{self.get_file_name()}] - {self.__messages_dict[key]}"
    
    
    def __get_log_level(self)->str:
        """
        Retrieves the log level of the logger.

        Returns:
            str: The log level of the logger.
        """
        return self.__log_level
    
    
    def log(self, message:str)->None:
        """
        Logs a message with the specified log level.

        Args:
            message (str): The message to log.

        Returns:
            None

        Example:
            >>> logger = GlobalLogger()
            >>> logger.log("This is an info message.")
        """
        print(f"[{self.__get_log_level()}] - {message}")


if __name__ == "__main__":
    """
    Main block for testing the functionality of the GlobalLogger class.
    """
    logger1:GlobalLogger = GlobalLogger()

    logger1.log("This is an info message.")
    logger1.message("This in an info message.")
    print(logger1["salat"])

    logger2:GlobalLogger = GlobalLogger()

    logger2.log("This is an error message.")
    logger2.message("This is an error message.")
    logger1.log("This message also shows as an error.")
    logger1.message("This message also shows as an error.")
    print(logger2["salat"])

    myLogger:GlobalLogger = GlobalLogger()

    myLogger.message("No onions!")

    print(myLogger["salat"])
