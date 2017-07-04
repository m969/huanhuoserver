# -*- coding: utf-8 -*-
import KBEngine, time
from KBEDebug import *
from triggerStrategies.Strategy import Strategy


class TriggerStrategy(Strategy):
    """
    触发器策略
    """

    def __init__(self):
        Strategy.__init__(self)
        pass

    def setInfo(self, origin=None, other=None, rangeXZ=None, rangeY=None, controllerID=None, userArg=None):
        """
        设置触发器策略的信息
        """
        self.origin = origin
        self.other = other
        self.triggerRangeXZ = rangeXZ
        self.triggerRangeY = rangeY
        self.triggerControllerID = controllerID
        self.triggerUserArg = userArg

    def setData(self, strategyData):
        pass

    def excute(self):
        """
        策略的执行方法
        :return:
        """
        Strategy.excute(self)
        pass


class DamageTriggerStrategy(TriggerStrategy):
    """
    伤害策略
    """

    def __init__(self):
        TriggerStrategy.__init__(self)
        pass

    def setInfo(self, origin=None, other=None, rangeXZ=None, rangeY=None, controllerID=None, userArg=None):
        super().setInfo(origin, other, rangeXZ, rangeY, controllerID, userArg)

    def setData(self, strategyData):
        super().setData(strategyData)
        self.damage = strategyData["攻击力"]

    def excute(self):
        super().excute()
        if self.other.getAttr("className") == self.origin.spellCaster.getAttr("className"):
            return
        if self.other.getAttr("combatable") is True:
            if self.other.getEntityID() != self.origin.spellCaster.getEntityID():
                self.other.receiveDamage(self.origin.spellCaster, self.damage)


class OnceDamageTriggerStrategy(TriggerStrategy):
    """
    伤害策略
    """

    def __init__(self):
        TriggerStrategy.__init__(self)
        pass

    def setInfo(self, origin=None, other=None, rangeXZ=None, rangeY=None, controllerID=None, userArg=None):
        super().setInfo(origin, other, rangeXZ, rangeY, controllerID, userArg)

    def setData(self, strategyData):
        super().setData(strategyData)
        self.damage = strategyData["攻击力"]

    def excute(self):
        super().excute()
        if self.other.getAttr("className") == self.origin.spellCaster.getAttr("className"):
            return
        if self.other.getAttr("combatable") is True:
            if self.other.getEntityID() != self.origin.spellCaster.getEntityID():
                self.other.receiveDamage(self.origin.spellCaster, self.damage)
                self.origin.destroy()


class GateWayTriggerStrategy(TriggerStrategy):
    """
    传送门策略
    """

    def __init__(self):
        TriggerStrategy.__init__(self)
        pass

    def setData(self, strategyData):
        super().setData(strategyData)
        self.targetSpaceName = strategyData["目标场景"]
        self.gateWayEntrancePosition = strategyData["传送门入口点"]

    def setInfo(self, origin=None, other=None, rangeXZ=None, rangeY=None, controllerID=None, userArg=None):
        super().setInfo(origin, other, rangeXZ, rangeY, controllerID, userArg)

    def excute(self):
        super().excute()
        if self.other.getAttr("isAvatar") is True:
            KBEngine.globalData["spacesManager"].teleportToSpaceByName(
                self.targetSpaceName,
                self.gateWayEntrancePosition,
                self.other.base)
