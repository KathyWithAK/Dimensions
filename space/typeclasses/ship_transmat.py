from django.conf import settings

import evennia
from evennia import CmdSet, Command
from typeclasses.objects import Object
from evennia.utils import ansi
from evennia.utils.evmenu import EvMenu

from space.typeclasses.shipmenu_library import titlecase, node_formatter, options_formatter
from space.utils import space_utils
from world.space.models import SpaceDB

"""
Space trans-mat system

    The trans-mat system is used as an alternative to landing/docking
    vehicles in order to access a location in space. The platform will
    break down solid matter and then transmit it to a given location, where
    it is then re-constituted. There may only be one trans-mit pad per planet,
    ship, etc.

"""
class ShipTransmat(Object):
    """
    This object represents the trans-mat platform, the central operational
    mechanism of the transmat system. In order to use the trans-mat, there
    needs to be a recieving platform whereever you are attempting to 
    travel to. Use of a trans-mat without a destination could result in the
    destruction of the source matter.

        @create Trans-Mat Pad;transmat:space.typeclasses.ship_transmat.ShipTransmat
        @type/reset/force Trans-Mat=console:space.typeclasses.ship_transmat.ShipTransmat

    Note: In order for the transmat to operate, you need to also set the dbref
    number of the transmat in the SpaceDB.

        ex. SpaceDB('Sulaco').db_transmat = <evennia transmat id>
    
    """
    def at_object_creation(self):
        super(ShipTransmat, self).at_object_creation()

        #Trans-mat objects may not be picked up. Adding a lock for this
        self.locks.add("get:false()")
        self.db.get_err_msg = "The trans-mat is firmly bolted to the floor, to prevent thieves like you from walking away with it."

        self.db.desc = "This device is housed in a sleek, chrome-finished casing with intricate glowing circuits embedded along its surface. The device stands at about 7 feet tall, resembling a vertical sarcophagus with transparent panels that reveal a constantly shifting array of holographic interfaces and ethereal lights swirling within. Its form is a blend of sharp, angular lines and smooth curves, giving it a simultaneously ancient and ultra-modern feel. To use the transmat, type: TRANSMIT"
        self.db.caption = "can transmit matter across space"

        self.db.max_transmit_distance=100000000000 # in km

        # Add HELM commands to the helm object
        self.cmdset.add_default(ShipTransmatCmdSet)        

    def get_ship(self): 
        results = ship = SpaceDB.objects.filter(db_transmat__exact=self.id)
        if len(results) == 1:
            return results[0]
        else:
            return None

    def return_appearance(self, looker, **kwargs):
        super().return_appearance(looker, **kwargs)
        looker.msg(self.get_display_desc(looker, **kwargs))
        ship = self.get_ship()
        if ship:
            objs = space_utils.get_visible_space_objects(ship, self.db.max_transmit_distance, transmat=True)
            count = 0
            if len(objs) > 0:                
                looker.msg(" ")
                looker.msg(" .----------------> Destinations <----------.------------------------.----------------.")
                looker.msg(" |                                          |                        |                |")

                for o in objs:
                    count += 1
                    looker.msg(f" | {count:3d} ) {ansi.parse_ansi(o['object'].db_name, strip_ansi=True):34} | {float(o['distance']):19.2f} km | {o['object'].db_category:14} |")
                
                looker.msg(" '------------------------------------------'------------------------'----------------'")
                looker.msg(f" | Range: {float(self.db.max_transmit_distance):22.4f} km                                                   |")
                looker.msg(" '------------------------------------------------------------------------------------'")

    def move_to_destination(self, caller, raw_text, **kwargs):
        caller.msg("Ready to transport")
        destination_transmat = kwargs['destination']['object'].db_transmat
        destination = evennia.search_object(f"#{destination_transmat}")
        if destination:
            caller.location.msg_contents(f"$You()|n $conj(press) a large flashing button on the {self.name}|n and $conj(disappear).",from_obj=caller)

            if caller.move_to(destination[0].location, quiet=True, use_destination=True, move_type='move'):            
                # Tell everything in room that caller has gone
                destination[0].location.msg_contents(f"$You()|n $conj(materialize) on the nearby trans-mat pad.",from_obj=caller)             
        else:
            caller.msg("Destination unreachable. Transmit failed.")

        return "menu_ship_entry_exit"

class ShipTransmatCmdSet(CmdSet):
    key = "ShipTransmatCmdSet"
    priority = 1

    def at_cmdset_creation(self):
        self.add(ShipTransmatTransmit)

class ShipTransmatTransmit(Command):
    """
    Usage:

        transmit

        Lists possible destinations and then broadcasts matter to one of the 
        destinations.
    """
    key = "transmit"
    help_category = "Space"

    def func(self):
        # Check if a ship_obj has been associated with the trans-mat
        ship = self.obj.get_ship()
        if not ship:
            self.caller.msg(f"No ship_obj object has been associated with {self.obj.name}. Command failed.")
            return
        
        if not ship.db_in_space == 1:
            self.caller.msg("You are not in space. Command failed.")
            return           

        if not self.args:
            self.do_transmat_transmit(ship)

    def do_transmat_transmit(self, ship):
        objs = space_utils.get_visible_space_objects(ship, self.obj.db.max_transmit_distance, transmat=True)
        if len(objs) > 0:
            self.caller.ndb.objs = objs
            self.caller.ndb.transmat = self.obj
            EvMenu(self.caller, "space.typeclasses.ship_transmat",
                startnode="menu_transmat_entry",
                cmdset_mergetype="Replace",
                node_formatter=node_formatter,
                auto_help=True,
                auto_quit=True,
                options_formatter=options_formatter,
                cmd_on_exit=None
            )

def menu_transmat_entry(caller):
    objs = caller.ndb.objs
    transmat = caller.ndb.transmat
    text = f"Available destinations:"
    options = []
    count = 0

    for o in objs:
        count += 1
        option = {"key": str(count),
                "desc": f"{o['object'].db_name}|n",
                "goto": (transmat.move_to_destination, {"destination": o})
                }
        options.append(option)
    return text, tuple(options)

def menu_ship_entry_exit(caller):
    return "", None

