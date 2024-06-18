from django.conf import settings

import evennia
from evennia import CmdSet, Command
from evennia.utils.evmenu import EvMenu
from typeclasses.objects import Object
from evennia import EvForm
from evennia.contrib.rpg.health_bar import display_meter

from space.typeclasses.shipmenu_library import titlecase, node_formatter, options_formatter
from world.space.models import SpaceDB

"""
Ship Engine

    This is the fuel source of a ship.

    @create Engine:space.typeclasses.ship_engine.Engine

"""
class Engine(Object):
    """
    Primary class for ship engine objects.
    
    Lock engine from being stolen
        Ex. @lock <engine>=get:false()

    @create Engine:space.typeclasses.ship_engine.Engine
    @type/reset/force <obj>=space.typeclasses.ship_engine.Engine

    """
    def at_object_creation(self):
        super(Engine, self).at_object_creation()

        self.db.brand = "StellarCore SF-500"
        self.db.fuel_efficiency = 1000000 # kilometers per second (k/s)
        self.db.maximum_speed = 300000 # kilometers per second (k/s)
        self.db.current_speed = 0 # kilometers per second (k/s)\
        self.db.burn = 0 # ship's retro (reverse) thrust
        self.db.minimum_burn = 10000 # npu (Newtons per Update)
        self.db.maximum_burn = 100000000 # npu (Newtons per Update)
        self.db.retro = 0 # ship's forward thrust
        self.db.minimum_retro = 1000 # npu (Newtons per Update)
        self.db.maximum_retro = 5000000 # npu (Newtons per Update)
        self.db.status = -1 # 1-Online; 0-Standby; -1-Offline
        self.db.output = 100 # percent output of the engine

        self.db.desc = "A compact yet powerful solid fuel rocket engine designed for small spacecraft. Engineered by the renowned StellarTech Corporation, the SF-500 combines advanced materials and cutting-edge technology to offer reliable propulsion for a variety of missions, from short-range planetary hops to interstellar travel within nearby star systems. Its reliability and performance have earned it a legendary status among spacefarers, often referred to as the 'Workhorse of the Stars.'"
        #self.db.name = "StellarCore SF-500"         
        self.db.caption = "converts fuel to power the ship"

        #Engine objects may not be picked up. Adding a lock for this
        self.locks.add("get:false()")
        self.db.get_err_msg = "The engine is firmly bolted to the floor, to prevent thieves like you from walking away with it."

        # Add HELM commands to the helm object
        self.cmdset.add_default(ShipEngineCmdSet)

    def engine_start(self):
        self.db.status = 1
        self.db.output = 100

    def engine_stop(self):
        self.db.status = -1
        self.db.output = 0
        self.db.current_speed = 0
        self.db.burn = 0
        self.db.retro = 0

        # Also stop the SpaceDB object velocity
        results = evennia.search_object(f"#{self.id}", attribute_name="engine_obj")
        if len(results) > 0:
            helm_obj = results[0]
            ship_obj = helm_obj.get_ship()
            if ship_obj:
                ship = SpaceDB.objects.filter(db_item_id__exact=ship_obj.id)
                if len(ship) > 0:
                    ship[0].db_x_vel = 0
                    ship[0].db_y_vel = 0
                    ship[0].db_z_vel = 0

    def engine_standby(self):
        self.db.status = 0
        self.db.output = 50 # Output reduced by 50%
        self.db.burn = 0
        self.db.retro = 0

    # Property: engine_status
    @property
    def engine_status(self):
        engine_status_list = {
            -1: 'Off-Line',
            0: 'Standby',
            1: 'On-Line', }
        
        return {'status': self.db.status, 
                'desc': engine_status_list.get(self.db.status, 'Unknown')}

    # Property: engine_output
    @property
    def engine_output(self):
        if self.db.status >= 0:
            return self.db.output
        else: 
            return 0

    def get_helm(self):
        helm = evennia.search_object(f"#{self.id}", attribute_name="engine_obj")
        if len(helm) > 0:
            return helm[0]
        else:
            return None

    def return_appearance(self, looker, **kwargs):
        super(Engine, self).return_appearance(looker, **kwargs)
        looker.msg(self.get_display_desc(looker, **kwargs))
        self.return_engine_console(looker)

    def return_engine_console(self, looker):
        current_fuel = "N/A"
        burn = 0
        retro = 0
        
        # We need to locate the helm object
        helm = self.get_helm()
        if helm:
            ship_obj = helm.get_ship()

            current_fuel = display_meter(cur_value=ship_obj.db.current_fuel_capacity, 
                                max_value=ship_obj.db.max_fuel_capacity, empty_color="X", 
                                show_values=True, length=80, align="right")            

        form = EvForm("space.forms.form_engine_console")
        form.map(cells=
            {
                1:  self.db.brand,
                2:  self.engine_status['desc'],
                3:  f"{self.db.output}%",
                4:  f"{self.db.current_speed} km/s",
                5:  f"{current_fuel}",
                6:  f"{self.db.fuel_efficiency} km/s",
                7:  f"{burn:+.0f} (max: {self.db.maximum_burn:+.0f})",
                8:  f"{retro:+.0f} (max: {self.db.maximum_retro:+.0f})",
                9:  f"{self.db.maximum_speed} km/s",
            } )
        looker.msg(form)

