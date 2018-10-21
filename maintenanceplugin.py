# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 01:05:57 2018

@author: ssc
"""

import re, logging, datetime
mtnLog = logging.getLogger('MaintenancePluginLog')

from plugin import Plugin

class MaintenancePlugin(Plugin):
    def __init__(self, name, bot):
        mtnLog.debug("Creating MaintenancePlugin")
        Plugin.__init__(self, name, bot)
        mtnLog.debug("Adding matcher for '![Vv]ersion'")
        Plugin.addMatcher(self, re.compile("![Vv]ersion"))
        Plugin.addMatcher(self, re.compile("![Ll]ist"))
        Plugin.addMatcher(self, re.compile("![Uu]ptime"))
        
        self.bot=bot #safe for later use
        self.firstrun = True
        self.pluginnames = ""
        
        self.version = "0.1.4"
        
        self.starttime = datetime.datetime.now()
        
    def collectPlugins(self):
        if not self.firstrun:
            return self.pluginnames
        else:
            for plugin in self.bot.plugins:
                self.pluginnames += ( plugin.name + '\n')                
            self.firstrun = False
            return self.pluginnames  

    def getVersion(self):
        if not self.firstrun:
            return self.version
        else:
            pattern = re.compile('##\s*(.*)')
            for i, line in enumerate(open('CHANGELOG.md')):
                m = re.match(pattern, line)
                if m != None:
                    self.version = m.group(1)
                    return self.version
            return self.version #default if no match   
        
    def getUptime(self):
        uptime = datetime.datetime.now() - self.starttime
        return str(uptime)
        
    def callback(self, room, event):         
         mtnLog.debug("{} sends response".format(self.name))
         if re.compile("![Vv]ersion").match(event['content']['body']):
             room.send_text(self.getVersion())
         if re.compile("![Ll]ist").match(event['content']['body']):
             room.send_text(self.collectPlugins())
         if re.compile("![Uu]ptime").match(event['content']['body']):
             room.send_text(self.getUptime())
     
    def getHelp(self):
        return("Returns version info on !version\n"
               "Lists available plugins on !list\n"
               "Reports time since last startup with !uptime\n")
     
