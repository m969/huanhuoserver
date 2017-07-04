# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TFriendsInfo(dict):
    def __init__(self):
        dict.__init__(self)
        pass

    def asDict(self):
        """
        
        :return: 
        """
        datas = []
        dic = {"values":datas}
        for key, value in self.items():
            datas.append(value)
        return dic

    def createFromDict(self, dictData):
        for data in dictData["values"]:
            self[data] = data
        return self

class FRIENDS_INFO_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dictData):
        return TFriendsInfo().createFromDict(dictData)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TFriendsInfo)

friends_info_inst = FRIENDS_INFO_PICKLER()