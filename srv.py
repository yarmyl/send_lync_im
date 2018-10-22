#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import dbus

def check_true_data(str):
    if str.split('--->')[1]:
        return 1
    else:
        print("bad data " + str)
        return 0

def sendIm(buddy, message, purple):
    conversationId = purple.PurpleConversationNew(1, buddy["accountId"], buddy["name"])
    imId = purple.PurpleConvIm(conversationId)
    purple.PurpleConvImSend(imId, message)

def main():
    bus = dbus.SessionBus()
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
    accounts = purple.PurpleAccountsGetAll()
    buddies = {}
    for accountId in accounts:
        buddyIds = purple.PurpleFindBuddies(accountId, "")
        for buddyId in buddyIds:
            buddy = {
                "id": buddyId,
                "name": purple.PurpleBuddyGetName(buddyId),
                "alias": purple.PurpleBuddyGetAlias(buddyId),
                "accountId": accountId
            }
            buddies[buddy["alias"]] = buddy

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
            if check_true_data(data):
                if buddies.get(data.split('--->')[1]):
                    sendIm(buddies[data.split('--->')[1]], data.split('--->')[0] +
                        " (Это сообщение было отправленно с сервера)", purple)
                    print("Success!")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
