# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class BigWorld(KBEngine.Base):
    def __init__(self):
        DEBUG_MSG("BigWorld:__init__")
        KBEngine.Base.__init__(self)
        self.createInNewSpace(None)
        KBEngine.globalData["BigWorld"] = self

    def onGetCell(self):
        DEBUG_MSG("BigWorld:onGetCell")
        self.npcList = {}
        if self.xinShouYinDaoDBID == 0 or self.xinShouYinDaoDBID is None:
            self.npcList["新手引导"] = KBEngine.createBaseLocally("Npc", {})
            if self.npcList["新手引导"]:
                self.npcList["新手引导"].cellData["entityName"] = "新手引导"
                self.npcList["新手引导"].cellData["modelName"] = "XinShouYinDaoNpc"
                self.npcList["新手引导"].cellData["position"] = (202.0, 0.0, 253.0)
                self.npcList["新手引导"].cellData["direction"] = (0.0, 0.0, 0.0)
                self.npcList["新手引导"].setAttr("spaceCell", self.cell)
                self.npcList["新手引导"].setAttr("entityName", "新手引导")
                self.npcList["新手引导"].writeToDB(self._onNpcSaved)
        else:
            KBEngine.createBaseFromDBID("Npc", self.xinShouYinDaoDBID, self.__onNpcCreateCB)

    def __onNpcCreateCB(self, baseRef, dbid, wasActive):
        DEBUG_MSG("BigWorld:__onNpcCreateCB")
        self.npcList["新手引导"] = baseRef
        self.npcList["新手引导"].cellData["entityName"] = "新手引导"
        self.npcList["新手引导"].cellData["modelName"] = "XinShouYinDaoNpc"
        self.npcList["新手引导"].cellData["position"] = (202.0, 0.0, 253.0)
        self.npcList["新手引导"].cellData["direction"] = (0.0, 180.0, 0.0)
        self.npcList["新手引导"].setAttr("spaceCell", self.cell)
        self.npcList["新手引导"].setAttr("entityName", "新手引导")
        pass

    def _onNpcSaved(self, success, npc):
        DEBUG_MSG("BigWorld:_onNpcSaved")
        if npc.getAttr("entityName") == "新手引导":
            self.xinShouYinDaoDBID = npc.databaseID
        self.writeToDB(self.__onBigWorldSaved)

    def __onBigWorldSaved(self, success, base):
        DEBUG_MSG("__onBigWorldSaved")

    def loginSpace(self, entityMailbox):
        DEBUG_MSG("loginSpace")
        if entityMailbox.cell is None:
            entityMailbox.createCell(self.cell)
        self.onEnter(entityMailbox)

    def onEnter(self, entityMailbox):
        DEBUG_MSG("BigWorld:onEnter")
        if self.cell is not None:
            self.cell.onEnter(entityMailbox)
