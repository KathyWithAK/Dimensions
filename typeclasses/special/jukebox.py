######
# 
# Ticker to move celestial bodies in space, other than things that can enter/leave regular game areas
#
#
# Usage:
#  @py evennia.create_script('space.scripts.space_ticker.SpaceTicker')
#
#######################

import evennia
from evennia import CmdSet, Command
from typeclasses.objects import Object

"""
Jukebox 

    Use to play discs containing lyrics to songs

"""
class Jukebox(Object):

    def at_object_creation(self):
        super(Jukebox, self).at_object_creation()

"""
JukeboxDisc 

    Discs containing lyrics to songs

"""
class Jukebox(Object):

    def at_object_creation(self):
        super(Jukebox, self).at_object_creation()

