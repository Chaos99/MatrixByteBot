"""
A test bot using the Python Matrix Bot API

Test it out by adding it to a group chat and doing one of the following:
1. Say "Hi"
2. Say !echo this is a test!
3. Say !d6 to get a random size-sided die roll result
"""

import random, logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

mainLog = logging.getLogger('MainLog')

from hiplugin import HiPlugin

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler

from matrixbot import MatrixBot

# Global variables
USERNAME = "MatrixBotAlpha"  # Bot's username
PASSWORD = ""  # Bot's password
SERVER = "https://erfurt.chat"  # Matrix server URL
ROOM = "#bot_test:erfurt.chat"

try:
   from private_settings import *
except ImportError:
   pass



def echo_callback(room, event):
    args = event['content']['body'].split()
    args.pop(0)

    # Echo what they said back
    room.send_text(' '.join(args))


def dieroll_callback(room, event):
    # someone wants a random number
    args = event['content']['body'].split()

    # we only care about the first arg, which has the die
    die = args[0]
    die_max = die[2:]

    # ensure the die is a positive integer
    if not die_max.isdigit():
        room.send_text('{} is not a positive number!'.format(die_max))
        return

    # and ensure it's a reasonable size, to prevent bot abuse
    die_max = int(die_max)
    if die_max <= 1 or die_max >= 1000:
        room.send_text('dice must be between 1 and 1000!')
        return

    # finally, send the result back
    result = random.randrange(1,die_max+1)
    room.send_text(str(result))


def main():
    # Create an instance of the MatrixBotAPI
    mainLog.debug("main() started, trying to initialize")
    mainLog.debug("MatrixBot initializing with room {}".format(ROOM))
    bot = MatrixBot(USERNAME, PASSWORD, SERVER, ROOM)

    # Add a regex handler waiting for the word 
    mainLog.debug("Creating HiPlugin")
    hiplug = HiPlugin("SayHi-Plugin", bot)
    
    for room_id, room in bot.client.get_rooms().items():
        mainLog.debug("Registering plugin in room {}".format(room_id))
        room.add_listener(hiplug.handle_message)
    
    # Start polling
    bot.start_polling()
    
    bot.send("Startup successful")

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        input()


if __name__ == "__main__":
    main()
