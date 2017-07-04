# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from interfaces.EntityObject import EntityObject
import monster_data
import npc_data
import space_data
from triggerStrategies.onEnterTrap.TriggerStrategy import *

class Space(KBEngine.Entity, EntityObject):
    """
    游戏场景，在这里代表野外大地图
    """

    def __init__(self):
        KBEngine.Entity.__init__(self)
        EntityObject.__init__(self)
        DEBUG_MSG("Space:cell:__init__ " + str(self.spaceID) + " " + str(self.id) + " " + self.spaceName)
        self.npcList = {}
        KBEngine.globalData["space_%i" % self.spaceID] = self.base
        KBEngine.globalData["space_" + self.spaceName] = self.base
        KBEngine.globalData["space_cell_%i" % self.spaceID] = self
        KBEngine.globalData["space_cell_" + self.spaceName] = self

        self.spaceData = space_data.data[self.name]     # 取出自身的场景数据

        self.respawnPoint = self.spaceData["重生点"]

        self.addTimer(0, 2, 0)    # 怪物生成定时器 每2秒生成5个
        self.monsterSpawnCounter = {}
        self.monsterSpawnPositionList = self.spaceData["怪物数据"]       # 怪物出生点列表
        for monsterName, monsterSpawnPositionList in self.monsterSpawnPositionList.items():
            self.monsterSpawnCounter[monsterName] = 0

        self.npcsData = self.spaceData["Npc数据"]      # 取出场景Npc数据
        for npcName, npcData in self.npcsData.items():
            self.npcList[npcName] = KBEngine.createEntity("Npc",
                                                          self.spaceID,
                                                          npcData["坐标"],
                                                          (0.0, 0.0, 0.0),
                                                          {
                                                              "npcID": npcData["id"],
                                                              "name": npcName,
                                                              "entityName": npcName,
                                                              'modelName': npcData["模型名称"]
                                                          })     # 创建Npc

        self.triggerData = self.spaceData["触发器数据"]      # 取出场景触发器数据
        for triggerData in self.triggerData.values():
            exec("self.triggerStrategy = " + triggerData["触发器类型"] + "Strategy()")
            DEBUG_MSG(self.triggerStrategy)
            self.triggerStrategy.setData(triggerData)
            trigger = KBEngine.createEntity("Trigger",
                                            self.spaceID,
                                            triggerData["触发器坐标"],
                                            (0.0, 0.0, 0.0),
                                            {
                                                'name': "GateWayTrigger",
                                                'lifeSpans': 0,
                                                'triggerSize': 4,
                                                "triggerStrategy": self.triggerStrategy
                                            })     # 创建触发器

    def onDestroy(self):
        """
        KBEngine method.
        """
        del KBEngine.globalData["space_%i" % self.spaceID]
        del KBEngine.globalData["space_" + self.spaceName]
        self.destroySpace()

    def onEnter(self, entityMailbox):
        """
        defined method.
        进入场景
        """
        DEBUG_MSG('Space::onEnter space[%d] entityID = %i.' % (self.spaceID, entityMailbox.id))
        entityMailbox.cell.onAvatarEnterSpace(self.spaceID, space_data.data[self.name]["场景名称"])

    def onNpcEnter(self, npcMailbox):
        DEBUG_MSG("Space:onNpcEnter")
        # self.npcList[npcMailbox.getAttr("entityName")] = npcMailbox

    def onTimer(self, timerHandle, userData):
        if userData is 0:
            finishCounter = 0
            for (monsterName, spawnPositionList) in self.monsterSpawnPositionList.items():
                tempCounter = 0
                counter = self.monsterSpawnCounter[monsterName]
                for position in spawnPositionList:
                    if counter >= len(spawnPositionList):
                        finishCounter += 1
                        break
                    else:
                        monster = KBEngine.createEntity(
                                                        "Monster",
                                                        self.spaceID,
                                                        spawnPositionList[counter],
                                                        (0.0, 0.0, 0.0),
                                                        {
                                                            "name": monsterName,
                                                            'entityName': monsterName,
                                                            'modelName': monster_data.data[monsterName]["模型名称"]
                                                        })      # 创建Monster
                        monster.receiveSpawnPos(spawnPositionList[counter])
                        if tempCounter >= 5:
                            break
                        counter += 1
                        tempCounter += 1
                        self.monsterSpawnCounter[monsterName] = counter
            if finishCounter >= len(self.monsterSpawnPositionList):
                self.delTimer(timerHandle)

    def requestNpc(self, npcName):
        DEBUG_MSG("Space:requestNpc")
        DEBUG_MSG(self.npcList)
        if npcName in self.npcList:
            return self.npcList[npcName]
        else:
            DEBUG_MSG("No this Npc")

    def onLeave(self, entityID):
        """
        defined method.
        离开场景
        """
        DEBUG_MSG('Space::onLeave space entityID = %i.' % (entityID))

    def monsterReborn(self, spawnPos, name):
        """
        重生怪物
        :param monsterMailbox:
        :return:
        """
        DEBUG_MSG("Space:monsterReborn")
        #重生怪物
        monster = KBEngine.createEntity("Monster", self.spaceID, spawnPos, (0.0, 0.0, 0.0),
                                            {
                                                "name": name,
                                                'entityName': name
                                            })
        monster.receiveSpawnPos(spawnPos)


