#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import argparse

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mess', nargs='?') # сообщение
    parser.add_argument('--to', nargs='?') # адресат
    parser.add_argument('--srv', nargs='?') # сервер
    parser.add_argument('--users', action='store_true') # список пользователей
    parser.add_argument('--sip', nargs='?') # по sip
    return parser

def send_mess(srv, mess):
    sock = socket.socket()
    sock.connect((srv, 1112))
    sock.send(bytes(mess, "utf8"))
    data = sock.recv(2048)
    sock.close()
    return data.decode()


def main():
    parser = createParser()
    namespace = parser.parse_args()
    if namespace.srv:
        srv = namespace.srv
    else:
        srv = '127.0.0.1'
    if namespace.users:
        print(send_mess(srv, "print users"))
    elif namespace.mess:
        if namespace.to:
            print(send_mess(srv, namespace.mess + '--->' + namespace.to))
        elif namespace.sip:
            print(send_mess(srv, namespace.mess + '+++>' + namespace.sip))
        else:
            print("Bad type!")
    else:
        print("Bad type!")

if __name__ == "__main__":
    main()
