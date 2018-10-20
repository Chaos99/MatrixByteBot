# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 16:02:38 2018

@author: ssc
"""
from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi

class MatrixBot:
    def __init__(self, username, password, server, roomId):
        self.username = username

        # Connect to server
        self.client = MatrixClient(server)
        self.token = self.client.login_with_password(username, password)

        #this is a second connection with different interface
        self.api = MatrixHttpApi(server, self.token)
        self.api.sync()
        if str(roomId).startswith('!'):
            self.api.join_room(roomId)
            self.currentRoom = roomId
        else:
            self.api.join_room(self.getRoomIdByName(roomId))
            self.currentRoom = self.getRoomIdByName(roomId)
    
        self.members = self.api.get_room_members(self.currentRoom)
        #self.rooms = 
        
    def getRoomIdByName(self, name):
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