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
from datesplugin import DatesPlugin
from statusplugin import StatusPlugin

# logging configuration
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PluginLog").setLevel(logging.WARNING)
logging.getLogger("schedule").setLevel(logging.WARNING)

MAIN_LOG = logging.getLogger('MainLog')

USERNAME = ""  # Bot's username (see private_settings.py)
PASSWORD = ""  # Bot's password (see private_settings.py)
SERVER = ""  # Matrix server URL (see private_settings.py)
ROOM = "" # Room name (see private_settings.py)

# import username, password, server and room name from external file
try:
    from private_settings import PASSWORD, USERNAME, SERVER, ROOM
except ImportError:
    pass


def main():
    """Main function to start the bot, add plugins and start listening loop"""
    # Create an instance of the MatrixBotAPI
    MAIN_LOG.debug("main() started, trying to initialize")
    MAIN_LOG.debug("MatrixBot initializing with room %s", ROOM)
    bot = MatrixBot(USERNAME, PASSWORD, SERVER, ROOM)

    # Add plugins to the bot
    bot.add_plugin(HiPlugin("SayHi-Plugin", bot))
    bot.add_plugin(HelpPlugin("Help-Plugin", bot))
    bot.add_plugin(MaintenancePlugin("Maintenance-Plugin", bot))
    bot.add_plugin(DatesPlugin("Dates-Plugin", bot))
    bot.add_plugin(StatusPlugin("Status-Plugin", bot))

    bot.register_listeners()

    # Start polling
    bot.start_polling()

    bot.send("Startup successful")

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        serial = input()
        print(serial)
        if 'q' in serial:
            bot.all_rooms.send_text("I was summond back to the workbech. Bye!")
            break
        if 'u' in serial:
            bot.all_rooms.send_text("I'm sensing an upstream update, be right back.")
            break

    bot.stop_scheduler()
    quit()

if __name__ == "__main__":
    main()
