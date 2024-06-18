from django.conf import settings

import evennia 
from datetime import datetime
from evennia import CmdSet, Command
from evennia.utils import evtable
from evennia import EvForm

from space.utils import space_utils
from space.utils.space_math import space_math
from world.space.models import SpaceContactDB

class CmdHelmSweep(Command):
    """
    Usage:

            sweep
            
            Sweep the area for contacts and record them in the helm database.
            Existing contacts that are found will also be updated. The sweep
            command will only work while ship_obj is in the space room.

    """
    key = "sweep"
    aliases = ["scan"]
    help_category = "Space"

    def func(self):
        if not self.obj.db.ship_obj:
            self.caller.msg(f"No ship object has been associated with {self.obj.name}. Command failed.")
            return
        
        # Display while in space
        shipobj = self.obj.get_ship()
        if not shipobj.db_location_id == settings.SPACE_ROOM:
            self.caller.msg(f"You are not in space. Command failed.")
        elif not self.obj.attributes.has("max_view_distance"):
            self.caller.msg("helm/max_view_distance is not set")
        elif not self.obj.attributes.has("power_to_sci"):
            self.caller.msg("helm/power_to_sci is not set")
        elif self.obj.db.power_to_sci <= 0:
            self.caller.msg("Cannot sweep. No power allocated to sciences.")            
        else:

            # Get the space object associated with the ship
            ref_obj = space_utils.get_space_obj_from_obj(shipobj)
            if ref_obj:
                ship = ref_obj
            else:
                self.caller.msg(f"No ship object has been associated with {self.obj.name}. Command failed.")
                return
            
            sweep_distance = self.obj.db.max_sweep_distance * (self.obj.db.power_to_sci/100)
            objs = space_utils.get_visible_space_objects(shipobj, sweep_distance)                
            self.caller.msg(f"Sweep found {len(objs)} contacts.")

            sm = space_math(self.obj, None, shipobj, ship)
            for o in objs:
                contacts = space_utils.get_all_helm_contacts(self.obj, o)
                if len(contacts) > 0:
                    self.update_contact(sm, o, contacts)
                else:
                    self.add_contact(sm, o)

    def build_contact_obj(self, helmobj, spaceobj):
        contact = SpaceContactDB(db_helm = helmobj,
                                db_space_obj = spaceobj)

        random_name = space_utils.random_contact_name()
        contact.db_key = random_name
        contact.db_history_name = random_name
        contact.db_date_updated = datetime.today().strftime('%Y-%m-%d %H:%M:%S')       
        contact.db_mass = float(spaceobj.db_mass)
        contact.db_radius = float(spaceobj.db_radius)
        contact.db_attraction = float('0.0')

        contact.db_x_coord = float(spaceobj.db_x_coord)
        contact.db_y_coord = float(spaceobj.db_y_coord)
        contact.db_z_coord = float(spaceobj.db_x_coord)

        contact.db_x_vel = float(spaceobj.db_x_vel)
        contact.db_y_vel = float(spaceobj.db_y_vel)
        contact.db_z_vel = float(spaceobj.db_z_vel)

        contact.db_distance = float('0.0')
        contact.db_bearing = float('0.0')
        contact.db_inclination = float('0.0')
        contact.db_approach_bearing = float('0.0')
        
        return contact
    
    def update_contact(self, sm, obj, contacts):        
        update_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        contact = contacts[0]
        dest_coords = []

        contact.db_date_updated = update_time

        contact.db_x_coord = float(obj['object'].db_x_coord)
        dest_coords.append(contact.db_x_coord)
        contact.db_y_coord = float(obj['object'].db_y_coord)
        dest_coords.append(contact.db_y_coord)
        contact.db_z_coord = float(obj['object'].db_z_coord)
        dest_coords.append(contact.db_z_coord)

        contact.db_distance = float(obj['distance'])
        contact.db_bearing = sm.get_bearing(dest_coords)
        contact.db_approach_bearing = sm.get_approach_bearing(dest_coords)

        vector = sm.calculate_velocity_orbitting(float(obj['object'].db_mass), float(obj['object'].orbital_radius), dest_coords)

        contact.db_x_vel = float(vector[0])
        contact.db_y_vel = float(vector[1])
        contact.db_z_vel = float(vector[2])

        contact.save()

    def add_contact(self, sm, obj):
        contact = self.build_contact_obj(self.obj, obj['object'])
        contact.db_distance = float(obj['distance'])

        dest_coords = []
        contact.db_x_coord = float(obj['object'].db_x_coord)
        dest_coords.append(contact.db_x_coord)
        contact.db_y_coord = float(obj['object'].db_y_coord)
        dest_coords.append(contact.db_y_coord)
        contact.db_z_coord = float(obj['object'].db_z_coord)
        dest_coords.append(contact.db_z_coord)

        vector = sm.calculate_velocity_orbitting(float(obj['object'].db_mass), float(obj['object'].orbital_radius), dest_coords)

        contact.db_x_vel = float(vector[0])
        contact.db_y_vel = float(vector[1])
        contact.db_z_vel = float(vector[2])

        contact.db_bearing = sm.get_bearing(dest_coords)
        contact.db_approach_bearing = sm.get_approach_bearing(dest_coords)

        contact.save()

class CmdHelmHistory(Command):
    """
    Usage:

            history            
            
            Display a list of contacts in the helm database. Objects are 
            listed in the order they were added.
    """
    key = "history"
    help_category = "Space"

    def func(self):
        contacts = space_utils.get_all_helm_contacts(self.obj)
        if len(contacts) > 0:
        
            table = evtable.EvTable("Contact", "Mass", "Radius", "Updated", corner_char=".")
            for contact in contacts:
                table.add_row(f"{contact.db_history_name}|n", 
                            f"{contact.db_mass:,.5g} kg",
                            f"{contact.db_radius:,.5g} km",
                            f"{contact.db_date_updated}")
            table.reformat(width=87, align="l")
            self.caller.msg(table)
        else:
            self.caller.msg("No contacts found. Please run a sweep to collect new contacts.")

class CmdHelmRecall(Command):
    """
    Usage:

            recall <contact>         
            
            Call up  the most recent, detailed information that has been aquired from
            a contact. Information for a contact is collected each time a contact is
            encountered during a sweep.
    """
    key = "recall"
    help_category = "Space"

    def func(self):
        if not self.args:
            self.caller.msg("Please specify a contact to recall.")
            return
        contact = space_utils.get_helm_contact(self.obj, self.args)
        if not contact:
            self.caller.msg("No contact was found.")
            return
        else:
            form = EvForm("space.forms.form_contact")
            form.map(cells=
                    {
                    1:  contact[0].db_history_name,
                    2:  f"{contact[0].db_x_coord:+.0f}",
                    3:  f"{contact[0].db_y_coord:+.0f}",
                    4:  f"{contact[0].db_z_coord:+.0f}",
                    5:  f"{contact[0].db_x_vel:+.0f}",
                    6:  f"{contact[0].db_y_vel:+.0f}",
                    7:  f"{contact[0].db_z_vel:+.0f}",
                    8:  f"{contact[0].db_bearing:+.0f} r",
                    9:  f"{contact[0].db_distance:.0f} km",
                    10: f"{contact[0].db_approach_bearing:+.0f} r",
                    11: f"{contact[0].db_radius:.2g} km",
                    12: f"{contact[0].db_mass:.2g} kg",
                    13: f"{contact[0].db_attraction:.0f}",
                    14: contact[0].db_date_updated,
                    15: f"{contact[0].db_inclination:.0f}",
                }
            )
        self.caller.msg(form)
