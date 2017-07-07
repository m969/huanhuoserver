# -*- coding: utf-8 -*-
import KBEngine
import random
from KBEDebug import *
from interfaces.EntityObject import EntityObject
from interfaces.CombatEntity import CombatEntity
from interfaces.AI import AI
import monster_data
from triggerStrategies.onEnterTrap.TriggerStrategy import *


class Monster(KBEngine.Entity, EntityObject, CombatEntity, AI):
    def __init__(self):
        DEBUG_MSG("Monster::__init__")
        KBEngine.Entity.__init__(self)
        EntityObject.__init__(self)
        CombatEntity.__init__(self)
        AI.__init__(self)

        self.spawnPos = (0, 0, 0)
        self.timerMoveID = self.addTimer(0, 4, 1)
        self.monsterData = monster_data.data[self.name]
        self.modelName = self.monsterData["模型名称"]
        DEBUG_MSG("modelName is " + str(self.modelName))
        self.HP = self.monsterData["生命值"]
        self.HP_Max = self.monsterData["生命值"]
        self.killerTaskCounterVariableName = self.modelName + "_TaskCounter"

    def isMonster(self):
        return True

    def isCombatEntity(self):
        return True

    def onWitnessed(self, isWitnessed):
        pass

    def receiveDamage(self, attackerMailbox, damage):
        DEBUG_MSG("Monster:receiveDamage-%s" % damage)
        CombatEntity.receiveDamage(self, attackerMailbox, damage)
        DEBUG_MSG(attackerMailbox.getAttr("position"))

    def receiveSpawnPos(self, spawnPos):
        """
        接收BigWorld中的怪物出生点
        :param spawnPos:
        :return:
        """
        #DEBUG_MSG("Monster:receiveSpawnPos")
        self.spawnPos = spawnPos

    def onTimer(self, tid, userArg):
        AI.onTimer(self, tid, userArg)

    def onDie(self, murderer):
        #DEBUG_MSG("Monster:onDie")
        CombatEntity.onDie(self, murderer)
        if murderer.hasAttr(self.killerTaskCounterVariableName) is True:
            murderer.setAttr(self.killerTaskCounterVariableName,
                             murderer.getAttr(self.killerTaskCounterVariableName) + 1)
        else:
            murderer.setAttr(self.killerTaskCounterVariableName, 1)
        if murderer.hasAttr("Pobudeyi_TaskCounter") is True:
            murderer.setAttr("Pobudeyi_TaskCounter",
                             murderer.getAttr("Pobudeyi_TaskCounter") + 1)
        else:
            murderer.setAttr("Pobudeyi_TaskCounter", 1)
        self.delTimer(self.timerMoveID)
        self.destroy()

    def onDestroy(self):
        # KBEngine.globalData["BigWorld_Cell"].monsterReborn(self)
        KBEngine.globalData["space_%i" % self.spaceID].cell.monsterReborn(self.spawnPos, self.name)
        pass
