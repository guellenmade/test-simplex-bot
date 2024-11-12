import threading
import json
import time
import random

from typing import Callable

#from timed_function import TimedFunction #Still in progress

class SimplexBot():

    def __init__(self, username:str, socket:str):
        self.username = username
        self.socket = socket
        print(f"New bot started for user: {self.username}.")

    def stop_bot(self):
        #ToDo: Store persistence stuff
        #ToDo: Close running threads
        pass

    def send_bot_command(self, command:list):
        # command handling for this bot
        #ToDo: Change and add your bot commands in this switch. Its recommended to just call one function witch handels the rest of the parameters
        match command[0].lower():
            case "help": 
                self.__help_bot_commands(command)

            #case "timer":
            #    example_timed_function(ws, message_sender, message_command_params)

            case _:
                message = "Command not found. Try \"help\" "
                self.__send_text_message(message)

    ''' #Still in progress
    #ToDo: copy rename this function as desired for every function you call in on_message
    def __example_timed_function(self, timer_command:str):
        invalid_parameter_error_message = "command used with wrong parameters. Try \"help\" "
        def example_function(ws, message_target:str, message:str):
            # functionality of the function that should be called after time
            self.__send_text_message(message)
        try:
            match timer_command[1].lower():
                case "new":
                    timer_string = timer_command[2]
                    notification_message = timer_command[3]
                    # call timed function
                    example_function(ws, message_target, f"Just a test. Inputs: {timer_string}, {notification_message}") #ToDo: change to the timed_function
                case "list":
                    pass
                case "stop":
                    pass
                case _:
                    send_text_message(ws, message_target, invalid_parameter_error_message)
        except IndexError:
            send_text_message(ws, message_target, invalid_parameter_error_message)'''

    def __send_text_message(self, message:str):
        # Sends text from the bot to the client
        corr_id = random.randint(0,100000)
        response = {
            "corrId": f"{corr_id}",
            "cmd": f"@{self.username} {message}"
        }
        response_json = json.dumps(response)
        self.socket.send(response_json)

    def __help_bot_commands(self, message_command_params:str):
        #ToDo: Modify this function so that it matches your bot commands
        command_overview = "help: Shows this screen or gives more information on given command\n" \
                        "\n" \
                        "timer: sets and controls a timer\n" \
                        "...\n"
        try:
            match message_command_params[1].lower():
                case "help":
                    help_message = "Shows help screen or gives more information on given command\n" \
                                "\n" \
                                "Usage: \n" \
                                "  help [command]\n" \
                                "\n" \
                                "Example: \n"\
                                "  help help\n"
                    self.__send_text_message(help_message)
                case "timer":
                    help_message = "Sets and controls timers.\n" \
                                "\n" \
                                "Usage: \n" \
                                "  timer new [hh:mm:ss] \"[Message]\"\n" \
                                "  timer list\n" \
                                "  timer stop [id]\n" \
                                "\n" \
                                "Example: \n" \
                                "  timer new 1:02:01 \"Notification message\"\n" \
                                "  timer new 12 \"Notification message\"\n"
                    self.__send_text_message(help_message)
                case _:
                    self.__send_text_message(command_overview)
        except IndexError:
            self.__send_text_message(command_overview)