# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 16:02:38 2018

@author: ssc
"""
import logging
botLog = logging.getLogger('BotLog')

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi

class MatrixBot:
    def __init__(self, username, password, server, roomId):
        self.username = username

        # Connect to server
        botLog.debug("creating matrix client for server {}".format( server))
        self.client = MatrixClient(server)
        try:
            botLog.debug("Trying to log in as {} pw: {}".format(username, "".join(['*' for p in password])))
            self.token = self.client.login_with_password(username, password)
            botLog.debug("Got Token {}..{}".format( self.token[0:3], self.token[-3:-1]))
        except Exception as e:
            botLog.error("Login Failed: {}".format(e))
            return(None)
        #this is a second connection with different interface
        self.api = MatrixHttpApi(server, self.token)
        botLog.debug("Matrix API endpoint created")
        self.api.sync()
        botLog.debug("synced")
        if str(roomId).startswith('!'):            
            self.currentRoom = roomId
        else:
            self.currentRoom = self.getRoomIdByName(roomId)
        self.api.join_room(self.currentRoom)
        botLog.debug("Joined room with id {}".format( self.currentRoom))
        
        self.members = self.api.get_room_members(self.currentRoom)
        botLog.debug("Members in room: {}".format(",".join([a.sender for a in self.members['chunk']])))
        #self.rooms = 
        
    def getRoomIdByName(self, name):
        botLog.debug("Getting room ID for name '{}'".format(name))
        try:
            if str(name).startswith('#'):
                rid = self.api.get_room_id(name)
            else:
                rid = self.api.get_room_id('#' + name)
        except Exception as e:
            print("room name not found")
            rid = ""
        return rid
    
    def send(self, text):
        self.api.send_message(self.currentRoom, text)