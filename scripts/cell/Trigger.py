# -*- coding: utf-8 -*-
import KBEngine, time
from KBEDebug import *
from interfaces.EntityObject import EntityObject
from triggerStrategies.onEnterTrap.TriggerStrategy import *


class Trigger(KBEngine.Entity, EntityObject):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        EntityObject.__init__(self)
        DEBUG_MSG("Trigger:__init__")
        DEBUG_MSG(self.triggerStrategy)
        if self.lifeSpans <= 0:
            pass
        else:
            self.addTimer(self.lifeSpans, 0, 0)
        # self.combatable = False

    def onTimer(self, tid, userArg):
        # self.delTimer(tid)
        self.destroy()

    def isTrigger(self):
        return True

    def onEnterTrap(self, other, rangeXZ, rangeY, controllerID, userArg):
        """
        当进入触发器时
        """
        # exec("self.strategy = " + self.triggerStrategy + "(self, other, rangeXZ, rangeY, controllerID, userArg)")
        self.triggerStrategy.setInfo(self, other, rangeXZ, rangeY, controllerID, userArg)
        self.triggerStrategy.excute()

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerID, userArg):
        """
        当离开触发器时
        """
        pass

    def onWitnessed(self, isWitnessed):
        """
        当被看到时
        """
        DEBUG_MSG("Trigger:onWitnessed")
        self.proximityID = self.addProximity(self.triggerSize, self.triggerSize, 0)
        pass

    def moveToPointSample(self, destination, velocity, distance=0.2):
        """
        移动到某点
        """
        self.moveToPoint(destination, velocity, distance, {}, True, True)
