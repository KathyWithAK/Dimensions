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

###### ENGINEERING CONTROLS ###############################################

class CmdHelmEngEngineStart(Command):
    """
    Usage:
    
        engine-start

        Starts the ship engine and brings output to 100%.
        While the engine is running, it will use fuel. If the fuel
        runs out, the engine will automatically stop.
    """
    key = "engine-start"
    help_category = "Space"

    def func(self):
        if not self.obj.db.engine_obj:
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return
        
        engineobj = self.obj.get_engine()
        if engineobj:
            if engineobj.engine_status['status'] == 1:
                self.caller.msg(f"The engine is already running. Command failed.")
            else:
                engineobj.engine_start()
                engineobj.location.msg_contents(f"$You() started the engine.", from_obj=self.caller)
                self.obj.location.msg_contents(f"$You() started the engine.", from_obj=self.caller)

class CmdHelmEngEngineStop(Command):
    """
    Usage:
    
        engine-stop

        Stops the ship engine and brings output to 0%.
        While the engine is running, it will use fuel. If the fuel
        runs out, the engine will automatically stop.
    """
    key = "engine-stop"
    help_category = "Space"

    def func(self):
        if not self.obj.db.engine_obj:
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return
        
        engineobj = self.obj.get_engine()        
        if engineobj:
            if engineobj.engine_status['status'] == -1:
                self.caller.msg(f"The engine is already offline. Command failed.")
            else:
                # Bring down all of the allocations to 0%
                self.obj.db.power_to_gen = 0
                self.obj.db.power_to_nav = 0
                self.obj.db.power_to_sci = 0
                self.obj.db.power_to_eng = 0
                self.obj.db.power_to_com = 0
                self.obj.db.power_to_tac = 0

                engineobj.engine_stop()
                engineobj.location.msg_contents(f"$You() turned off the engine.", from_obj=self.caller)
                self.obj.location.msg_contents(f"$You() turned off the engine.", from_obj=self.caller)

class CmdHelmEngEngineStandby(Command):
    """
    Usage:
    
        engine-standby

        Starts the ship engine and brings output to 50%.
        While the engine is running, it will use fuel. If the fuel
        runs out, the engine will automatically stop.
    """
    key = "engine-standby"
    help_category = "Space"

    def func(self):
        if not self.obj.db.engine_obj:
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return
        
        engineobj = self.obj.get_engine()        
        if engineobj:
            if engineobj.engine_status['status'] == 0:
                self.caller.msg(f"The engine is already on stand-by. Command failed.")
            else:
                # Bring down all of the allocations by 50%
                self.obj.db.power_to_gen /= 2
                self.obj.db.power_to_nav /= 2
                self.obj.db.power_to_sci /= 2
                self.obj.db.power_to_eng /= 2
                self.obj.db.power_to_com /= 2
                self.obj.db.power_to_tac /= 2

                engineobj.engine_standby()
                engineobj.location.msg_contents(f"$You() set idled the engine.", from_obj=self.caller)
                self.obj.location.msg_contents(f"$You() has idled the engine.", from_obj=self.caller)

class CmdHelmEngAllocate(Command):
    """
    Usage:

        allocate <section>=<% to allocate>

        Allocating engine output to a system will increase/decrease the
        performance of that system. For example, a scan at 100% will reach
        further into space than a scan at 20%. Some systems, like docking
        and broadcasting are either on or off, rather than functional to a
        percentage. Total allocation can never be < 0% or > 100%.
    """
    key = "allocate"
    help_category = "Space"

    valid_allocations = ['gen', 'nav', 'eng', 'com', 'tac', 'sci']

    def get_engine_output(self):
        engineobj = self.obj.get_engine()
        if engineobj:
            return engineobj.engine_output
        else:
            return 0

    def func(self):
        if not self.obj.db.engine_obj:
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return
                
        args = self.args.strip()
        if not args:
            self.do_display_allocations()
        else:
            args = args.split("=")
            if len(args) == 1:
                self.do_display_allocation_section(args[0])
            else:
                self.do_set_allocation(args[0], args[1])   

    def get_allocation_value(self, allocation):
        allocation = allocation.strip().lower()
        if allocation in self.valid_allocations:
            return self.obj.attributes.get(f"power_to_{allocation}")
        else:
            return -1

    def display_allocation(self, allocation, max_output):
        amt = self.get_allocation_value(allocation.lower())
        if amt < 0:
            amt = 0
        
        display_bar = display_meter(cur_value=amt, max_value=max_output, empty_color="X", 
                                    show_values=True, length=33, align="right")
        return display_bar
        
    def do_display_allocations(self):
        max_output = self.get_engine_output()

        self.caller.msg(" .----------------> Allocation <-----------.")
        self.caller.msg(" |                                         |")

        for a in self.valid_allocations:
            self.caller.msg(f" |  {a.upper()}  {self.display_allocation(a, max_output)} |")

        total = self.get_total_allocation()
        remaining = max_output-total
        if remaining < 0:
            remaining = 0
            
        self.caller.msg(" |                                         |")
        self.caller.msg(f" | Remaining: {float(remaining):3.0f}                          |")
        self.caller.msg(" '-----------------------------------------'")

    def do_display_allocation_section(self, allocation):
        allocation = allocation.strip()
        amt = self.get_allocation_value(allocation.upper())
        
        if amt >= 0:
            self.caller.msg(f"{allocation.upper()}: {self.display_allocation(allocation.lower())}")
        else:
            self.caller.msg(f"Unknown allocation '{allocation.upper()}'.")

    def get_total_allocation(self, exclude=None):
        total = 0
        for a in self.valid_allocations:
            attrib = f"power_to_{a}"
            if not attrib == exclude:
                total += self.obj.attributes.get(attrib, 0)
        return total

    def do_set_allocation(self, allocation, amount):
        allocation = allocation.strip().lower()
        max_output = self.get_engine_output()
        engineobj = self.obj.get_engine()
        
        if not amount.isnumeric():
            self.caller.msg("Allocation amount must be a number.")
            return
        amount = abs(int(amount))
        engine_status = engineobj.engine_status
        if engine_status['status'] < 0:
            self.caller.msg("Engine is not running.")
            return
        
        if allocation not in self.valid_allocations:
            self.caller.msg(f"Unknown allocation '{allocation.upper()}'.")
            return
        
        total = self.get_total_allocation(f"power_to_{allocation}")
        if total + amount > max_output:
            self.caller.msg(f"Cannot allocate more than current engine output, currently at {max_output}%.")
        else:
            self.obj.attributes.add(f"power_to_{allocation}", amount)
            self.caller.msg(f"Updating allocation -> {allocation.upper()}: {amount}%")
