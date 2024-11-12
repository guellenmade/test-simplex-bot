import websocket
import threading
import json
import time
import random

from typing import Callable

from simplex_bot import SimplexBot

running_bots = {}

def format_command(bot_command_string:str)-> list:
    #formats an incomming command. Splits parameters and extracts inner strings
    try:
        param_list = []
        # separate strings from other parameters
        param_list_strings = bot_command_string.split("\"")
        for index,item in enumerate(param_list_strings):
            if index%2==0:
                param_list.extend(item.split(" "))
            else:
                param_list.append(f"\"{item}\"")
        param_list = list(filter(lambda x: x!='',param_list))
        return param_list
    except ValueError:
        raise ValueError("Invalid command format.")

def on_open(ws):
    print("Connected")

def on_message(ws, message):
    # Bot command and response flow here
    message_converted = json.loads(message)
    if message_converted["resp"]["type"] == "newChatItems":
        if message_converted["resp"].get("chatItems"):
            if message_converted["resp"]["chatItems"][0]["chatItem"]["chatDir"]["type"] == "directRcv":
                message_command = message_converted["resp"]["chatItems"][0]["chatItem"]["content"]["msgContent"]["text"]
                message_sender = message_converted["resp"]["chatItems"][0]["chatInfo"]["contact"]["profile"]["displayName"]
                message_command_params = format_command(message_command)
                if message_sender in running_bots:
                    running_bots[message_sender].send_bot_command(message_command_params)
                else:
                    running_bots[message_sender] = SimplexBot(message_sender, ws)
                    running_bots[message_sender].send_bot_command(message_command_params)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def run_websocket():
    ws.run_forever()

# create WebSocket-App
ws = websocket.WebSocketApp(
    "ws://localhost:3030", # Default websocket if started with starting script
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# run WebSocket in a thread
ws_thread = threading.Thread(target=run_websocket)
ws_thread.daemon = True  # thread gets terminated if main script gets terminated
ws_thread.start()

# wait until connection is established
time.sleep(1)

# Bot loop. Just listen for some exit command
try:
    while True:
        print("Enter command (or 'exit' to close): ")
        command = input().lower()
        match command:
            case "exit":
                break
            case "help": 
                print("exit: stops bots and quits") 
                print("help: shows this screen")
                print("list: lists all running bots")
            case "list":
                print("Bots running for:")
                print(*list(running_bots.keys()), sep="\n")
            #ToDo: add more control commands as desired (don't forget to update the "help" command ;) )
except KeyboardInterrupt:
    pass
finally:
    # Closing connection
    ws.close()
    ws_thread.join()
    for k in running_bots:
        running_bots[k].stop_bot()
