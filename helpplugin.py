# -*- coding: utf-8 -*-
"""
Plugin that collects help messages
from all other plugins and displays them
"""

import re
import logging

from plugin import Plugin

HELP_LOG = logging.getLogger('HelpPluginLog')

class HelpPlugin(Plugin):
    """Collects help messages
    from all other plugins and displays them"""

    def __init__(self, name, bot):
        HELP_LOG.debug("Creating HelpPlugin")
        Plugin.__init__(self, name, bot)
        HELP_LOG.debug("Adding matcher for '!Help'")
        Plugin.add_matcher(self, re.compile("![Hh]elp"))
        Plugin.add_matcher(self, re.compile("![Aa]bout"))

        self.bot = bot #safe for later use
        self.help_text = ""
        self.first_run = True

    def collect_help(self):
        """collect help messages from all plugins in the bot's list
        if called for the first time; else return cached value"""

        if not self.first_run:
            pass #already cached
        else:
            for plugin in self.bot.plugins:
                HELP_LOG.debug("Adding help text for %s", plugin.name)
                self.help_text += ('**' + plugin.name + '**\n')
                self.help_text += (plugin.get_help() + '\n')
                self.help_text += "\n"
            self.first_run = False

        return self.help_text

    @staticmethod
    def get_about():
        text = ("MatrixByteBot by @Chaos:erfurt.chat\n"
                "GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html)\n"
                "Sources at https://github.com/Chaos99/MatrixByteBot\n"
                "This is an alpha version with just partial functionality and a lot of bugs!\n"
                "\n Please use Github to submit bug reports or feature requests.")
        return text

    def callback(self, room, event):
        """send collected help messages"""
        HELP_LOG.debug("%s sends response", self.name)
        if re.compile("![Aa]bout").match(event['content']['body']):
            room.send_text(self.get_about())
        else:
            room.send_text(self.collect_help())

    @staticmethod
    def get_help():
        """Return help text"""
        return ("Prints this help text on !help\n"
                "and some meta info on !about")
