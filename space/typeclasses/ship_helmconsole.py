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
from space.utils import space_utils
from space.utils.space_math import space_math

from space.commands import commandset_helm_menu
from space.commands import commandset_helm_gen
from space.commands import commandset_helm_com
from space.commands import commandset_helm_eng
from space.commands import commandset_helm_nav
from space.commands import commandset_helm_sci
from space.commands import commandset_helm_tac

"""
Ship's Helm Console

    This is the command console of any given ship within the space system.
    It controls all of the main systems from the 'bridge' location of a ship.

"""
class ShipHelmConsole(Object):
    """
    This is the object that represents the helm. It should be created
    on the 'bridge' location of a given ship with in the space system.
    Without a helm, a ship cannot be controlled by users.

    @create Helm Console;console:space.typeclasses.ship_helmconsole.ShipHelmConsole
    @type/reset/force Helm=space.typeclasses.ship_helmconsole.ShipHelmConsole 

    You should also set three additional attributes on the Helm object in order
    it to function properly.

    1) Ship Object

        @create Ship:space.typeclasses.ship.Ship
        @set Helm/ship_obj=#<dbref of the ship object>

    2) Engine Object

        @create Engine:space.typeclasses.ship_engine.Engine
        @set Helm/engine_obj=#<dbref of the engine object>

    3) Zone Tag

        @tag room=<zone>:ShipZone
        @set Helm/ship_zone=<zone name>

    """
    def at_object_creation(self):
        super(ShipHelmConsole, self).at_object_creation()

        #Helm objects may not be picked up. Adding a lock for this
        self.locks.add("get:false()")
        self.db.get_err_msg = "The helm is firmly bolted to the floor, to prevent thieves like you from walking away with it."

        self.db.desc = "The helm console is a sleek, advanced control panel central to the operation of the starship. It features a wide array of holographic displays, touch-sensitive interfaces, and a variety of physical controls for precise maneuvering. The console is designed with ergonomic efficiency, allowing the navigator to manage complex starship functions with ease."
        self.db.caption = "allows access to ship systems"

        #References to objects used by the Helm
        self.db.ship_obj = None
        self.db.engine_obj = None
        self.db.ship_zone = None

        # Power allocation between systems
        self.db.power_to_gen = 30 # percent to General Functions
        self.db.power_to_nav = 30 # percent to Navigation
        self.db.power_to_sci = 0 # percent to Sciences
        self.db.power_to_eng = 10 # percent to Engineering
        self.db.power_to_com = 0 # percent to Communications
        self.db.power_to_tac = 30 # percent to Tactical

        self.db.max_view_distance = 80.4672 # in km (50 miles)
        self.db.max_sweep_distance = 160900000.34 # in km (100000000 miles)
        self.db.max_dock_distance = 1.61 # in km (1 mile)

        self.db.ship_bearing = 0.0 # in radians
        self.db.ship_pitch = 0.0 # in radians
        self.db.ship_roll = 0.0 # in radians

        # Add HELM commands to the helm object
        self.cmdset.add_default(ShipHelmCmdSet)  

    def get_engine(self):
        if not self.db.engine_obj:
            return None
        else:
            results = evennia.search_object(self.db.engine_obj)
            if len(results) == 1:
                return results[0]
            else:
                return None

    def get_ship(self): 
        if not self.db.ship_obj:
            return None
        else:
            results = evennia.search_object(self.db.ship_obj)
            if len(results) == 1:
                return results[0]
            else:
                return None
            
    def return_appearance(self, looker, **kwargs):
        super(ShipHelmConsole, self).return_appearance(looker, **kwargs)
        looker.msg(self.get_display_desc(looker, **kwargs))
        self.return_helm_console(looker)
    
    def return_helm_console(self, looker):
        # Check if a ship object has been associated with the helm
        ship_obj = self.get_ship()
        ship_obj_name = None
        if ship_obj:
            ship_obj_name = ship_obj.get_display_name(looker)

        # Check if a engine object has been associated with the helm
        engine_obj = self.get_engine()
        engine_obj_name = None
        engine_max_speed = None
        engine_cur_speed = None
        engine_burn = None
        engine_retro = None

        if engine_obj:
            engine_obj_name = engine_obj.get_display_name(looker)
            engine_obj_name = f"{engine_obj_name} ({engine_obj.engine_status['desc']})"
            engine_max_speed = engine_obj.db.maximum_speed
            engine_cur_speed = engine_obj.db.current_speed
            engine_burn = f"{engine_obj.db.burn} npu"
            engine_retro = f"{engine_obj.db.retro} npu"
        
        # Get the space object associated with the ship
        ref_obj = space_utils.get_space_obj_from_obj(ship_obj)
        if ref_obj:
            ship = ref_obj
            # Get ship-related data
            mass = ref_obj.db_mass 
            if ship_obj:
                mass = f"{int(float(mass) + float(ship_obj.db.current_fuel_capacity))} kg"
            else: 
                mass = f"{int(mass)} kg"
            x_coord = ref_obj.db_x_coord
            y_coord = ref_obj.db_y_coord
            z_coord = ref_obj.db_z_coord

        else:
            ship = None
            # Get ship-related data
            mass = None
            x_coord = None
            y_coord = None
            z_coord = None

        # Check for ship zone
        ship_zone = self.attributes.get("ship_zone", None)

        max_dock_distance = self.attributes.get("max_dock_distance", None)
        max_dock_distance_miles = float(max_dock_distance) / 1.609344 # convert to miles
        max_sweep_distance = self.attributes.get("max_sweep_distance", None)
        max_sweep_distance_miles = float(max_sweep_distance) / 1.609344 # convert to miles
        max_view_distance = self.attributes.get("max_view_distance", None)
        max_view_distance_miles = float(max_view_distance) / 1.609344 # convert to miles

        ship_bearing = self.attributes.get("ship_bearing", None)
        ship_pitch = self.attributes.get("ship_pitch", None)
        ship_roll = self.attributes.get("ship_roll", None)

        sm = space_math(self, engine_obj, ship_obj, ship)
        ship_velocity = sm.calculate_velocity(ship_bearing, ship_pitch)
        
        if ship_obj:
            fuel = display_meter(cur_value=ship_obj.db.current_fuel_capacity, 
                                max_value=ship_obj.db.max_fuel_capacity, empty_color="X", 
                                show_values=True, length=80, align="right")
        else: 
            fuel = ""

        form = EvForm("space.forms.form_helm_console")
        form.map(cells=
            {
                1:  f"{ship_obj_name}|n", 
                2:  f"{engine_obj_name}|n", 
                3:  f"{x_coord:+.0f}",
                4:  f"{y_coord:+.0f}",
                5:  f"{z_coord:+.0f}",
                7:  f"{ship_velocity[0]:+.4f}",
                8:  f"{ship_velocity[1]:+.4f}",
                9:  f"{ship_velocity[2]:+.4f}",
                11: f"{max_dock_distance:.1f} km ({max_dock_distance_miles:.1f} mi)",
                12: f"{max_sweep_distance:.1f} km ({max_sweep_distance_miles:.1f} mi)",
                13: f"{max_view_distance:.1f} km ({max_view_distance_miles:.1f} mi)",
                14: f"{ship_bearing:+.0f} r",
                16: f"{mass}",
                18: f"{ship_bearing:+.0f} r",
                19: f"{ship_pitch:+.0f} r",
                20: f"{ship_roll:+.0f} r",
                21: f"{engine_cur_speed:+.1f} km/s",
                22: ship_zone,
                23: ship.db_name,
                24: f"{engine_max_speed:+.1f} km/s",
                25: fuel,
                26: engine_burn,
                27: engine_retro,
            } )
        looker.msg(form)

