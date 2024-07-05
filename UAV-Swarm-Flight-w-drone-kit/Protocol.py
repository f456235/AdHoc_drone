from dronekit import connect, VehicleMode, LocationGlobalRelative
import dronekit
import json
import time
import sys
import math
from threading import Timer
from RepeatTimer import RepeatTimer
from datetime import datetime
import socket

class Protocol():
    '''
    0   latitude(:011.8f), 
        longitude(:012.8f),
        altitude(:06.2f), 
        time(minute+second, 4 chars)  34 chars (including "0" in the beginning)
    1   "TAKEOFF"                     1 char (only "1")
    2   "TOOKOFF"                     1 char (only "2")
    3   "LAND"                        1 char (only "3")
    4   "LANDED"                      1 char (only "4")
    '''
    def __init__(self, send_port=37020, recv_port=37021): #socket configuration , one for send and one for receive
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.recv_socket.settimeout(0.2)
        self.recv_socket.bind(('', recv_port))  # Bind to all interfaces on the receive port
        
        self.broadcast_ip = '192.168.4.255'
        self.send_port = send_port

    def sendMsg(self, msgName, vehicle=None): # send a UDP message to the client
        if msgName == "COORDINATES":
            lat = float(vehicle.location.global_frame.lat)
            lon = float(vehicle.location.global_frame.lon)
            alt = float(vehicle.location.global_relative_frame.alt)
            current_time = datetime.now().strftime("%M%S")          # This will turn the time into minute and second format, something like 0835 (08:35)
            # assert(lat <= 90 and lat >= -90)              
            # assert(lon <= 180 and lon >= -180)      
            # assert(alt < 100)                    # Assumes altitude below 100, if higher the message format requires adaptation
            msg = "0"+ str("{:011.8f}".format(lat)) + str("{:012.8f}".format(lon)) + str("{:06.2f}".format(alt)) + str(current_time)
        
        elif msgName in  ["TAKEOFF", "TOOKOFF", "LAND", "LANDED"]:
            msg = str(["TAKEOFF", "TOOKOFF", "LAND", "LANDED"].index(msgName) + 1)
        else:
            print("ERROR: Wrong Message Name:", msgName)
            return
        
        self.send_socket.sendto(msg.encode() , (self.broadcast_ip, self.send_port))
        print("Sent",msgName)

    def recvMsg(self):
        try: 
            msg, addr = self.recv_socket.recvfrom(1024)
            msgName = msg.decode()[0]
            print("Received Msg Name", msgName)
            if msgName == "0": # coordinates
                msg = msg.decode()[1:]
                # print("Received:",msg)
                lat = float(msg[0:11])
                lon = float(msg[11:23])
                alt = float(msg[23:29])
                recvTime = int(msg[31:33]) #only needs second
                # assert(lat <= 90 and lat >= -90)               
                # assert(lon <= 180 and lon >= -180)             
                # assert(alt < 100)                   # Assumes altitude below 100, if higher the message format requires adaptation
                return (lat, lon, alt, recvTime ,addr)
            elif msgName in ["1", "2", "3", "4"]: # return a tuple that states the message name and the address
                return (["TAKEOFF", "TOOKOFF", "LAND", "LANDED"][int(msgName)-1] ,addr)
        except socket.timeout:
            return (None,None)
            
            