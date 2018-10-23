#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dbus


class Lync:

    def sendIm(self, name, message, sip=0):
        if not sip:
            buddy = self.__buddies[name]
            name = buddy["name"]
            acc = buddy["accountId"]
        else:
            acc = self.__acc
        conversationId = self.__purple.PurpleConversationNew(1, acc, name)
        imId = self.__purple.PurpleConvIm(conversationId)
        self.__purple.PurpleConvImSend(imId, message)

    def __init__(self):
        bus = dbus.SessionBus()
        obj = bus.get_object("im.pidgin.purple.PurpleService",
            "/im/pidgin/purple/PurpleObject")
        self.__purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
        accounts = self.__purple.PurpleAccountsGetAll()
        self.__buddies = {}
        self.__acc = ""
        for accountId in accounts:
            self.__acc = accountId
            buddyIds = self.__purple.PurpleFindBuddies(accountId, "")
            for buddyId in buddyIds:
                buddy = {
                    "id": buddyId,
                    "name": self.__purple.PurpleBuddyGetName(buddyId),
                    "alias": self.__purple.PurpleBuddyGetAlias(buddyId),
                    "accountId": accountId
                }
                self.__buddies[buddy["alias"]] = buddy

    def check(self, name):
        if self.__buddies.get(name):
            return 1
        else:
            return 0

    def users(self):
        ret = ""
        for user in self.__buddies:
            ret = ret + user + '\n'
        return ret[:-1]
