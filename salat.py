import inspect
import re


class GlobalLogger:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalLogger, cls).__new__(cls, *args, **kwargs)
            cls._instance.__messages_dict = {}
        return cls._instance

    def __init__(self):
        self.__file_name = self.__my_file_name()
        self.__log_level = "LOG"
        if self.get_file_name() not in self.__messages_dict:
            self.__messages_dict = {self.get_file_name(): []}
        
    def __my_file_name(self)->str:
        module_name = inspect.currentframe().f_globals['__file__']
        file_name = re.search(r"(\w+).py", module_name)
        return file_name.group(1)
    
    def get_file_name(self)->str:
        return self.__file_name

    def message(self, msg:str):
        self.__messages_dict[self.get_file_name()].append(msg)

    def __getitem__(self, key):
        return f"[{self.get_file_name()}] - {self.__messages_dict[key]}"
    
    def __get_log_level(self):
        return self.__log_level
    
    def log(self, message):
        print(f"[{self.__get_log_level()}] - {message}")


logger1 = GlobalLogger()
logger1.log("This is an info message.")
logger1.message("This in an info message.")
print(logger1["salat"])
logger2 = GlobalLogger()
logger2.log("This is an error message.")
logger2.message("This is an error message.")
logger1.log("This message also shows as an error.")
logger1.message("This message also shows as an error.")
print(logger2["salat"])

myLogger = GlobalLogger()
myLogger.message("No onions!")

print(myLogger["salat"])