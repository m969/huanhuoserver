# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from interfaces.CombatProperty import CombatProperty


class CombatEntity(CombatProperty):
    def __init__(self):
        CombatProperty.__init__(self)
        #DEBUG_MSG("CombatEntity:__init__")
        self.combatable = True

    def receiveDamage(self, attackerMailbox, damage):
        DEBUG_MSG("CombatEntity:receiveDamage")
        oldHP = self.HP
        if damage >= self.HP:
            self.HP = 0
        else:
            self.HP -= damage
        if oldHP != self.HP:
            self.onHPChange(attackerMailbox)

    def onHPChange(self, murderer):
        if self.HP <= 0:
            self.dieSelf(murderer)

    def dieSelf(self, murderer):
        # taskCounter = murderer.getAttr("taskCounter")
        # taskCounter += 1
        # murderer.setAttr("taskCounter", taskCounter)
        self.onDie(murderer)

    def onDie(self, murderer):
        DEBUG_MSG("CombatEntity:onDie")
        self.allClients.OnDie()
