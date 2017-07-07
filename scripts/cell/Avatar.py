# -*- coding: utf-8 -*-
import KBEngine, copy, enum, operator
from KBEDebug import *
from KTween.KTweenEnum import KTweenEnum
import Skills
import avatar_skill_data
import npc_data
import goods_data
import level_data
from TASK_INFO import TTaskInfo
from AVATAR_BAG import TAvatarBag
from FRIENDS_INFO import TFriendsInfo
from interfaces.EntityObject import EntityObject
from interfaces.CombatEntity import CombatEntity
from taskScripts.MuJingGuaiRenWu import MuJingGuaiRenWu
from taskScripts.YanShiLingGuaiRenWu import YanShiLingGuaiRenWu
from taskScripts.Duihuarenwu import Duihuarenwu
from taskScripts.Xiaoshiniudao_San import Xiaoshiniudao_San
from taskScripts.Caijizuanshi import Caijizuanshi
from taskScripts.TanxianshandongRenWu import TanxianshandongRenWu
from taskScripts.Bangzhushenmiren import Bangzhushenmiren
from taskScripts.Sidingzhongsheng import Sidingzhongsheng
from taskScripts.Qianlisongqing import Qianlisongqing
from taskScripts.Xunzhaobaoma import Xunzhaobaoma
from taskScripts.Pobudeyi import Pobudeyi
from triggerStrategies.onEnterTrap.TriggerStrategy import *


class AvatarState:
    def __init__(self):
        DEBUG_MSG("AvatarState")


class StandState(AvatarState):
    def __init__(self):
        DEBUG_MSG("StandState")
        AvatarState.__init__(self)


class RunState(AvatarState):
    def __init__(self):
        DEBUG_MSG("RunState")
        AvatarState.__init__(self)


