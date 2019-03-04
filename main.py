"""
A test bot using the Python Matrix Bot API

Test it out by adding it to a group chat and doing one of the following:
1. Say "Hi"
2. Say !echo this is a test!
3. Say !d6 to get a random size-sided die roll result
"""

import logging
from configparser import ConfigParser
import os

from matrixbot import MatrixBot

from plugins.hiplugin import HiPlugin
from plugins.helpplugin import HelpPlugin
from plugins.maintenanceplugin import MaintenancePlugin
from plugins.datesplugin import DatesPlugin
from plugins.statusplugin import StatusPlugin


# logging configuration
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PluginLog").setLevel(logging.WARNING)
logging.getLogger("schedule").setLevel(logging.WARNING)

MAIN_LOG = logging.getLogger('MainLog')

CONFIG = ConfigParser(comment_prefixes=(';'), interpolation=None)
if not CONFIG.read('config/config.ini'):
    raise ValueError("No config file found at config/config.ini")

def main():
    """Main function to start the bot, add plugins and start listening loop"""
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    # Create an instance of the MatrixBotAPI
    MAIN_LOG.debug("main() started, trying to initialize")
    MAIN_LOG.debug("MatrixBot initializing with room %s", CONFIG['bot']['room'])
    bot = MatrixBot(CONFIG)
    bot.init_scheduler()

    bot.connect()

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
