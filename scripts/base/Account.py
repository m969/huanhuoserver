# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from DBID_LIST import TDBIDList


class Account(KBEngine.Proxy):
    def __init__(self):
        KBEngine.Proxy.__init__(self)

    def onTimer(self, id, userArg):
        """
        KBEngine method.
        使用addTimer后， 当时间到达则该接口被调用
        @param id		: addTimer 的返回值ID
        @param userArg	: addTimer 最后一个参数所给入的数据
        """
        DEBUG_MSG(id, userArg)

    def onEntitiesEnabled(self):
        """
        KBEngine method.
        该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
        cell部分。
        """
        DEBUG_MSG(self.avatarDBIDList)
        INFO_MSG("account[%i] entities enable. mailbox:%s" % (self.id, self.client))
        if self.avatarDBID == 0:
            self.avatar = KBEngine.createBaseLocally("Avatar", {})
            if self.avatar:
                self.avatar.accountEntity = self
                self.avatar.cellData["position"] = (211.4, 0.44, 253.6)
                self.avatar.cellData["direction"] = (0.0, 0.0, 0.0)
                self.avatar.cellData["entityName"] = self.__ACCOUNT_NAME__
                self.avatar.writeToDB(self._onAvatarSaved)
                self.giveClientTo(self.avatar)
        else:
            KBEngine.createBaseFromDBID("Avatar", self.avatarDBID, self.__onAvatarCreateCB)

    def __onAvatarCreateCB(self, baseRef, dbid, wasActive):
        DEBUG_MSG("__onAvatarCreateCB")
        if wasActive:
            ERROR_MSG("Account::__onAvatarCreated:(%i): this character is in world now!" % (self.id))
            return
        if baseRef is None:
            ERROR_MSG("Account::__onAvatarCreated:(%i): the character you wanted to created is not exist!" % (self.id))
            return

        avatar = KBEngine.entities.get(baseRef.id)
        if avatar is None:
            ERROR_MSG("Account::__onAvatarCreated:(%i): when character was created, it died as well!" % (self.id))
            return
        avatar.accountEntity = self
        avatar.setAvatarName(self.__ACCOUNT_NAME__)
        self.giveClientTo(avatar)

    def _onAvatarSaved(self, success, avatar):
        self.avatarDBID = self.avatar.databaseID
        self.writeToDB(self._onAccountSaved)

    def _onAccountSaved(self, success, account):
        pass

    def _onAccountSavedThenDestroy(self, success, account):
        self.destroy()

    def onDestroy(self):
        DEBUG_MSG("Account:onDestroy")

    def onLogOnAttempt(self, ip, port, password):
        """
        KBEngine method.
        客户端登陆失败时会回调到这里
        """
        INFO_MSG(ip, port, password)
        return KBEngine.LOG_ON_ACCEPT

    def onClientDeath(self):
        """
        KBEngine method.
        客户端对应实体已经销毁
        """
        DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
        self.destroy()

    def destroyAccount(self):
        self.writeToDB(self._onAccountSavedThenDestroy)
