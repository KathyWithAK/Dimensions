from django.conf import settings
import re
import random
import string
import math

import evennia 
from evennia import CmdSet, Command
from evennia.utils.evmenu import EvMenu
from evennia import EvForm
from evennia.contrib.rpg.health_bar import display_meter
from typeclasses.objects import Object

from space.typeclasses.shipmenu_library import titlecase, node_formatter, options_formatter
from world.space.models import SpaceDB, SpaceContactDB
from space.utils.space_math import space_math

# HELPER FUNCTIONS #########################

def msg_space(msg):
    """
    Usage:

    Send error/info messages to the spaceinfo channel.
    """
    chan = evennia.search_channel("SpaceInfo")
    if chan:
        chan[0].msg(f"System: {msg}")

def get_space_obj_from_obj(obj):
    # Function to return the space object connected to a given evennia object
    ref_obj = None
    if isinstance(obj, SpaceDB):
        ref_obj = obj
    else:
        ref_obj = SpaceDB.objects.filter(db_key__exact=f"#{obj.dbid}")
        if len(ref_obj) <= 1:
            ref_obj = ref_obj[0]
    return ref_obj

def distance_between_space_objects(obj1, obj2):
    """
    Function to determine the spacial distance between this object and any given <obj>
    passed to it. Distance is in three-dimensions and is returned in kilometers (km).
    """
    ref_obj1 = get_space_obj_from_obj(obj1)
    ref_obj2 = get_space_obj_from_obj(obj2)
    
    if ref_obj1 and ref_obj2:
        if ref_obj1 == ref_obj2:
            return None 
        else:
            import math
            # Distance in kilometers (km)
            distance = math.sqrt((ref_obj2.db_x_coord - ref_obj1.db_x_coord)**2 + (ref_obj2.db_y_coord - ref_obj1.db_y_coord)**2 + (ref_obj2.db_z_coord - ref_obj1.db_z_coord)**2)
            if distance == 0.0:
                distance = 0.000000000000000000001 # No two objects can be in the same place
            return distance
    else:
        return None

def all_get_space_objects(shipobj, transmat=False):
    # Get all objects in space
    obj_can_see = []
    if transmat:
        objs_in_space = SpaceDB.objects.filter(db_in_space__exact=1, db_transmat__isnull=False)
    else:
        objs_in_space = SpaceDB.objects.filter(db_in_space__exact=1)
        
    for o in objs_in_space:
        dist = o.distance_between_space_objects(shipobj)
        if dist is not None:  # Ensure distance is valid
            obj_can_see.append({'object': o, 'distance': dist, 'mass': o.mass})
    return obj_can_see        

def get_visible_space_objects(shipobj, max_distance, transmat=False, reverse=False):
    objs = all_get_space_objects(shipobj, transmat)
    
    # Sort objects based on distance and mass (larger mass is easier to see)
    objs.sort(key=lambda x: (x['distance'], -x['mass']), reverse=reverse)  # -x['mass'] for descending mass
    
    found_objs = []
    for o in objs:        
        if transmat:
            # Account for visibility based on distance only
            if float(o['distance']) <= max_distance:
                found_objs.append(o.copy())         
        else:
            # Account for visibility based on distance AND size
            o_diameter = float(o['object'].db_radius) * 2
            #o_surface_area = 4 * ( float(o['object'].db_radius) ** 3)
            #o_volume = (4/3) * math.pi * ( float(o['object'].db_radius) ** 3)

            visibility_factor = o_diameter
            #visibility_factor += float(o['mass'])

            if float(o['distance']) <= max_distance + visibility_factor:
                found_objs.append(o.copy())               

    return found_objs

def random_contact_name():
    """
    Generate a random name in the format [character][character][character][character][character]-[integer][integer][integer].

    Returns:
    str: The generated random name.
    """
    # Generate 5 random characters
    characters = ''.join(random.choices(string.ascii_letters, k=5))
    # Generate 3 random integers
    integers = ''.join(random.choices(string.digits, k=3))
    # Combine characters and integers with a hyphen
    random_name = f"{characters}-{integers}"
    return random_name

def get_all_helm_contacts(helmobj, spacedb_id=None):
    # Get all objects in contact table
    obj_contacts = []
    if spacedb_id:
        obj_contacts = SpaceContactDB.objects.filter(db_space_obj_id__exact=spacedb_id['object'].id, 
                                                    db_helm__exact=helmobj.dbid)
    else:
        obj_contacts = SpaceContactDB.objects.filter(db_helm__exact=helmobj.dbid)
    return obj_contacts

def get_helm_contact(helmobj, contact_name):
    # Search for a single contact based on helm and name
    contact_name = contact_name.strip()
    obj_contacts = SpaceContactDB.objects.filter(db_helm__exact=helmobj.dbid, 
                                                db_key__startswith=contact_name)
    if len(obj_contacts) < 1:
        return None
    if len(obj_contacts) > 1:
        return None
    else: 
        return obj_contacts