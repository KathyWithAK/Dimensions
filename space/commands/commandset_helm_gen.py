from django.conf import settings
import re

import evennia 
from evennia import CmdSet, Command
from evennia.utils.evmenu import EvMenu
from evennia import EvForm
from evennia.contrib.rpg.health_bar import display_meter
from typeclasses.objects import Object

from space.typeclasses.shipmenu_library import titlecase, node_formatter, options_formatter
from world.space.models import SpaceDB
from space.utils.space_math import space_math
from space.utils import space_utils

###### GENERAL CONTROLS ###################################################

class CmdHelmBroadcast(Command):
    """
    Usage:

        broadcast <msg> - send a zone-wide message based on what is set in
                          helm.db.ship_zone on the ship Helm object.

        A broadcasted message will be sent to the contents of every room
        with the specified tag. Rooms should be set as follows:
        
        @tag room=<zone>:ShipZone
    
    """
    key ="broadcast"
    help_category = "Space"

    def func(self):
        args = self.args.strip()

        if not args:
            self.caller.msg("You must specify a message to broadcast.")
        else:
            if self.obj.db.ship_zone:
                rooms = evennia.search_tag(key=(self.obj.db.ship_zone), category='shipzone')
                for r in rooms:
                    r.msg_contents(f"BROADCAST from {self.caller.name}|n: {args}")
            else:
                self.caller.msg("You must set a zone for this ship in order to broadcast.")
