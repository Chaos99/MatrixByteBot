# -*- coding: utf-8 -*-
"""
Plugin that displays room status
"""

import re
import logging
from json import loads as json_loads
from json import JSONDecodeError

from urllib import request
from urllib.error import HTTPError, URLError

from .plugin import Plugin


STATUS_LOG = logging.getLogger('StatusPluginLog')

class StatusPlugin(Plugin):
    """Collects help messages
    from all other plugins and displays them"""

    def __init__(self, name, bot):
        STATUS_LOG.debug("Creating StatusPlugin")
        Plugin.__init__(self, name, bot)
        STATUS_LOG.debug("Adding matcher for '!status'")
        Plugin.add_matcher(self, re.compile("![sS]tatus"))
        Plugin.add_matcher(self, re.compile("![Uu]ser"))

        self.bot = bot #safe for later use
        self.help_text = ""
        self.first_run = True


    def callback(self, room, event):
        """send collected help messages"""
        STATUS_LOG.debug("%s sends response", self.name)
        if re.compile("![Ss]tatus").match(event['content']['body']):
            self.status(room)
        else:
            self.users(room)

    @staticmethod
    def get_help():
        """Return help text"""
        return ("Print room status with !status\n"
                "Print list of users in the space with !users")

    def status(self, room):
        """Returns the door status of the hackerspace rooms

            %%status
        """
        try:
            data = self.spaceapi(room)

            room.send_text('Space status:')
            if data['state']['open']:
                room.send_text('\tThe space is open!')
            else:
                room.send_text('\tThe space is closed!')
        except JSONDecodeError as error:
            STATUS_LOG.error(error)
            room.send_text('\tError while retrieving space status')


    def users(self, room):
        """Returns the current users inside the hackerspace rooms

            %%users
        """
        try:
            data = self.spaceapi(room)
            data = data['sensors']['people_now_present'][0]

            if data['value'] > 0:
                room.send_text('Space users: ' + str(', '.join(data['names'])))
            elif data['value'] == 0:
                room.send_text('Nobody is logged into teh space :(')
            else:
                room.send_text("I'm not sure if anyone's in the space")
        except JSONDecodeError as error:
            STATUS_LOG.error(error)
            room.send_text('\tError while retrieving user data')

    @staticmethod
    def spaceapi(room):
        ''' Download spacapi json and return decoded content'''
        url = "https://status.bytespeicher.org/status.json"
        try:
            #Request the status api file.
            #urllib may pose a security risk because it can open local files with file://
            #this is not a problem here as URLs are hardcoded/come from settings file
            req = request.Request(url) #nosec (disables security warning)
            with request.urlopen(req) as resp:
            # with request.urlopen(url if url.startswith("http") else "") as resp:
                STATUS_LOG.debug("URL requested")
                if resp.status == 200:
                    #Get text content from http request.
                    STATUS_LOG.debug("Get text")
                    r_raw = resp.read()
                    encoding = resp.headers.get_content_charset('utf-8')
                    text = r_raw.decode(encoding)
                else:
                    room.send_text("Error while retrieving calendar data")
                    raise Exception()
        except HTTPError as error:
            STATUS_LOG.error('HTTPError = %s', str(error.code))
            room.send_text("Error while retrieving calendar data\n"
                           'HTTPError = ' + str(error.code))
        except URLError as error:
            STATUS_LOG.error('URLError = %s', str(error.reason))
            room.send_text("Error while retrieving calendar data\n"
                           'URLError = ' + str(error.reason))

        return json_loads(text)
