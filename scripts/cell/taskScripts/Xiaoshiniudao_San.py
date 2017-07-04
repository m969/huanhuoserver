# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class Xiaoshiniudao_San(object):
    def __init__(self, owner, selfIndex, npcName, npcTaskIndex):
        DEBUG_MSG("Xiaoshiniudao_San:__init__")
        self.owner = owner
        self.selfIndex = selfIndex
        self.npcName = npcName
        self.npcTaskIndex = npcTaskIndex
        self.owner.setAttr("Xiaoshiniudao_San_TaskCounter", 0)
        self.oldTaskCounter = self.owner.getAttr("Xiaoshiniudao_San_TaskCounter")

    def detectTaskCompleteness(self):
        if self.owner.getAttr("Xiaoshiniudao_San_TaskCounter") - self.oldTaskCounter >= 1:
            self.owner.setTaskFinish(self.npcName, self.npcTaskIndex, self.selfIndex)
