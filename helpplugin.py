# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 01:05:57 2018

@author: ssc
"""

import re, logging
helpLog = logging.getLogger('HelpPluginLog')

from plugin import Plugin

class HelpPlugin(Plugin):
    def __init__(self, name, bot):
        helpLog.debug("Creating HelpPlugin")
        Plugin.__init__(self, name, bot)
        helpLog.debug("Adding matcher for '!Help'")
        Plugin.addMatcher(self, re.compile("![Hh]elp"))
        
        self.bot=bot #safe for later use
        self.helptext=""
        self.firstrun = True
        
    def collectHelp(self):
        if not self.firstrun:
            return self.helptext
        else:
            for plugin in self.bot.plugins:
                helpLog.debug("Adding help text for {}".format(plugin.name))
                self.helptext += ('**' + plugin.name + '**\n')
                self.helptext += (plugin.getHelp() + '\n')
                self.helptext += "\n"
            self.firstrun = False
            return self.helptext            
        
    def callback(self, room, event):
         # Somebody said hi, let's say Hi back
         helpLog.debug("{} sends response".format(self.name))
         room.send_text(self.collectHelp())
     
    def getHelp(self):
        return("Prints this help text on !help")
     
