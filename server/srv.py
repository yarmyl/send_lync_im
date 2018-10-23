#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import lync

def check_true_sip_data(str):
    if len(str.split('+++>')) == 2:
        return 1
    else:
        return 0

def check_true_user_data(str):
    if len(str.split('--->')) == 2:
        return 1
    else:
        return 0

def main():
    myLync = lync.Lync()
    sock = socket.socket()
    sock.bind(('', 1112))
    sock.listen(10)
    while True:
        conn, addr = sock.accept()
        conn.settimeout(5)
        try:
            data = conn.recv(2048).decode()
            print(data)
        except:
            print(addr[0] + " timeout or bad data")
        else:
            if check_true_user_data(data):
                if myLync.check(data.split('--->')[1]):
                    myLync.sendIm(data.split('--->')[1], data.split('--->')[0] +
                        " (Это сообщение было отправленно с сервера)")
                    conn.send(bytes("Success!", "utf8"))
                    print("Success!")
                else:
                    conn.send(bytes("Haven't user " + data.split('--->')[1], "utf8"))
                    print("Haven't user " + data.split('--->')[1])
            elif data == "print users":
                conn.send(bytes(myLync.users(), "utf8"))
                print("Success!")
            elif check_true_sip_data(data):
                myLync.sendIm(data.split('+++>')[1], data.split('+++>')[0] +
                    " (Это сообщение было отправленно с сервера)", 1)
                conn.send(bytes("Success!", "utf8"))
                print("Success!")
            else:
                conn.send(bytes("bad Data", "utf8"))
                print("bad Data")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
