# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug


class Skill:
    def __init__(self, spellCaster):
        KBEDebug.DEBUG_MSG("Skill:__init__")
        self.spellCaster = spellCaster

    def conjure(self, spellCaster):
        KBEDebug.DEBUG_MSG("Skill:conjure")

#----------------------------------------------------------------------------------------------
class SkillQ(Skill):
    def __init__(self, spellCaster, point):
        Skill.__init__(self, spellCaster)
        self.point = point

    def conjure(self, spellCaster):
        Skill.conjure(self, spellCaster)
        bullet = KBEngine.createEntity("Trigger", spellCaster.spaceID,
                                       spellCaster.position, spellCaster.direction, {})
        bullet.damage = 10
        bullet.moveToPointSample(self.point, 4, 1)
        商店 = {}

def 水电费(skill):
    def __init__(self, spellCaster, point):
        skill.__init__(self, spellCaster)
