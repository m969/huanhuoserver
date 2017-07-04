# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import datetime
from interfaces.EntityObject import EntityObject


class Npc(KBEngine.Base, EntityObject):
    def __init__(self):
        KBEngine.Base.__init__(self)
        EntityObject.__init__(self)
        self.timerID = self.addTimer(1, 1, 0)

    def onTimer(self, timerHandle, userData):
        if userData == 0:
            if hasattr(self, "entityName"):
                if self.entityName == "新手引导":
                    KBEngine.globalData["BigWorld"].loginSpace(self)
                    self.delTimer(self.timerID)
        pass

    def onDestroy(self):
        DEBUG_MSG("Npc:Base:onDestroy")

    def onWriteToDB(self, cellData):
        DEBUG_MSG("Npc:Base:onWriteToDB")

    def onGetCell(self):
        DEBUG_MSG("Npc:onGetCell")
        pass

    def createCell(self, space):
        DEBUG_MSG("Npc:createCell")
        self.createCellEntity(space)
