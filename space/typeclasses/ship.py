
from django.conf import settings
from evennia import CmdSet, Command
from evennia.utils.evmenu import EvMenu
from typeclasses.objects import Object
from space.typeclasses.shipmenu_library import titlecase, node_formatter, options_formatter

from world.space.models import SpaceDB
"""
Ship

    This is the exterior ship object, which is used to track the
    position of 'ship' within the x,y,z coord space. When not within
    the 'Space' room, objs may 'enter' and 'exit' the ship object.

        @create Ship:space.typeclasses.ship.Ship

    SpaceDB ID

        SpaceDB('Ship').db_item_id = <evennia ship id>

    Entry List:

        @set <ship>/entry_list={'room': '#<room dbref>'}

    
    Note: To set the SpaceDB object, put the evennia ship object in
    a 'dock' room and then launch it using the ship's helm. This will
    automatically create the SpaceDB object representing the ship and
    connect it to Evennia.
"""

class ShipCmdSet(CmdSet):
    key = "ShipCmdSet"
    priority = 1

    def at_cmdset_creation(self):
        self.add(CmdEnterShip())

class CmdEnterShip(Command):
    """
    Ship objects default to having one airlock or docking bay, but may have multiple
    such rooms defined in self.db.entry_list. If more than one is defined, object attempting
    to enter the ship object will need to specify which entry to use.

    Usage:

        enter <ship>
    """
    key = "enter"
    locks = "cmd:not inspace()"    # Command cannot be used in the Space room. Caller is tested
    help_category = "Space"

    def func(self):    
        args = self.args.strip()
        if not args:
            self.caller.msg("Enter what?")
            return()  

        obj = self.caller.search(args)
        if obj:
            if obj.location == self.caller:
                # Object cannot enter something in its inventory
                self.caller.msg(f"You cannot enter {obj.name}|n while carrying it.")
            elif hasattr(obj, "at_enter_ship"):
                obj.at_enter_ship(self.caller)
            else:
                self.caller.msg("You don't know how to enter that.")
        else:
            self.caller.msg("You don't know how to enter that.")

def _menu_ship_entry_wrapper(caller, ship, obj):
    return lambda caller: ship.move_inside_ship(caller, obj)

def menu_ship_entry(caller):
    ship = caller.ndb.ship
    text = f"Available entrances to {ship.name}|n:"
    options = []
    count = 0

    for key in ship.db.entry_list.values():
        obj = caller.search(key, global_search=True, use_dbref=True)
        if obj:
            count += 1
            option = {"key": str(count),
                    "desc": "{}|n".format(obj.name),
                    "goto": (ship.move_inside_ship, {"destination": obj})
                    }
            options.append(option)
    return text, tuple(options)

def menu_ship_entry_exit(caller):
    return "", None

class Ship(Object):
    """
    Primary class for ship objects.
    
    Access enter the ship can be blocked using an "enter" lock.
        Ex. @lock <ship>=enter:false()

    @type/reset/force <obj>=space.typeclasses.ship.Ship

    @set #96/entry_list={'airlock1': '#99', 'airlock2': '#100'}

    """
    def at_object_creation(self):
        super(Ship, self).at_object_creation()

        # Ship objects may not be picked up. Add a lock for this
        self.locks.add("get:false()")
        self.locks.add("enter:all()")
        self.db.get_err_msg = "Even putting your back into it, there is just no way you could ever budge such an immensely heavy object."
        self.db.move_enter_ship_msg = None
        self.db.move_exit_ship_msg = None

        # Add a SHIP commands to the ship object
        self.cmdset.add_default(ShipCmdSet)

        self.db.entry_list = None

        self.db.max_fuel_capacity = 10000000000 # Units are measured by mass
        self.db.current_fuel_capacity = 10000000000 # Units are measured by mass

    def at_enter_ship(self, caller):
        # Handle entering ship
        if self.db.entry_list is None or len(self.db.entry_list) <= 0:
            caller.msg("There doesn't appear to be any way inside the ship.")
            return
        elif not self.access(caller, "enter"):
            caller.msg("You don't appear to have authorization to enter the {}|n.".format(self.name))
            return
        else:
            # If we are here, then caller can enter the ship. Now determine where they go.
            if len(self.db.entry_list) == 1:
                # There is only one entry. No need for a menu. Just try to push obj to location
                for val in self.db.entry_list.values():
                    # Pull whatever value is from the dict in attrib
                    pass
                if val:
                    obj = caller.search(val, global_search=True, use_dbref=True)
                    if obj:
                        self.move_inside_ship(caller, raw_text="", destination=obj)
                else:
                    caller.msg(f"There doesn't appear to be any way inside {self.name}|n.")
                    return
            else:
                # Build a EvMenu of possible entrances to use:   
                caller.ndb.ship = self           
                EvMenu(caller, "space.typeclasses.ship",
                    startnode="menu_ship_entry", 
                    cmdset_mergetype="Replace",
                    node_formatter=node_formatter,
                    auto_help=False,
                    auto_quit=False,
                    options_formatter=options_formatter,
                    cmd_on_exit=None
                )

    def move_inside_ship(self, caller, raw_text, **kwargs):
        # Send message to caller that they are entering
        if self.db.move_enter_ship_msg:
            caller.msg(self.db.move_enter_ship_msg)
        else:
            caller.msg("You cycle through the airlock, preparing to enter the ship...")
        destination = None
        if kwargs.get("destination"):
            destination = kwargs.get("destination")
        if caller.move_to(destination, quiet=True, use_destination=True):
            # Tell everything in room that caller has gone
            self.location.msg_contents("{}|n boarded {}|n.".format(
                caller.name, self.name), exclude=caller)                
        return "menu_ship_entry_exit"

    def get_space_object(self, id):
        spaceobj = SpaceDB.objects.filter(db_item_id__exact=id)
        if len(spaceobj) == 1:
            return spaceobj[0]
        else:
            return None
    
