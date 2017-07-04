# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class Sidingzhongsheng(object):
    def __init__(self, owner, selfIndex, npcName, npcTaskIndex):
        DEBUG_MSG("Sidingzhongsheng:__init__")
        self.owner = owner
        self.selfIndex = selfIndex
        self.npcName = npcName
        self.npcTaskIndex = npcTaskIndex
        self.owner.setAttr("Sidingzhongsheng_TaskCounter", 0)
        self.oldTaskCounter = self.owner.getAttr("Sidingzhongsheng_TaskCounter")
        # 给予任务者玉佩(18是玉佩id)
        self.owner.giveGoods(18)
        #将信给刘公子
        self.owner.deleteGoods(17)


    def detectTaskCompleteness(self):
        self.owner.setAttr("Sidingzhongsheng_TaskCounter", 0)
        if self.owner.getAttr("Sidingzhongsheng_TaskCounter") >= 0:
            self.owner.setTaskFinish(self.npcName, self.npcTaskIndex, self.selfIndex)
