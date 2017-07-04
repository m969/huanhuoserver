# -*- coding: utf-8 -*-
import KBEngine
import space_data
from KBEDebug import *
import sys


class SpacesManager(KBEngine.Base):
    def __init__(self):
        DEBUG_MSG("SpacesManager:__init__")
        KBEngine.Base.__init__(self)
        KBEngine.globalData["spacesManager"] = self
        # 根据场景配置表（space_data）来创建场景
        for (cityName, spaceData) in space_data.data.items():
            DEBUG_MSG("spaceName:" + spaceData["场景名称"])
            space = KBEngine.createBaseLocally("Space",
                                               {
                                                   'name': cityName,
                                                   "cityName": cityName,
                                                   "spaceName": spaceData["场景名称"]
                                               })

    def loginToSpaceByName(self, spaceName, entityMailbox):
        """
        通过Space名称登录到Space
        :param spaceName:
        :param entityMailbox:
        :return:
        """
        DEBUG_MSG("SpacesManager:loginToSpaceByName")
        KBEngine.globalData["space_" + spaceName].loginSpace(entityMailbox)

    def teleportToSpaceByName(self, spaceName, gateWayEntrancePosition, entityMailbox):
        """
        通过Space名称传送到Space
        :param spaceName:
        :param entityMailbox:
        :return:
        """
        DEBUG_MSG("SpacesManager:teleportToSpaceByName")
        entityMailbox.cell.isGoingToTeleport(spaceName, gateWayEntrancePosition)
        # KBEngine.globalData["space_" + spaceName].requestTeleport(entityMailbox)

    def logoutSpace(self, avatarID, spaceID):
        """
        defined method.
        某个玩家请求登出这个space
        """
        space = KBEngine.globalData["space_%i" % spaceID]
        space.logoutSpace(avatarID)
