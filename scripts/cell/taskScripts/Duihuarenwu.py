# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class Duihuarenwu(object):
    def __init__(self, owner, selfIndex, npcName, npcTaskIndex):
        DEBUG_MSG("Duihuarenwu:__init__")
        self.owner = owner
        self.selfIndex = selfIndex
        self.npcName = npcName
        self.npcTaskIndex = npcTaskIndex

    def detectTaskCompleteness(self):
        self.owner.setTaskFinish(self.npcName, self.npcTaskIndex, self.selfIndex)
