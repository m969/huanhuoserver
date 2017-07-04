# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class TanxianshandongRenWu(object):
    def __init__(self, owner, selfIndex, npcName, npcTaskIndex):
        DEBUG_MSG("TanxianshandongRenWu:__init__")
        self.owner = owner
        self.selfIndex = selfIndex
        self.npcName = npcName
        self.npcTaskIndex = npcTaskIndex
        self.owner.setAttr("TanxianshandongRenWu_TaskCounter", 0)
        self.oldTaskCounter = self.owner.getAttr("TanxianshandongRenWu_TaskCounter")

    def detectTaskCompleteness(self):
        if self.owner.getAttr("TanxianshandongRenWu_TaskCounter") - self.oldTaskCounter >= 1:
            self.owner.setTaskFinish(self.npcName, self.npcTaskIndex, self.selfIndex)