class Avatar(KBEngine.Entity, EntityObject, CombatEntity):
    def __init__(self):
        DEBUG_MSG("Avatar.cell:__init__")
        KBEngine.Entity.__init__(self)
        EntityObject.__init__(self)
        CombatEntity.__init__(self)
        self.skillPool = avatar_skill_data.data
        self.levelInfoData = level_data.level_info_data
        self.isAvatar = True
        self.levelName = level_data.level_name_data[self.level]
        self.levelPeriodName = level_data.level_period_name_data[self.levelPeriod]
        self.HP = 100 #self.HP_Max
        self.MSP = 1000 # self.MSP_Max
        self.SP = 1000 # self.SP_Max
        self.MSP_Max = 1000
        self.SP_Max = 1000
        self.taskScriptList = {}
        self.finishTaskScriptList = []
        """
        在角色初始化时，遍历角色的任务列表，通过任务的所属npc（avatarTaskInfo[0]）以及任务索引（avatarTaskInfo[1]）
        找出任务的所有信息，
        提取任务脚本信息并且创建任务监视脚本。onTimer函数会每秒调用任务监视脚本的检测函数检测任务是否满足完成条件。
        """
        for (key, avatarTaskInfo) in self.taskInfoList.items():
            npcTaskList = npc_data.data[avatarTaskInfo[0]]
            for (taskIndex, taskInfo) in npcTaskList.items():
                if taskIndex == avatarTaskInfo[1]:
                    taskScript = taskInfo["任务脚本"]
                    nextTaskScriptKey = 0
                    for taskScriptKey in self.taskScriptList.keys():
                        if taskScriptKey >= nextTaskScriptKey:
                            nextTaskScriptKey = taskScriptKey
                    nextTaskScriptKey += 1
                    exec("self.taskScriptList[" + str(nextTaskScriptKey) + "] = " + taskScript + "(self, " + str(nextTaskScriptKey) +
                         ", avatarTaskInfo[0], avatarTaskInfo[1])")
        self.addTimer(1, 1, 0)  # 添加 任务监视检测 定时器
        self.addTimer(1, 60, 1)  # 添加 灵力上限值 定时器
        self.counter = 0    # 新场景重置坐标次数计数器

    def onTimer(self, timerHandle, userData):
        if userData == 0:   # 任务监视脚本定时器
            """
            此Timer会每秒调用任务监视脚本的检测函数检测任务是否满足完成条件。
            """
            tempDict = {}
            for k in self.taskScriptList.keys():
                self.taskScriptList[k].detectTaskCompleteness()
            count = 0
            for (key, value) in self.taskScriptList.items():
                for k in self.finishTaskScriptList:
                    if k == key:
                        count = 1
                if count == 0:
                    tempDict[key] = value
            self.taskScriptList = tempDict
            self.finishTaskScriptList.clear()
        if userData == 1:   # 灵力值增加定时器，每60秒调用一次
            currentLevelSpLimit = self.levelInfoData[self.level]["等阶灵力需求值"][self.levelPeriod]
            if self.SP_Max >= currentLevelSpLimit:
                self.SP_Max = currentLevelSpLimit
            else:
                self.SP_Max += self.talent  # 历练度、饥渴度
        if userData == 2:   # 进入新场景重置坐标定时器
            DEBUG_MSG("Avatar : reset position!")
            self.position = self.newSpacePosition
            self.counter += 1
            if self.counter >= 10:
                self.delTimer(timerHandle)
        if userData == 3:   # 重生定时器
            DEBUG_MSG("Avatar set respawnPosition!")
            respawnPosition = self.getCurrSpace().getAttr("respawnPoint")
            DEBUG_MSG(respawnPosition)
            self.position = respawnPosition
            self.HP = self.HP_Max
            self.MSP = self.MSP_Max
            self.SP = self.SP_Max
            self.allClients.OnRespawn(respawnPosition)
            self.delTimer(timerHandle)

    def isAvatar(self):
        return True

    def isCombatEntity(self):
        return True

    def isGoingToTeleport(self, spaceName, gateWayEntrancePosition):
        DEBUG_MSG("Avatar:isGoingToTeleport")
        self.client.onMainAvatarLeaveSpace()
        self.newSpaceName = spaceName
        self.newSpacePosition = gateWayEntrancePosition
        pass

    def teleportToSpace(self, spaceCellMailbox, position, direction):
        """
        defined.
        baseapp返回teleportSpace的回调
        """
        DEBUG_MSG("Avatar:teleportToSpace")
        self.getCurrSpaceBase().onLeave(self.id)
        self.teleport(spaceCellMailbox, position, direction)
        self.base.onTeleportSuccess(self.newSpaceName)
        self.counter = 0
        self.resetPositionTimerHandle = self.addTimer(0.1, 0.2, 2)  # 重置角色坐标计数器
        # self.addTimer(3, 0, 3)   # 删除 重置角色坐标计数器
        self.onAvatarEnterSpace(spaceCellMailbox.getAttr("spaceID"), spaceCellMailbox.getAttr("spaceName"))

    def _onTeleportSuccess(self, nearbyEntity):
        DEBUG_MSG("Avatar:onTeleportSuccess")
        self.base.onTeleportSuccess(self.newSpaceName)
        self.teleport(None, self.newSpacePosition, (0.0, 0.0, 0.0))

    def onLeaveSpaceClientInputInValid(self, exposed):
        DEBUG_MSG("Avatar:onLeaveSpaceClientInputInValid")
        KBEngine.globalData["space_" + self.newSpaceName].requestTeleport(self.base)
        pass

    def onAvatarEnterSpace(self, spaceID, spaceName):
        DEBUG_MSG("Avatar:onEnterSpace")
        self.client.onMainAvatarEnterSpace(spaceID, spaceName)
        pass

    def requestMove(self, exposed, point):
        if self.movable:
            self.allClients.DoMove(point)

    def stopMove(self, exposed):
        # DEBUG_MSG("Avatar:stopMove")
        if self.movable:
            self.allClients.OnStopMove()

    def doSkill(self, *args, **kwargs):
        DEBUG_MSG("Avatar:doSkill", args)

    def requestDoSkillQ(self, exposed, point, yaw):
        if exposed != self.id:
            return
        if point is not None:
            skillData = avatar_skill_data.data[1]   # 技能1
            minSp = skillData["levelSpLimit"][1]    # 使用这个技能最少需要的灵力值
            maxSp = skillData["levelSpLimit"][1]    # 使用这个技能最多可以使用的灵力值
            skillSpAmount = 0   # 此次技能实际使用的灵力值
            if self.MSP < minSp:
                return
            if self.MSP >= maxSp:
                skillSpAmount = maxSp
                self.MSP -= maxSp
            else:
                skillSpAmount = self.MSP
                self.MSP = 0
            skillQuality = skillData["quality"]     # 技能品质，即将灵力转化为攻击力的效率
            damage = int(skillSpAmount * skillQuality)

            triggerStrategy = DamageTriggerStrategy()
            triggerStrategy.setData({"攻击力": self.attackForce})
            trigger = KBEngine.createEntity("Trigger",
                                           self.spaceID,
                                           self.position,
                                           (0.0, 0.0, yaw),
                                           {
                                               'name': "SkillQ",
                                               'triggerID': 1,
                                               'triggerSize': 4,
                                               'damage': damage,
                                               'parentSkill': "SkillQ",
                                               'spellCaster': self,
                                               'triggerStrategy': triggerStrategy
                                           })
            trigger.moveToPointSample(point, 80)

        self.allClients.DoSkillQ(point, yaw)        # 在客户端上调用DoSkillQ函数

    def requestDoSkillW(self, exposed, point):
        DEBUG_MSG("Avatar:requestDoSkillW")
        if exposed != self.id:
            return
        if point is not None:
            skillData = avatar_skill_data.data[2]   # 技能2
            minSp = skillData["levelSpLimit"][1]    # 使用这个技能最少需要的灵力值
            maxSp = skillData["levelSpLimit"][1]    # 使用这个技能最多可以使用的灵力值
            skillSpAmount = 0   # 此次技能实际使用的灵力值
            if self.MSP < minSp:
                return
            if self.MSP >= maxSp:
                skillSpAmount = maxSp
                self.MSP -= maxSp
            else:
                skillSpAmount = self.MSP
                self.MSP = 0
            skillQuality = skillData["quality"]     # 技能品质，即将灵力转化为攻击力的效率
            damage = int(skillSpAmount * skillQuality)

            triggerStrategy = DamageTriggerStrategy()
            triggerStrategy.setData({"攻击力": 10})
            trigger = KBEngine.createEntity("Trigger",
                                            self.spaceID,
                                            point,
                                            (0.0, 0.0, 0.0),
                                            {
                                                'name': "SkillW",
                                                'triggerID': 2,
                                                'triggerSize': 4,
                                                'damage': damage,
                                                'parentSkill': "SkillW",
                                                'spellCaster': self,
                                                'triggerStrategy': triggerStrategy
                                            })
        self.allClients.DoSkillW(point)

    def requestBuyGoods(self, exposed, spaceID, npcName, goodsID):
        if exposed != self.id:
            return
        DEBUG_MSG("Avatar:requestBuyGoods")
        npcMailbox = KBEngine.globalData["space_cell_%i" % spaceID].requestNpc(npcName)
        result = npcMailbox.requestBuyGoods(self, goodsID)
        self.client.BuyResult(result)
        pass

    def giveGoods(self, goodsID):
        DEBUG_MSG("Avatar:giveGoods")
        tempBag = self.avatarBag
        DEBUG_MSG(tempBag)
        tempBag[goodsID] = goodsID
        self.avatarBag = tempBag
        DEBUG_MSG(self.avatarBag)
        #郑晓飞--小试牛刀三任务--购买木剑
        if goods_data.data[goodsID]['name'] == "木剑":
            if self.hasAttr("Xiaoshiniudao_San_TaskCounter") is True:
                self.setAttr("Xiaoshiniudao_San_TaskCounter",
                             self.getAttr("Xiaoshiniudao_San_TaskCounter") + 1)
            else:
                self.setAttr("Xiaoshiniudao_San_TaskCounter", 1)
        #郑晓飞--探险山洞任务--获得宝箱
        if goods_data.data[goodsID]['name'] == "精致宝箱":
            if self.hasAttr("TanxianshandongRenWu_TaskCounter") is True:
                self.setAttr("TanxianshandongRenWu_TaskCounter",
                             self.getAttr("TanxianshandongRenWu_TaskCounter") + 1)
            else:
                self.setAttr("TanxianshandongRenWu_TaskCounter", 1)
        # 郑晓飞--采集钻石任务--采集钻石
        if goods_data.data[goodsID]['name'] == "钻石":
            if self.hasAttr("Caijizuanshi_TaskCounter") is True:
                self.setAttr("Caijizuanshi_TaskCounter",
                            self.getAttr("Caijizuanshi_TaskCounter") + 1)
            else:
                self.setAttr("Caijizuanshi_TaskCounter", 1)
        # 郑晓飞--寻找宝马任务--寻找宝马
        if goods_data.data[goodsID]['name'] == "宝马":
            if self.hasAttr("Xunzhaobaoma_TaskCounter") is True:
                self.setAttr("Xunzhaobaoma_TaskCounter",
                            self.getAttr("Xunzhaobaoma_TaskCounter") + 1)
            else:
                self.setAttr("Xunzhaobaoma_TaskCounter", 1)
        #/郑晓飞
        pass

    def deleteGoods(self, goodsID):
        """
        郑晓飞----删除背包中的物品
        :param goodID: 物品ID
        :return: 
        """
        DEBUG_MSG("Avatar:deleteGoods")
        tempBag = self.avatarBag
        DEBUG_MSG(tempBag)
        if goodsID in tempBag.keys():
            del tempBag[goodsID]
        self.avatarBag = tempBag
        DEBUG_MSG(self.avatarBag)
        # 郑晓飞--千里送情任务--将信给予刘公子(丢弃)
        if goods_data.data[goodsID]['name'] == "信":
            if self.hasAttr("Qianlisongqing_TaskCounter") is True:
                self.setAttr("Qianlisongqing_TaskCounter",
                             self.getAttr("Qianlisongqing_TaskCounter") + 1)
            else:
                self.setAttr("Qianlisongqing_TaskCounter", 1)
        pass

    def deductMoney(self, num):
        DEBUG_MSG("getMoney")
        self.goldCount -= num
        pass

    def requestDialog(self, exposed, spaceID, npcName):
        """
        此函数由客户端调用，此函数会向指定npc请求返回对话的内容。
        """
        if exposed != self.id:
            return
        dialog = ""
        # npcMailbox = KBEngine.globalData["BigWorld_Cell"].requestNpc(npcName)
        npcMailbox = KBEngine.globalData["space_cell_%i" % spaceID].requestNpc(npcName)
        if npcMailbox:
            dialog = npcMailbox.requestTask(self)
            self.client.DoDialog(npcMailbox.getAttr("name"), dialog)
        else:
            DEBUG_MSG("npcMailbox is None")

    def getTaskInfo(self, npcName):
        DEBUG_MSG("Avatar:getTaskInfo")
        specificNpcTaskInfo = []
        for aTaskInfo in self.taskInfoList.values():
            if aTaskInfo[0] == npcName:
                specificNpcTaskInfo.append(aTaskInfo)
        return specificNpcTaskInfo

    def setAvatarName(self, entityName):
        self.entityName = entityName

    def setTaskFinish(self, npcName, taskIndex, watcherIndex):
        """
        任务完成度监视脚本会监测任务是否已完成，如果任务完成了就会调用这个函数，设置角色任务信息为已完成状态，
        并且删除任务完成度监视脚本。
        :param npcName:
        :param taskIndex:
        :return:
        """
        DEBUG_MSG("Avatar:setTaskFinish")
        for (key, taskInfo) in self.taskInfoList.items():
            if npcName == taskInfo[0] and taskIndex == taskInfo[1]:
                DEBUG_MSG("setTaskFinish")
                taskInfo[2] = True
                self.taskInfoList[key] = taskInfo
                self.finishTaskScriptList.append(watcherIndex)

    def isTaskFinish(self, npcName, taskIndex):
        DEBUG_MSG("Avatar:isTaskFinish")
        for taskInfo in self.taskInfoList.values():
            if npcName == taskInfo[0] and taskIndex == taskInfo[1]:
                DEBUG_MSG("return isTaskFinish")
                return taskInfo[2]
        return False

    def giveAward(self, npcName, taskIndex):
        """
        任务完成给予奖励，由npc调用，成功给予奖励后设置角色任务信息为已提交。
        :param npcName:
        :param taskIndex:
        :return:
        """
        DEBUG_MSG("Avatar:giveAward")
        self.goldCount += npc_data.data[npcName][taskIndex]["金币奖励"]
        for (propName, propCount) in npc_data.data[npcName][taskIndex]["道具奖励"].items():
            # goodsInfo = {0:propName, 1:propCount}
            i = 0
            for (k, va) in goods_data.data.items():
                if propName == va["name"]:
                    i = 1
                    DEBUG_MSG("give prop id = " + str(k))
                    self.giveGoods(k)
            if i == 0:
                DEBUG_MSG("has no this prop!")
        #郑晓飞------丢掉任务道具
        for (propName, propCount) in npc_data.data[npcName][taskIndex]["道具丢弃"].items():
            i = 0
            for (k, va) in goods_data.data.items():
                if propName == va["name"]:
                    i = 1
                    DEBUG_MSG("delete prop id = " + str(k))
                    self.deleteGoods(k)
            if i == 0:
                DEBUG_MSG("has no this prop!")
        #/郑晓飞
        for (key, value) in self.taskInfoList.items():
            if value[0] == npcName and value[1] == taskIndex:
                self.taskInfoList[key][3] = True
                return

    def giveTask(self, npcName, taskIndex):
        """
        赋予任务，由npc调用。
        :param npcName:
        :param taskIndex:
        :return:
        """
        DEBUG_MSG("Avatar:giveTask")
        taskInfo = TTaskInfo()
        taskInfo.extend([npcName, taskIndex, False, False])
        self.taskInfoList[npcName + str(taskIndex)] = taskInfo
        taskScript = npc_data.data[npcName][taskIndex]["任务脚本"]
        indexOnAvatarTaskScriptList = 0
        for keyIndex in self.taskScriptList.keys():
            DEBUG_MSG("taskScriptList.keys() = ")
            DEBUG_MSG(self.taskScriptList.keys())
            if keyIndex >= indexOnAvatarTaskScriptList:
                indexOnAvatarTaskScriptList = keyIndex
        indexOnAvatarTaskScriptList += 1
        exec("self.taskScriptList[" + str(indexOnAvatarTaskScriptList) + "] = " + taskScript + "(self, " + str(indexOnAvatarTaskScriptList) +
             ", npcName, taskIndex)")

    def onDestroy(self):
        """
        实体被销毁时会被调用。
        :return:
        """
        DEBUG_MSG("onAvatarCellDestroy")

    def onDie(self, murderer):
        """
        当实体HP小于或等于0时被调用。
        :return:
        """
        CombatEntity.onDie(self, murderer)
        self.addTimer(4, 0, 3)  # 添加重生时间器
        return

    def onSendChatMessage(self, exposed, selfName, chatContent):
        """
        郑晓飞---响应客户端的聊天函数并将聊天内容转发给其他客户端    
        :param chatContent: 聊天内容
        :return: null
        """
        DEBUG_MSG("onSendChatMessage" + chatContent)
        self.allClients.onReciveChatMessage(selfName, chatContent)

    def FindFriends(self, exposed):
        """
        #--郑晓飞---返回数据库中的所有注册人员在客户端进行比对，在客户端检测是否有此搜索朋友
        :param exposed: 
        :return: 
        """
        DEBUG_MSG("FindFriends")
        avatarId = self.id
        KBEngine.globalData["avatarId"] = self.id
        DEBUG_MSG(avatarId)
        KBEngine.executeRawDatabaseCommand("SELECT sm_entityName from tbl_Avatar", _getAllEntityName)

    def AddFriends(self, exposed, goldxFriendsName):
        """
        郑晓飞---添加好友，并将此好友写入数据库
        :return: 
        """
        DEBUG_MSG("Avatar:AddFriends")
        tempFriends = self.avatarFriends
        DEBUG_MSG(tempFriends)
        tempFriends[goldxFriendsName] = goldxFriendsName
        self.avatarFriends = tempFriends
        DEBUG_MSG(self.avatarFriends)
        self.allClients.OnShowAllFriends(self.avatarFriends)

    def DeleteFriends(self, exposed, goldxFriendsName):
        """
        郑晓飞---删除好友，同时也删除数据库中的信息
        :return: 
        """
        DEBUG_MSG("Avatar:DeleteFriends")
        tempFriends = self.avatarFriends
        DEBUG_MSG(tempFriends)
        del tempFriends[goldxFriendsName]
        self.avatarFriends = tempFriends
        DEBUG_MSG(self.avatarFriends)
        self.allClients.OnShowAllFriends(self.avatarFriends)

    def ShowAllFriends(self, exposed):
        """
        郑晓飞---显示全部好友
        :return: 
        """
        DEBUG_MSG("Avatar:ShowAllFriends")
        DEBUG_MSG(self.avatarFriends)
        self.allClients.OnShowAllFriends(self.avatarFriends)

    def SendAvatarNameToClient(self, entityNames):
        """
        将所有玩家的名字发给客户端
        :param entityNames: 数据库中所有注册玩家的字符串
        :return: 
        """
        DEBUG_MSG("Avatar:SendAvatarNameToClient")
        self.allClients.OnFindFriends(entityNames)

def _getAllEntityName(resultCollect, num, errorInfo):
    DEBUG_MSG("_getAllEntityName")
    DEBUG_MSG(resultCollect)
    entityNames = ""
    if errorInfo is None:
        for value in resultCollect:
            entityNames += str(value[0]) + " "
        DEBUG_MSG(KBEngine.globalData["avatarId"])
        KBEngine.entities[KBEngine.globalData["avatarId"]].SendAvatarNameToClient(entityNames)
        DEBUG_MSG("_getAllEntityName" + entityNames)
    else:
        ERROR_MSG("create tbl failed")