#!/usr/bin/python
# Autor: Alexandre Mariano

import socket
import ConfigParser
import thread

config = ConfigParser.ConfigParser()
config.read("connection.ini")  # reading the config file

host = config.get('Section one', 'host')  # using the config file values
port = config.getint('Section one', 'port')

des = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating a socket object


def command(w):

    print ('Sending command...')
    s.sendto(w, des)
    print ('OK...')
    thread.start_new_thread(results, ())


def results():
    print ('Tread 2 - Waiting for results...')
    print ("Server Result: ", s.recv(1400))
    print ('### Select a option: ###')
    print ('### 1-Create data ###')
    print ('### 2-Retrieve data ###')
    print ('### 3-Update data ###')
    print ('### 4-Delete data ###')
    print ('')
    print ('### 0-Close connection ###')


z = 5
while z != '0':
    print ('### Select a option: ###')
    print ('### 1-Create data ###')
    print ('### 2-Retrieve data ###')
    print ('### 3-Update data ###')
    print ('### 4-Delete data ###')
    print ('')
    print ('### 0-Close connection ###')
    x = raw_input()
    print ('Enter with key, value')
    v = raw_input()
    w = x + '.' + v
    thread.start_new_thread(command, (w,))
s.close()
