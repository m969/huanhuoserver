# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import datetime
from interfaces.EntityObject import EntityObject


class Sectarian(KBEngine.Base, EntityObject):
    def __init__(self):
        KBEngine.Base.__init__(self)
        EntityObject.__init__(self)
        self.timerId = self.addTimer(1, 1, 0)  # 参数代表什么含义
