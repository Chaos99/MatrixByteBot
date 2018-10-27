# -*- coding: utf-8 -*-
"""
Plugin to do maintenance tasks and show general info
about the bot.
"""

import re
import logging
import datetime

from .plugin import Plugin

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
        Plugin.add_matcher(self, re.compile("![Hh]istory"))

        self.bot = bot #safe for later use
        self.first_run = {'plugins':True,
                          'version':True,
                          'history':True}

        self.plugin_names = "names could not be read"
        self.version = "no version set"
        self.history = "history could not be read"

        self.start_time = datetime.datetime.now()

    def collect_plugins(self):
        """traverse plugin list in bot an get names"""
        if not self.first_run['plugins']:
            pass
        else:
            self.plugin_names = ""
            for plugin in self.bot.plugins:
                self.plugin_names += (plugin.name + '\n')
            self.first_run['plugins'] = False
        return self.plugin_names

    def get_version(self):
        """ get version number from topmost entry in CHANGELOG.mf"""
        if not self.first_run['version']:
            pass
        else:
            pattern = re.compile(r'##\s*(.*)')
            for line in open('CHANGELOG.md'):
                match = re.match(pattern, line)
                if match is not None:
                    self.version = match.group(1)
                    break #stop at first match
            self.first_run['version'] = False
        return self.version

    def get_uptime(self):
        """ calculate uotime since start"""
        uptime = datetime.datetime.now() - self.start_time
        return str(uptime)

    def get_history(self):
        """ extract a few lines from the CHANGELOG file"""
        length = 9
        if not self.first_run['history']:
            pass
        else:
            pattern = re.compile(r'##\s*(.*)')
            with open('CHANGELOG.md') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if pattern.match(line):
                        upper_limit = i + length if ((i+length) < len(lines)) else (len(lines)-1)
                        MTN_LOG.debug("Found %s, printing lines %d to %d",
                                      line[:-1], i, upper_limit)
                        self.history = lines[i:upper_limit]
                        break #stop at first match
                self.first_run['history'] = False
        return "".join(self.history)

    def callback(self, room, event):
        """ collect info based on input match"""
        MTN_LOG.debug("%s sends response", self.name)
        if re.compile("![Vv]ersion").match(event['content']['body']):
            room.send_text(self.get_version())
        if re.compile("![Ll]ist").match(event['content']['body']):
            room.send_text(self.collect_plugins())
        if re.compile("![Uu]ptime").match(event['content']['body']):
            room.send_text(self.get_uptime())
        if re.compile("![Hh]istory").match(event['content']['body']):
            room.send_text(self.get_history())

    @staticmethod
    def get_help():
        """Return help text"""
        return ("Returns version info on !version\n"
                "Lists available plugins on !list\n"
                "Reports time since last startup with !uptime\n"
                "Give last few lines of changelog with !history")
