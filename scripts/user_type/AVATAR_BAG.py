# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TAvatarBag(dict):
    def __init__(self):
        dict.__init__(self)
        pass

    def asDict(self):
        datas = []
        dic = {"values":datas}
        for key, value in self.items():
            datas.append(value)
        return dic

    def createFromDict(self, dictData):
        for data in dictData["values"]:
            self[data] = data
        return self

class AVATAR_BAG_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dictData):
        return TAvatarBag().createFromDict(dictData)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TAvatarBag)

avatar_bag_inst = AVATAR_BAG_PICKLER()