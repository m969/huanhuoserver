# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TTaskInfo(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        datas = {
            "taskNpcName":self[0],
            "taskIndex":self[1],
            "isTaskFinish":self[2],
            "isTaskCommit":self[3]
        }
        return datas

    def createFromDict(self, dicData):
        self.extend([dicData["taskNpcName"], dicData["taskIndex"], dicData["isTaskFinish"], dicData["isTaskCommit"]])
        return self

class TASK_INFO_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dic):
        return TTaskInfo().createFromDict(dic)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TTaskInfo)

task_info_inst = TASK_INFO_PICKLER()

class TTaskInfoList(dict):
    def __init__(self):
        dict.__init__(self)

    def asDict(self):
        """
        转换格式存到数据库
        :return:
        """
        datas = []
        for key, val in self.items():
            datas.append(val)
        dic = {"values": datas}       #还原为固定字典
        return dic

    def createFromDict(self, dictData):
        """
        从数据库取出并转换格式
        taskInfoList=
        {
            npc名字+任务索引:
                {
                    0: npc名字,
                    1: 任务索引,
                    2: 是否完成
                    3: 是否提交
                },
            npc名字+任务索引:
                {
                    0: npc名字,
                    1: 任务索引,
                    2: 是否完成
                    3: 是否提交
                },
        }
        :param dictData:
        :return:
        """
        for data in dictData["values"]:
            self[data[0] + str(data[1])] = data
        return self

class TASK_INFO_LIST_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dic):
        return TTaskInfoList().createFromDict(dic)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TTaskInfoList)

task_info_list_inst = TASK_INFO_LIST_PICKLER()