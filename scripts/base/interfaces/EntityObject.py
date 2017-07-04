# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class EntityObject:
    def __init__(self):
        pass

    def hasAttr(self, attr):
        return hasattr(self, attr)

    def setAttr(self, attr, value):
        if hasattr(self, attr):
            setattr(self, attr, value)
        else:
            exec("self." + attr + "= value")

    def getAttr(self, attr):
        return getattr(self, attr)

    def delAttr(self, attr):
        delattr(self, attr)

    def getDatabaseID(self):
        return self.databaseID

    def getScriptName(self):
        return self.__class__.__name__()

    def getCell(self):
        return self.cell
