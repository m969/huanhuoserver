# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class CombatProperty:
    def __init__(self):
        self.movable = True
        self.attackable = True

    def setOnOff(self, onOffName, boolValue):
        setattr(self, onOffName, boolValue)
        return

    def getOnOff(self, onOffName):
        return getattr(self, onOffName)

    def setProperty(self):
        return
