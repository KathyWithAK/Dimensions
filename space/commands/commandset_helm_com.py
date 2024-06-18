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

###### COMMUNICATIONS CONTROLS ############################################

