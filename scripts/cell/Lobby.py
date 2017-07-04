import KBEngine
from KBEDebug import *


class Lobby(KBEngine.Entity):
    def __init__(self):
        DEBUG_MSG("Lobby:__init__")
        KBEngine.Entity.__init__(self)
