# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class Task(object):
    def __init__(self):
        object.__init__(self)
        DEBUG_MSG("Task:__init__")
        self.npcInfo = {'NpcSpace': '', 'NpcName': ''}
        self.taskIndex = 0

    def detectTaskCompleteness(self):
        pass
