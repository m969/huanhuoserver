# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class Bangzhushenmiren(object):
    def __init__(self, owner, selfIndex, npcName, npcTaskIndex):
        DEBUG_MSG("Bangzhushenmiren:__init__")
        self.owner = owner
        self.selfIndex = selfIndex
        self.npcName = npcName
        self.npcTaskIndex = npcTaskIndex
        self.owner.setAttr("Bangzhushenmiren_TaskCounter", 1)
        self.oldTaskCounter = self.owner.getAttr("Bangzhushenmiren_TaskCounter")

    def detectTaskCompleteness(self):
        self.owner.setAttr("Bangzhushenmiren_TaskCounter", 0)
        if self.owner.getAttr("Bangzhushenmiren_TaskCounter") == 0:
            self.owner.setTaskFinish(self.npcName, self.npcTaskIndex, self.selfIndex)
