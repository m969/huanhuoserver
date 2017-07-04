# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class YanShiLingGuaiRenWu(object):
    def __init__(self, owner, selfIndex, npcName, npcTaskIndex):
        """
        创建任务
        :param owner: 玩家
        :param selfIndex: 玩家任务里的索引
        :param npcName: npc的名字
        :param taskIndex: NPC中的任务索引
        """
        DEBUG_MSG("YanShiLingGuaiRenWu:__init__")
        self.owner = owner
        self.selfIndex = selfIndex
        self.npcName = npcName
        self.npcTaskIndex = npcTaskIndex
        self.owner.setAttr("YanShiLingGuai_TaskCounter", 0)
        self.oldTaskCounter = self.owner.getAttr("YanShiLingGuai_TaskCounter")

    def detectTaskCompleteness(self):
        if self.owner.getAttr("YanShiLingGuai_TaskCounter") - self.oldTaskCounter >= 2:
            self.owner.setTaskFinish(self.npcName, self.npcTaskIndex, self.selfIndex)
