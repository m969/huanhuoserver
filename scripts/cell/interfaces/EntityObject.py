# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from taskScripts.YanShiLingGuaiRenWu import YanShiLingGuaiRenWu


class EntityObject:
    def __init__(self):
        #DEBUG_MSG("EntityObject:__init__")
        pass

    def hasAttr(self, attr):
        # DEBUG_MSG("hasAttr : " + attr)
        return hasattr(self, attr)

    def getAttr(self, attr):
        # DEBUG_MSG("getAttr : " + attr)
        return getattr(self, attr, None)
        # if hasattr(self, attr):
        #     return getattr(self, attr)
        # else:
        #     return None

    def setAttr(self, attr, value):
        # exec("setattr(self, "+ "'" + attr + "'" + ", " + valueStr + ")")
        # exec("DEBUG_MSG(self."+attr+")")
        if hasattr(self, attr):
            setattr(self, attr, value)
        else:
            exec("self." + attr + "= value")
        # exec("DEBUG_MSG(self."+attr+")")
        DEBUG_MSG("setAttr:" + attr + "=" + str(value))

    def delAttr(self, attr):
        DEBUG_MSG("delAttr : " + attr)
        return delattr(self, attr)

    def hasTag(self, tag):
        # DEBUG_MSG("hasTag : " + tag)
        return hasattr(self, tag)

    def setTag(self, tag):
        if hasattr(self, tag):
            DEBUG_MSG("already hasTag : " + tag)
        else:
            DEBUG_MSG("on give tag : " + tag)
            exec("self." + tag + "= True")

    def isAvatar(self):
        return False

    def isMonster(self):
        return False

    def isNpc(self):
        return False

    def isTrigger(self):
        return False

    def isCombatEntity(self):
        return False

    def getEntityID(self):
        return self.id

    def getDatabaseID(self):
        return self.base.getDatabaseID()

    def getScriptName(self):
        return self.__class__.__name__

    def getCurrSpaceBase(self):
        """
        获得当前space的entity baseMailbox
        """
        return KBEngine.globalData["space_%i" % self.spaceID]

    def getCurrSpace(self):
        """
        获得当前space的entity
        """
        spaceBase = self.getCurrSpaceBase()
        return KBEngine.entities.get(spaceBase.id, None)

    def getSpaces(self):
        """
        获取场景管理器
        """
        return KBEngine.globalData["Spaces"]
