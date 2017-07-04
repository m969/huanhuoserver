# -*- coding: utf-8 -*-
import KBEngine
import random
from KBEDebug import *
from interfaces.EntityObject import EntityObject

class Sectarian(KBEngine.Entity, EntityObject):
    def __init__(self):
        DEBUG_MSG("Sectarian:_init_")
        KBEngine.Entity.__init__(self)
        EntityObject.__init__(self)
        #KBEngine.globalData["sectarian_%i" % self.]
