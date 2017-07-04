# -*- coding: utf-8 -*-
import KBEngine
import time
import math
import random
import monster_data
from KBEDebug import *
from triggerStrategies.onEnterTrap.TriggerStrategy import *


class AI:
    def __init__(self):
        # 移动速度
        self.speed = monster_data.data[self.name]["移动速度"]
        # 怪物的攻击距离
        self.monsterAttackDistance = monster_data.data[self.name]["攻击距离"]
        # 怪物的活动范围
        self.territoryArea = monster_data.data[self.name]["活动范围"]
        #技能移动速度
        self.skillSpeed = monster_data.data[self.name]["技能移动速度"]
        # 移动目标位置
        self.movePos = (100, 0, 200)
        # 怪物攻击的敌人ID
        self.targetID = 0
        # 怪物技能攻击的实体
        self.targetEntity = None
        # 怪物移向敌人的移动id
        self.moveToEntityID = 0
        #
        self.addTimer(1, 1, 0)

    def initEntity(self):
        """
        virtual method.
        """
        pass

    def checkInTerritory(self):
        """
        virtual method.
        检查自己是否在可活动领地中
        """
        ret = False
        if math.fabs(self.movePos[0]) > self.spawnPos[0] - self.territoryArea:
            if math.fabs(self.movePos[0]) < self.spawnPos[0] + self.territoryArea:
                if math.fabs(self.movePos[2]) > self.spawnPos[2] - self.territoryArea:
                    if math.fabs(self.movePos[2]) < self.spawnPos[2] + self.territoryArea:
                        ret = True
        return ret

    def randomMovePos(self):
        """
        怪物的随机运动的坐标
        :return:True
        """
        while True:
            rnd = random.random()
            a = int(self.territoryArea * rnd)  # 移动半径距离在30米内
            b = int(360.0 * rnd)  # 随机一个角度
            x = int(a * math.cos(b))  # 半径 * 正余玄
            z = int(a * math.sin(b))
            # 新的位置
            self.movePos = (self.movePos[0] + x, self.movePos[1], self.movePos[2] + z)
            break
        return True

    def woodMonsterSkill(self, point, yaw):
        """
        木精怪的技能:发射一个火球
        :return:
        """
        # 如果目标位置不为空
        if point is not None:
            # 创建一个火球技能实体
            triggerStrategy = OnceDamageTriggerStrategy()
            triggerStrategy.setData({"攻击力": 10})
            bullet = KBEngine.createEntity("Trigger",
                                           self.spaceID,
                                           (self.position.x, 1, self.position.z),
                                           (0.0, 0.0, 0.0),
                                           {
                                               'lifeSpans': 2,
                                                'name':"MuJingGuaiSkill",
                                                'triggerID': 3,
                                                'triggerSize': 2,
                                                'damage': 10,
                                                'parentSkill': "MuJingGuaiSkill",
                                                'spellCaster': self,
                                                'triggerStrategy': triggerStrategy
                                            })
            # 火球技能移动到目标位置
            bullet.moveToPointSample((point.x, 1, point.z), self.skillSpeed)

    def yanshilingMonsterSkill(self, point, yaw):
        """
        岩石灵怪的技能:发射一个火球
        :return:
        """
        # 如果目标位置不为空
        if point is not None:
            # 创建一个火球技能实体
            triggerStrategy = OnceDamageTriggerStrategy()
            triggerStrategy.setData({"攻击力": 10})
            bullet = KBEngine.createEntity("Trigger",
                                           self.spaceID,
                                           (self.position.x, 1, self.position.z),
                                           (0.0, 0.0, 0.0),
                                           {
                                               'lifeSpans': 2,
                                                'name':"YanshilingGuaiSkill",
                                                'triggerID': 3,
                                                'triggerSize': 2,
                                                'damage': 10,
                                                'parentSkill': "YanshilingGuaiSkill",
                                                'spellCaster': self,
                                                'triggerStrategy': triggerStrategy
                                            })
            # 火球技能移动到目标位置
            bullet.moveToPointSample((point.x, 1, point.z), self.skillSpeed)

    def langshourenguaiMonsterSkill(self, point, yaw):
        """
        狼兽人怪的技能:发射一个火球或水球
        :return:
        """
        # 如果目标位置不为空
        if point is not None:
            # 创建一个火球技能实体
            triggerStrategy = OnceDamageTriggerStrategy()
            triggerStrategy.setData({"攻击力": 10})
            rnd = int(random.random() * 10)
            if rnd % 2 == 0:
                bullet = KBEngine.createEntity("Trigger",
                                               self.spaceID,
                                               (self.position.x, 1, self.position.z),
                                               (0.0, 0.0, 0.0),
                                               {
                                                   'lifeSpans': 2,
                                                   'name': "MuJingGuaiSkill",
                                                   'triggerID': 3,
                                                   'triggerSize': 2,
                                                   'damage': 10,
                                                   'parentSkill': "YanshilingGuaiSkill",
                                                   'spellCaster': self,
                                                   'triggerStrategy': triggerStrategy
                                               })
                #if self.name == "狼兽人怪":
                self.allClients.Attack_01()
            else:
                bullet = KBEngine.createEntity("Trigger",
                                               self.spaceID,
                                               (self.position.x, 1, self.position.z),
                                               (0.0, yaw, 0.0),
                                               {
                                                   'lifeSpans': 2,
                                                   'name': "YanshilingGuaiSkill",
                                                   'triggerID': 3,
                                                   'triggerSize': 2,
                                                   'damage': 10,
                                                   'parentSkill': "YanshilingGuaiSkill",
                                                   'spellCaster': self,
                                                   'triggerStrategy': triggerStrategy
                                               })
                #if self.name == "狼兽人怪":
                self.allClients.Attack_02()
            # 技能移动到目标位置
            bullet.moveToPointSample((point.x, 1, point.z), self.skillSpeed)

    def addTerritory(self):
        """
        添加领地
        进入领地范围的某些entity将视为敌人
        """
        # 有实体进入领域，并返回领域ID
        self.addProximity(self.territoryArea, 0, 0)

    def setTarget(self, entityID):
        """
        设置攻击目标
        """
        self.targetID = entityID

    # -------------------------------------Callbacks--------------------------------------

    def onEnterTrap(self, entityEntering, range_xz, range_y, controllerID, userarg):
        """
        KBEngine method.
        有entity进入trap
        """
        # 如果此领域不是以前定义的领域，则返回
        # if controllerID != self.territoryControllerID:
        # return
        # 如果不是玩家或实体已经被销毁或试图已经死亡则返回
        if entityEntering.getScriptName() != "Avatar":
            return
        # 当敌人进入检测区域并对怪物进行了攻击，添加敌人
        if self.HP < self.HP_Max:
            # 添加敌人ID
            self.onAddEnemy(entityEntering.id)
            # 添加敌人实体
            self.targetEntity = entityEntering
        # 添加敌人ID
        self.onAddEnemy(entityEntering.id)
        # 添加敌人实体
        self.targetEntity = entityEntering

    def onLeaveTrap(self, entityLeaving, range_xz, range_y, controllerID, userarg):
        """
        KBEngine method.
        有entity离开trap
        """
        # 如果此领域不是以前定义的领域，则返回假
        # if controllerID != self.territoryControllerID:
        #     return
        # 如果不是玩家或实体已经被销毁或试图已经死亡则返回假
        if entityLeaving.getScriptName() != "Avatar":
            return
        # 删除敌人ID
        self.onRemoveEnemy(entityLeaving.id)
        self.targetEntity = None

    def onAddEnemy(self, entityID):
        """
        virtual method.
        有敌人进入列表并将设置为敌人
        """
        if self.targetID == 0:
            self.setTarget(entityID)

    def onRemoveEnemy(self, entityID):
        """
        virtual method.
        删除敌人
        """
        if self.targetID == entityID:
            # 敌人丢失
            self.onLoseTarget()

    def onLoseTarget(self):
        """
        敌人丢失
        """
        self.targetID = 0

    def onMoveOver(self, controllerID, userData):
        """
        当怪物停止移动时调用闲置时的动画
        """
        self.allClients.StopMove()

        if controllerID == self.moveToEntityID:
            # 岩石灵怪释放技能
            if self.name == "炎石灵怪":
                self.yanshilingMonsterSkill(self.targetEntity.position, self.position.y)

            # 木精怪释放技能
            if self.name == "木精怪":
                self.woodMonsterSkill(self.targetEntity.position, self.position.y)

            # 狼兽人怪释放技能
            if self.name == "狼兽人怪":
                self.langshourenguaiMonsterSkill(self.targetEntity.position, self.position.y)



    def onTimer(self, tid, userArg):
        """
        KBEngine method.
        引擎回调timer触发
        """
        # 建立检测区域
        # self.addTerritory()
        # 没敌人或着敌人丢失就在自己的领域里运动
        if userArg == 0:
            #DEBUG_MSG("AI:addTerritory")
            self.addTerritory()
            self.delTimer(tid)

        if self.targetID == 0:
            # 在区域内没有目标，血量自动回满
            self.HP = self.HP_Max
            # 如果怪物在自己的领地内则随机运动，如果不在则返回出生点
            if self.checkInTerritory():
                self.randomMovePos()
            else:
                self.movePos = self.spawnPos
            self.moveToPoint(self.movePos, self.speed, 0, self, True, False)
            self.allClients.StartMove()

        if self.targetID != 0 and self.HP < self.HP_Max:
            # 敌人存在，向敌人移动并进攻敌人
            # 返回此移动的id
            self.moveToEntityID = self.moveToEntity(self.targetID, self.speed, self.monsterAttackDistance, self, True,
                                                    False)
            self.allClients.StartMove()
