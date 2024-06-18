from evennia import CmdSet, Command
from evennia import default_cmds
from evennia.utils import ansi
from typeclasses.rooms import Room

"""
Usage:
    @dig <space_room>: space.typeclasses.spaceroom.SpaceRoom

"""

class SpaceRoom(Room):
    """
    There is only one space room within the game. Objects placed in this
    room operate on X,Y,Z coords and move via each. Space is a vaccuum, so
    most commands do not work within the room.

    @type/reset/force here=space.typeclasses.spaceroom.SpaceRoom

    """
    def at_object_creation(self):
        super(SpaceRoom, self).at_object_creation()
        
        self.db.desc="Before you stretches an endless panorama of stars and galaxies, their shimmering light dancing across the darkness like a celestial symphony. Nebulae swirl and twist in cosmic ballets, their vibrant hues painting the vast canvas of space with splashes of color. In the distance, distant planets hang suspended in the void, their surfaces a patchwork of craters, mountains, and oceans gleaming beneath the gentle glow of distant suns. Asteroid fields drift lazily by, their rocky forms casting long shadows against the backdrop of eternity. Yet despite the breathtaking beauty of the cosmos, there is an underlying sense of danger lurking in the shadows. Solar flares erupt in brilliant bursts of energy, casting harsh light and intense radiation across the void. Black holes lurk like hungry predators, their gravitational pull threatening to swallow everything in their path."

