#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import argparse

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mess', nargs='?') # сообщение
    parser.add_argument('--to', nargs='?') # адресат
    parser.add_argument('--srv', nargs='?') # сервер
    return parser

def main():
    parser = createParser()
    namespace = parser.parse_args()
    if namespace.mess and namespace.to:
        if namespace.srv:
            srv = namespace.srv
        else:
            srv = '127.0.0.1'
        sock = socket.socket()
        sock.connect((srv, 1112))
        sock.send(bytes(namespace.mess + '--->' + namespace.to, "utf8"))
        data = sock.recv(2048)
        sock.close()
        print("Send message '" + namespace.mess + "' to " + namespace.to)
    else:
        print("Bad type!")

if __name__ == "__main__":
    main()