class ShipHelmCmdSet(CmdSet):
    key = "ShipHelmCmdSet"
    priority = 1

    def at_cmdset_creation(self):
        self.add(commandset_helm_menu.CmdHelmMenu)

        self.add(commandset_helm_gen.CmdHelmBroadcast)

        self.add(commandset_helm_nav.CmdHelmNavDock)
        self.add(commandset_helm_nav.CmdHelmNavUndock)
        self.add(commandset_helm_nav.CmdHelmPlotCourse)
        self.add(commandset_helm_nav.CmdHelmSetBearing)
        self.add(commandset_helm_nav.CmdHelmSetBurn)
        self.add(commandset_helm_nav.CmdHelmSetRetro)        
        self.add(commandset_helm_nav.CmdHelmCourse)

        self.add(commandset_helm_sci.CmdHelmSweep)
        self.add(commandset_helm_sci.CmdHelmHistory)
        self.add(commandset_helm_sci.CmdHelmRecall)

        self.add(commandset_helm_eng.CmdHelmEngAllocate)
        self.add(commandset_helm_eng.CmdHelmEngEngineStart)
        self.add(commandset_helm_eng.CmdHelmEngEngineStandby)
        self.add(commandset_helm_eng.CmdHelmEngEngineStop)

        self.add(commandset_helm_tac.CmdHelmView)
        self.add(commandset_helm_tac.CmdHelmTactical)     
