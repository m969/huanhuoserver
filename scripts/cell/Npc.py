# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from interfaces.EntityObject import EntityObject
import npc_data
import store_data
import goods_data
import baoxiang_data
import zuanshi_data
import baoma_data

class Npc(KBEngine.Entity, EntityObject):
    def __init__(self):
        """
        entityName属性由实体的创建者给出，以区分不同的npc并且提取不同的任务数据初始化npc，如果是商人则会提取商店物品数据初始化npc。
        :return:
        """
        # DEBUG_MSG("Npc:__init__")
        KBEngine.Entity.__init__(self)
        KBEngine.globalData["space_%i" % self.spaceID].cell.onNpcEnter(self)
        if (self.entityName == "新手引导") | (self.entityName == "上水村长") | (self.entityName == "守村人") | \
            (self.entityName == "工匠") | (self.entityName == "神秘人") | (self.entityName == "店小二") | \
                (self.entityName == "刘公子") | (self.entityName == "陈丘村长") | (self.entityName == "姑娘") \
                | (self.entityName == "钱大娘") | (self.entityName == "兽族族长") | (self.entityName == "宝马盗贼") \
                | (self.entityName == "看箱人"):
            self.npcData = npc_data.data
            for key in self.npcData:
                if key == self.entityName:
                    self.myTaskDict = self.npcData.get(key)
                    break
        elif (self.entityName == "商人") | (self.entityName == "上水商人"):
            self.storeData = store_data.data
            self.goodsData = goods_data.data
            i = 0
            for value in self.storeData:
                for (k, v) in self.goodsData.items():
                    if value == v['name']:
                        self.storeGoodsIDList[i] = k
                        i += 1
        #变相商人，利用商人给予物品的特性，给予商品价格为0的任务道具
        elif self.entityName == "钻石商人":
            self.storeData = zuanshi_data.data
            self.goodsData = goods_data.data
            i = 0
            for value in self.storeData:
                for (k, v) in self.goodsData.items():
                    if value == v['name']:
                        self.storeGoodsIDList[i] = k
                        i += 1

    def isNpc(self):
        return True

    def onWitnessed(self, isWitnessed):
        """
        当npc被玩家观察到时此函数被调用。
        :param isWitnessed:
        :return:
        """
        # DEBUG_MSG("Npc:onWitnessed")
        pass

    def requestBuyGoods(self, requester, goodsID):
        DEBUG_MSG("Npc:requestBuyGoods")
        goodsName = goods_data.data[goodsID]['name']
        if goodsName in self.storeData:
            if requester.getAttr('goldCount') >= goods_data.data[goodsID]['price']:
                requester.giveGoods(goodsID)
                requester.deductMoney(goods_data.data[goodsID]['price'])
                return True
            else:
                return False
        else:
            return False

    def requestDialog(self, requester, flag=0):
        DEBUG_MSG("Npc:requestDialog")

    def requestTask(self, requester):
        """
        请求任务接口。由玩家发起调用，此函数会视情况决策，当玩家没有任务时会赋予玩家任务，当玩家任务已完成会给予奖励，并返回玩家此npc对应的对话信息。
        :param requester:
        :return:
        """
        DEBUG_MSG("Npc:requestDialog")
        requesterTaskInfoList = []
        requesterTaskInfoList = requester.getTaskInfo(self.entityName)
        taskCommitCount = 0 # 任务完成数
        if requesterTaskInfoList.__len__() == 0:
            DEBUG_MSG("avatar has no my task!")
            DEBUG_MSG("give task " + str(1))
            self.giveTask(requester, 1)
            return self.myTaskDict[1].get("任务描述")
            pass
        else:
            for requesterTaskInfo in requesterTaskInfoList:

                taskNpcName = requesterTaskInfo[0] # npc名称
                taskIndex = requesterTaskInfo[1] # 任务索引
                isTaskFinish = requesterTaskInfo[2] # 任务是否已完成
                isTaskCommit = requesterTaskInfo[3] # 任务是否已提交

                if isTaskFinish == False and isTaskCommit == False:
                    return self.myTaskDict[taskIndex].get("任务描述")
                    pass
                if isTaskFinish == True and isTaskCommit == False:
                    requester.giveAward(taskNpcName, taskIndex)
                    return self.myTaskDict[taskIndex].get("任务完成描述")
                    pass
                if isTaskFinish == True and isTaskCommit == True:
                    taskCommitCount += 1
                    if taskCommitCount >= self.myTaskDict.__len__():
                        return self.myTaskDict[1]['对话列表'][0]

        DEBUG_MSG("avatar has some finish task!")
        requesterNextTaskIndex = 0  # 请求者的下一个任务的索引
        # for (taskIndexFromNpc, taskInfo) in self.npcData.items():
        for aTaskInfoFromRequester in requesterTaskInfoList:
            aTaskIndexFromRequester = aTaskInfoFromRequester[1]
            DEBUG_MSG("task " + str(aTaskIndexFromRequester) + " has finish!")
            if aTaskIndexFromRequester >= requesterNextTaskIndex:
                requesterNextTaskIndex = aTaskIndexFromRequester + 1  # 如果有完成的任务，就将已完成的任务的索引加一，作为下一个任务的索引
        if requesterNextTaskIndex == 0:
            ERROR_MSG("avatar has some finish task, but requesterNextTaskIndex == 0")
        else:
            DEBUG_MSG("requesterNextTaskIndex is " + str(requesterNextTaskIndex))
            DEBUG_MSG("give task " + str(requesterNextTaskIndex))
            self.giveTask(requester, requesterNextTaskIndex)
            return self.myTaskDict[requesterNextTaskIndex].get("任务描述")

    def giveTask(self, requester, taskID):
        """
        赋予请求者任务。
        :param requester:
        :param taskID:
        :return:
        """
        DEBUG_MSG("Npc:giveTask")
        requester.giveTask(self.entityName, taskID)

    def onTimer(self, timerHandle, userData):
        pass