class CmdEngEngineStart(Command):
    """
    Usage:
    
        start

        Starts the ship engine and brings output to 100%.
        While the engine is running, it will use fuel. If the fuel
        runs out, the engine will automatically stop.
    """
    key = "start"    

    def func(self):
        if self.obj.engine_status['status'] == 1:
            self.caller.msg(f"The engine is already running. Command failed.")
        else:
            # We need to locate the helm object
            helm = self.obj.get_helm()
            if helm:            
                self.obj.engine_start()
                self.obj.location.msg_contents(f"$You() started the engine.", from_obj=self.caller)
                helm.location.msg_contents(f"$You() started the engine.", from_obj=self.caller)

class CmdEngEngineStop(Command):
    """
    Usage:
    
        stop

        Stops the ship engine and brings output to 0%.
        While the engine is running, it will use fuel. If the fuel
        runs out, the engine will automatically stop.
    """
    key = "stop"

    def func(self):
        if self.obj.engine_status['status'] == 1:
            self.caller.msg(f"The engine is already running. Command failed.")
        else:
            # We need to locate the helm object
            helm = self.obj.get_helm()
            if helm:
                # Bring down all of the allocations to 0%
                helm.db.power_to_gen = 0
                helm.db.power_to_nav = 0
                helm.db.power_to_sci = 0
                helm.db.power_to_eng = 0
                helm.db.power_to_com = 0
                helm.db.power_to_tac = 0
                    
                self.obj.engine_stop()
                self.obj.location.msg_contents(f"$You() started the engine.", from_obj=self.caller)
                helm.location.msg_contents(f"$You() started the engine.", from_obj=self.caller)

class CmdEngEngineStandby(Command):
    """
    Usage:
    
        standby

        Starts the ship engine and brings output to 50%.
        While the engine is running, it will use fuel. If the fuel
        runs out, the engine will automatically stop.
    """
    key = "standby"

    def func(self):
        if self.obj.engine_status['status'] == 0:
                self.caller.msg(f"The engine is already on stand-by. Command failed.")
        else:
            # We need to locate the helm object
            helm = self.obj.get_helm()
            if helm:
                # Bring down all of the allocations by 50%
                helm.db.power_to_gen /= 2
                helm.db.power_to_nav /= 2
                helm.db.power_to_sci /= 2
                helm.db.power_to_eng /= 2
                helm.db.power_to_com /= 2
                helm.db.power_to_tac /= 2

                self.obj.engine_standby()
                self.obj.location.msg_contents(f"$You() set idled the engine.", from_obj=self.caller)
                helm.location.msg_contents(f"$You() has idled the engine.", from_obj=self.caller)

class ShipEngineCmdSet(CmdSet):
    key = "ShipEngineCmdSet"
    priority = 1

    def at_cmdset_creation(self):
        self.add(CmdEngEngineStart)
        self.add(CmdEngEngineStop)        
        self.add(CmdEngEngineStandby)
        