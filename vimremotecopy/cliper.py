#!/usr/bin/python3
import socket
import os
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.bind(('192.168.69.182', 30000))
s.listen()

while True:
    c,addr = s.accept()
    content = c.recv(2048).decode('UTF-8')
    if content is not None:
        #print(content)
        os.system("echo -n '%s' | xclip -selection clipboard" % (content.strip()))
    c.close()
