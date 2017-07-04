# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class Qianlisongqing(object):
    def __init__(self, owner, selfIndex, npcName, npcTaskIndex):
        DEBUG_MSG("Qianlisongqing:__init__")
        self.owner = owner
        self.selfIndex = selfIndex
        self.npcName = npcName
        self.npcTaskIndex = npcTaskIndex
        self.owner.setAttr("Qianlisongqing_TaskCounter", 0)
        self.oldTaskCounter = self.owner.getAttr("Qianlisongqing_TaskCounter")
        # 给予任务者信(17是信id)
        self.owner.giveGoods(17)


    def detectTaskCompleteness(self):
        #self.owner.setAttr("Qianlisongqing_TaskCounter", 0)
        if self.owner.getAttr("Qianlisongqing_TaskCounter") >= 1:
            self.owner.setTaskFinish(self.npcName, self.npcTaskIndex, self.selfIndex)
