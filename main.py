"""
A test bot using the Python Matrix Bot API

Test it out by adding it to a group chat and doing one of the following:
1. Say "Hi"
2. Say !echo this is a test!
3. Say !d6 to get a random size-sided die roll result
"""

import logging

from matrixbot import MatrixBot

from hiplugin import HiPlugin
from helpplugin import HelpPlugin
from maintenanceplugin import MaintenancePlugin

# logging configuration
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

MAIN_LOG = logging.getLogger('MainLog')

# Global variables
USERNAME = "MatrixBotAlpha"  # Bot's username
PASSWORD = ""  # Bot's password
SERVER = "https://erfurt.chat"  # Matrix server URL
ROOM = "#bot_test:erfurt.chat"

try:
    from private_settings import PASSWORD
except ImportError:
    pass


def main():
    """Main function to start the bot, add plugins and start listening loop"""
    # Create an instance of the MatrixBotAPI
    MAIN_LOG.debug("main() started, trying to initialize")
    MAIN_LOG.debug("MatrixBot initializing with room %s", ROOM)
    bot = MatrixBot(USERNAME, PASSWORD, SERVER, ROOM)

    # Add a regex handler waiting for the word
    MAIN_LOG.debug("Creating HiPlugin")
    bot.add_plugin(HiPlugin("SayHi-Plugin", bot))
    bot.add_plugin(HelpPlugin("Help-Plugin", bot))
    bot.add_plugin(MaintenancePlugin("Maintenance-Plugin", bot))

    for room_id, room in bot.client.get_rooms().items():
        MAIN_LOG.debug("Registering plugins in room %s", room_id)
        for plugin in bot.plugins:
            room.add_listener(plugin.handle_message)

    # Start polling
    bot.start_polling()

    bot.send("Startup successful")

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        serial = input()
        print(serial)
        if 'q' in serial:
            break

    quit()

if __name__ == "__main__":
    main()
