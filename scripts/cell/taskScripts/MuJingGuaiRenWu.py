# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class MuJingGuaiRenWu(object):
    def __init__(self, owner, selfIndex, npcName, npcTaskIndex):
        DEBUG_MSG("MuJingGuaiRenWu:__init__")
        self.owner = owner
        self.selfIndex = selfIndex
        self.npcName = npcName
        self.npcTaskIndex = npcTaskIndex
        self.owner.setAttr("MuJingGuai_TaskCounter", 0)
        self.oldTaskCounter = self.owner.getAttr("MuJingGuai_TaskCounter")

    def detectTaskCompleteness(self):
        if self.owner.getAttr("MuJingGuai_TaskCounter") - self.oldTaskCounter >= 2:
            self.owner.setTaskFinish(self.npcName, self.npcTaskIndex, self.selfIndex)
