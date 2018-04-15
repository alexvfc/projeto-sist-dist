# !/usr/bin/python
# Autor: Alexandre Mariano

import socket
import ConfigParser
import thread

config = ConfigParser.ConfigParser()
config.read("connection.ini")  # reading the config file

host = ''  # I AM THE HOST
port = config.getint('Section one', 'port')  # using the config file values

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating a socket object
orig = (host, port)
s.bind(orig)  # bind the host and the port

f = []  # queue for received commands
q = []  # queue for log in disk
p = []  # queue for process commands


# s.listen(10)

def worker(cli, fla):  # cli=host and port information fla, flag for crud
    if not f:
        print('Waiting for commands')
    else:
        print ('Saving in disk')
        temp = f.pop() # Retrieve the command and remove from older queue
        q.append(temp)  # Insert the command in disk log queue
        # process
        if fla == '1':  # if 1 try create element
            if p is None:  # queue empty
                p.append(temp)
            else:
                if temp in p:
                    s.sendto('Already exist!!!', cli)
                else:
                    p.append(temp)
                    s.sendto('Created with success!!!', cli)
        elif fla == '2':  # if 2 try retrieve element
            if p is None:
                s.sendto('Empty queue!!!', cli)
            else:
                if temp in p:
                    s.sendto(temp, cli)
                else:
                    s.sendto('Element not found!!!', cli)
        elif fla == '3':
            if p is None:
                s.sendto('Empty file!!!', cli)
            else:
                if temp in p:
                    p.remove(temp)
                    p.append(temp)
                    s.sendto('Element updated!', cli)
                else:
                    s.sendto('Key not found!!!', cli)
        elif fla == '4':
            if p is None:
                s.sendto('Empty file!!!', cli)
            else:
                if temp in p:
                    p.remove(p.index(temp))
                    s.sendto('Element removed' + e, cli)
                else:
                    s.sendto('Key not found', cli)

        # p.append(temp)  # Insert the command in consumer queue
        disk_file = open("server.txt", 'a')  # open file for write a command
        value = fla+' '+temp
        disk_file.writelines(value)  # Write the value in disk
        disk_file.write("\n")
        disk_file.close()  # Close the file
        print('Successful...')
        # worker
        s.sendto("Command received", cli)  # feedback client


def receiver(val, cli):  # val=values, cli=information about (IP, port), fla=flag
    fla, cont = val.split(".")
    print('Message received: ', cont)
    f.append(cont)
    print('Command inserted in Queue')

    thread.start_new_thread(worker, (cli, fla))


while True:
    rec, client = s.recvfrom(1400)
    print ("Received connection from: ", client)
    thread.start_new_thread(receiver, (rec, client))
