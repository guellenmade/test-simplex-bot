# why this fork?
I am bored :)



# Original readme:

# simplex-bot-playground
A playground that can be used as a basis for developing [simplex](https://simplex.chat/) bots.

Please report bugs, problems, ideas and bad coding ;)

Have fun!


## Usage
Install SimpleX CLI and generate profile as described [here](https://simplex.chat/docs/cli.html).\
Don't forget to generate an invitation and use it with your default profile.

Start SimpleX in websocked mode with the command:\
`simplex-chat -p 3030`\
or use the `start_simplex_websocket.sh` script in the repository.

Modify the `simplex_bot.py` as desired. Interesting parts for modification are marked with a `ToDo`.\
Start the bot using:\
`python3 simplex_bot_coordinator.py`\
or using the `start_simplex_bot.sh` script in the repository.

## Features
- Basic send and receive logic
- (Stateful) multiuser support

## Upcomming features
- ScheduledFunctions: Call a function at a date and time
- RepetitiveFunctions: Call a function every x timesteps
- RepetitiveFunctions

## Currently working on
- TimedFunctions: Call a function after a timer passed