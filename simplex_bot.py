import websocket
import threading
import json
import time
import random

def on_open(ws):
    print("Connected")

def on_message(ws, message):
    # Bot command and response flow here
    message_converted = json.loads(message)
    if message_converted["resp"]["type"] == "newChatItems":
        if message_converted["resp"].get("chatItems"):
            if message_converted["resp"]["chatItems"][0]["chatItem"]["chatDir"]["type"] == "directRcv":
                message_command = message_converted["resp"]["chatItems"][0]["chatItem"]["content"]["msgContent"]["text"].lower()
                message_sender = message_converted["resp"]["chatItems"][0]["chatInfo"]["contact"]["profile"]["displayName"]
                match message_command:
                    case "help":
                        message = "Command a: Usage\n" \
                                "Command b: Usage\n" \
                                "...\n"
                    case _:
                        message = "Command not found. Try \"help\" "
                    #ToDo: add your bot commands here and handle their response logic

                corr_id = random.randint(0,100000)
                response = {
                    "corrId": f"{corr_id}",
                    "cmd": f"@{message_sender} {message}"
                }
                response_json = json.dumps(response)
                ws.send(response_json)

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
        command = input("Enter command: (or 'exit' to close): ").lower()
        match command:
            case "exit":
                break
            case "help": 
                print("List of commands and their funcionality") 
            #ToDo: add more control commands as desired (don't forget to update the "help" command ;) )
except KeyboardInterrupt:
    pass
finally:
    # Closing connection
    ws.close()
    ws_thread.join()