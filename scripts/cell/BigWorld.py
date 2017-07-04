# -*- coding: utf-8 -*-
import KBEngine, os, random, math, time, sys, Monster
from KBEDebug import *
from interfaces.EntityObject import EntityObject
import monster_data
import npc_data
import space_data


class BigWorld(KBEngine.Entity, EntityObject):
    def __init__(self):
        DEBUG_MSG("BigWorld:__init__")
        KBEngine.Entity.__init__(self)
        EntityObject.__init__(self)
        KBEngine.globalData["space_%i" % self.spaceID] = self.base
        KBEngine.globalData["BigWorld_Cell"] = self
        self.timerID = self.addTimer(2, 0.1, 0)
        # 创建传送门触发器
        # self.gateWayTrigger = KBEngine.createEntity("GateWayTrigger", self.spaceID, (10.0, 1.0, 10.0), (0.0, 0.0, 0.0), {})
        # 生成Npc
        self.npcList = {}
        # 木精怪的字典，大小为5
        self.muJingGuaiMonsters = {}
        # 岩石灵怪的字典，大小为5
        self.yanShiLingGuaiMonsters = {}
        # self.npcList["新手引导"] = KBEngine.createEntity("Npc", self.spaceID, (202.0, 0.0, 253.0), (0.0, 0.0, 0.0), {"entityName": "新手引导"})
        self.npcList["商人"] = KBEngine.createEntity("Npc", self.spaceID, (204.0, 0.0, 277.0), (0.0, 180.0, 0.0),
                                                   {"entityName": "商人", 'modelName': "StoreNpc"})
        # self.monsterSpawnPointData = monster_spawnpoint_data.data

        # MuJingGuai怪物的出生点
        self.spawnMuJingGuaiPos = space_data.data["木灵村"]["怪物数据"]["木精怪"]
        # yanShiLingGuai怪物的出生点
        self.spawnYanShiLingGuaiPos = space_data.data["木灵村"]["怪物数据"]["炎石灵怪"]

        # 生成木精怪怪物
        for x in self.spawnMuJingGuaiPos:
            self.muJingGuaiMonsters[x] = KBEngine.createEntity("Monster", self.spaceID, x, (0.0, 0.0, 0.0),
                                                               {'entityName': "木精怪", 'modelName': "MuJingGuai"})
            self.muJingGuaiMonsters[x].receiveSpawnPos(x)
            self.muJingGuaiMonsters[x].setAttr("killerTaskCounterVariableName", "MuJingGuai_TaskCounter")
        # 生成炎石灵怪怪物
        for x in self.spawnYanShiLingGuaiPos:
            self.yanShiLingGuaiMonsters[x] = KBEngine.createEntity("Monster", self.spaceID, x, (0.0, 0.0, 0.0),
                                                                   {'entityName': "炎石灵怪",
                                                                    'modelName': "YanShiLingGuai"})
            self.yanShiLingGuaiMonsters[x].receiveSpawnPos(x)
            self.yanShiLingGuaiMonsters[x].setAttr("killerTaskCounterVariableName", "YanShiLingGuai_TaskCounter")

    def onEnter(self, entityMailbox):
        DEBUG_MSG("BigWorld:onEnter - %s" % entityMailbox)

    def onNpcEnter(self, npcMailbox):
        DEBUG_MSG("BigWorld:onNpcEnter")
        # self.npcList[npcMailbox.getAttr("entityName")] = npcMailbox

    def onTimer(self, timerHandle, userData):
        if userData is not 0:
            return

    def requestNpc(self, npcName):
        DEBUG_MSG("BigWorld:requestNpc")
        if npcName in self.npcList:
            return self.npcList[npcName]

    def onLeave(self, avatarMailbox):
        DEBUG_MSG("BigWorld:onLeave")

    def onDestroy(self):
        pass

    def monsterReborn(self, monsterMailbox):
        """
        重生怪物
        :param monsterMailbox:
        :return:
        """
        DEBUG_MSG("BigWorld:monsterReborn")
        # 重生岩石精怪
        for x in self.spawnYanShiLingGuaiPos:
            if (self.yanShiLingGuaiMonsters[x].isDestroyed == True):
                self.yanShiLingGuaiMonsters[x] = KBEngine.createEntity("Monster", self.spaceID, x, (0.0, 0.0, 0.0),
                                                                       {'entityName': "炎石灵怪",
                                                                        'modelName': "YanShiLingGuai"})
                self.yanShiLingGuaiMonsters[x].receiveSpawnPos(x)
                self.yanShiLingGuaiMonsters[x].setAttr("killerTaskCounterVariableName", "YanShiLingGuai_TaskCounter")

        # 重生木灵怪
        for x in self.spawnMuJingGuaiPos:
            if (self.muJingGuaiMonsters[x].isDestroyed == True):
                self.muJingGuaiMonsters[x] = KBEngine.createEntity("Monster", self.spaceID, x, (0.0, 0.0, 0.0),
                                                                   {'entityName': "木精怪", 'modelName': "MuJingGuai"})
                self.muJingGuaiMonsters[x].receiveSpawnPos(x)
                self.muJingGuaiMonsters[x].setAttr("killerTaskCounterVariableName", "MuJingGuai_TaskCounter")
