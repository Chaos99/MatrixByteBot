# -*- coding: utf-8 -*-
"""
Plugin to do maintenance tasks and show general info
about the bot.
"""

import re
import logging
import datetime

from plugin import Plugin

MTN_LOG = logging.getLogger('MaintenancePluginLog')

class MaintenancePlugin(Plugin):
    """Show general bot info like version, uptime, plugin list"""

    def __init__(self, name, bot):
        MTN_LOG.debug("Creating MaintenancePlugin")
        Plugin.__init__(self, name, bot)
        MTN_LOG.debug("Adding matcher for '![Vv]ersion'")
        Plugin.add_matcher(self, re.compile("![Vv]ersion"))
        Plugin.add_matcher(self, re.compile("![Ll]ist"))
        Plugin.add_matcher(self, re.compile("![Uu]ptime"))

        self.bot = bot #safe for later use
        self.first_run = True
        self.plugin_names = ""

        self.version = "no version set"

        self.start_time = datetime.datetime.now()

    def collect_plugins(self):
        """traverse plugin list in bot an get names"""
        if not self.first_run:
            pass
        else:
            for plugin in self.bot.plugins:
                self.plugin_names += (plugin.name + '\n')
            self.first_run = False
        return self.plugin_names

    def get_version(self):
        """ get version number from topmost entry in CHANGELOG.mf"""
        if not self.first_run:
            pass
        else:
            pattern = re.compile(r'##\s*(.*)')
            for line in open('CHANGELOG.md'):
                match = re.match(pattern, line)
                if match is not None:
                    self.version = match.group(1)
                    break #stop at first match
        return self.version

    def get_uptime(self):
        """ calculate uotime since start"""
        uptime = datetime.datetime.now() - self.start_time
        return str(uptime)

    def callback(self, room, event):
        """ collect info based on input match"""
        MTN_LOG.debug("%s sends response", self.name)
        if re.compile("![Vv]ersion").match(event['content']['body']):
            room.send_text(self.get_version())
        if re.compile("![Ll]ist").match(event['content']['body']):
            room.send_text(self.collect_plugins())
        if re.compile("![Uu]ptime").match(event['content']['body']):
            room.send_text(self.get_uptime())

    def get_help(self):
        """Return help text"""
        return ("Returns version info on !version\n"
                "Lists available plugins on !list\n"
                "Reports time since last startup with !uptime\n")
