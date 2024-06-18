from django.conf import settings
from typeclasses.exits import Exit

"""
ShipExit

    Ships require a special exit to (1) prevent objects from
    roaming into Space() rooms and (2) to send exiting objects to
    the location of the Ship object.

    @open |m<|gA|m>|girlock|n;a:space.typeclasses.ship_exit.ShipExit=here
    @type/reset/force #149=space.typeclasses.ship_exit.ShipExit
    
    @set <exit>/shipobject=#<ship object>

    @lock a=airlock:not inspace(#<ship object>)
    @set a/shipobject=#96

"""

class ShipExit(Exit):

    def at_object_creation(self):
        super(ShipExit, self).at_object_creation()
        #self.locks.add("airlock:inspace()")

    def at_traverse(self, traversing_object, target_location, **kwargs):
        #print(target_location)

        # Determine if ship object is defined
        if not self.db.shipobject:
            traversing_object.msg("The exit doesn't appear to go anywhere.")
            return

        # Determine if ship object exists
        ship_obj = self.search(self.db.shipobject, global_search=True, use_dbref=True)
        if not ship_obj:
            traversing_object.msg("The exit doesn't appear to go anywhere.")
            return    

        # Determine if object can pass the transverse lock. In order 
        # for this to work, the airlock:inspace() lock needs to be on the ship object,
        # then the test on 'caller' is also made on the ship object
        #if not ship_obj.access(ship_obj, "airlock"):
        if self.access(self, "airlock"):
            traversing_object.msg("The cold of space is all that awaits you through that door!")
            return

        # Send message to caller that they are entering
        if ship_obj.db.move_exit_ship_msg:
            traversing_object.msg(ship_obj.db.move_exit_ship_msg)
        else:
            traversing_object.msg("You cycle through the airlock, preparing to exit the ship...")

        if traversing_object.move_to(ship_obj.location, quiet=True, use_destination=True):
            # Tell everything in room that caller has gone
            traversing_object.location.msg_contents("{}|n exits from {}|n.".format(
                traversing_object.name, ship_obj.name), exclude=traversing_object)