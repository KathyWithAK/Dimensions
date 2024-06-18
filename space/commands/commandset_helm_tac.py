from django.conf import settings
import re
import random
import numpy as np

import evennia 
from evennia import CmdSet, Command
from evennia.utils.evmenu import EvMenu
from evennia import EvForm
from evennia.contrib.rpg.health_bar import display_meter
from typeclasses.objects import Object

from space.typeclasses.shipmenu_library import titlecase, node_formatter, options_formatter
from world.space.models import SpaceDB
from world.space.models import SpaceContactDB
from space.utils.space_math import space_math
from space.utils import space_utils
import space.forms.viewscreen_art as art

###### TACTICAL CONTROLS ##################################################

class CmdHelmView(Command):
    """
    Usage:

        view - Look at the viewscreen for nearby objects

        view <obj> - Look at a single object nearby

        Note:
        
        While in space, a viewscreen at 100% will display all objects within 
        6.44 km (4 miles). While docked, a viewscreen will always display
        all objects visible in the current location.
    """
    key = "view"
    locks = "read:all()"
    help_category = "Space"

    def func(self):
        if not self.obj.db.ship_obj:
            self.caller.msg(f"No ship object has been associated with {self.obj.name}. Command failed.")
            return
        
        args = self.args.strip()
        if not self.obj.attributes.has("max_view_distance"):
            self.caller.msg("helm/max_view_distance is not set")
        elif not self.obj.attributes.has("power_to_tac"):
            self.caller.msg("helm/power_to_tac is not set")
        elif self.obj.db.power_to_tac <= 0:
            self.caller.msg("Cannot view. No power allocated to tactical.")
        else:
            if not args:
                self.do_general_view()
            else:
                self.do_specific_view(args)            

    def update_contact(self, helmobj, spaceobj):
        contact = SpaceContactDB.objects.filter(db_space_obj_id__exact=spaceobj.id, db_helm_id__exact=helmobj.id)
        if len(contact) > 0:
            contact = contact[0]
            contact.db_history_name = spaceobj.db_name
            contact.db_key = spaceobj.db_key
            contact.save()
        else:
            return

    def do_general_view(self):
        # Display while in space
        shipobj = self.obj.get_ship()
        
        if shipobj.db_location_id == settings.SPACE_ROOM:
            display_distance = self.obj.db.max_view_distance * (self.obj.db.power_to_tac/100)            
            objs = space_utils.get_visible_space_objects(shipobj, display_distance)

            self.caller.msg("You look at the viewscreen...")

            if len(objs) > 0:
                if objs[0]['distance'] <= display_distance:
                    self.get_art(objs[0]['object'].db_ascii_art)
                else:
                    found = False
                    for o in objs:
                        if o['object'].db_category == 'star':
                            self.get_art('STAR')
                            found = True
                            break
                    if not found:
                        self.get_art(None)
            else:
                self.get_art(None)

            #self.caller.msg(".----------------> Viewscreen <--------------------------------------------------------.")
            self.caller.msg(shipobj.location.get_display_name(self.caller))
            self.caller.msg(shipobj.location.db.desc)
            
            # Display distance is equal to max distance times percent Tactical (TAC) power used
            if len(objs) > 0:
                self.caller.msg("|wNearby Objects|n")
                for o in objs:
                    self.update_contact(self.obj, o['object'])
                    if self.caller.permissions.check("Builder"):
                        self.caller.msg(f" {o['object'].db_name}|n ({round(o['distance'],2)} km)")
                    else:
                        self.caller.msg(f" {o['object'].db_name}|n")

            #self.caller.msg("'--------------------------------------------------------------------------------------'")
        else:
            # Display while docked
            self.caller.msg("You look at the viewscreen...")
            self.get_art('DOCK')

            #self.caller.msg(".----------------> Viewscreen <--------------------------------------------------------.")
            self.caller.msg(shipobj.location.return_appearance(shipobj))
            #self.caller.msg("'--------------------------------------------------------------------------------------'")

    def get_art(self, img):
        art_map = {
            'ASTEROID': art.ASTEROID_1,
            'BLUE_PLANET': art.BLUE_PLANET,
            'COMET': art.COMET,
            'DOCK': random.choice([art.DOCK_1, art.DOCK_2]),
            'GREEN_PLANET': art.GREEN_PLANET,
            'LANDED': art.LANDED_1,
            'MOON': art.MOON_1,            
            'RED_PLANET': art.RED_PLANET,
            'RINGS': art.RINGS,
            'STAR': art.STAR,
            'STATION': art.STATION_1,            
        }
        if img in art_map:
            self.caller.msg(art_map[img])
        else:
            empty_space_arts = [art.EMPTY_SPACE_1, art.EMPTY_SPACE_2, art.EMPTY_SPACE_3, art.EMPTY_SPACE_4, art.EMPTY_SPACE_5]
            self.caller.msg(random.choice(empty_space_arts))

    def do_specific_view(self, args):
        # Display while in space
        shipobj = self.obj.get_ship()

        if shipobj.db_location_id == settings.SPACE_ROOM:
            display_distance = self.obj.db.max_view_distance * (self.obj.db.power_to_tac/100)
            objs = space_utils.get_visible_space_objects(shipobj, display_distance)
            matchs = []
            for o in objs:
                self.update_contact(self.obj, o['object'])
                if o['object'].db_key.upper().__contains__(args.upper()):
                    matchs.append(o)
            if len(matchs) == 0:
                self.caller.msg(f"Could not find '{args}'.")
            elif len(matchs) > 1:
                self.caller.msg(f"Multiple matches found for '{args}'.")
            else:
                self.caller.msg("You look at the viewscreen...")
                self.caller.msg(" ")
                #self.caller.msg(".----------------> Viewscreen <--------------------------------------------------------.")                    
                if self.caller.permissions.check("Builder"):
                    self.caller.msg(f"{o['object'].db_name}|n ({round(o['distance'],2)} km)")
                else:
                    self.caller.msg(f"{o['object'].db_name}|n")
                self.caller.msg(o['object'].db_desc)
                #self.caller.msg("'--------------------------------------------------------------------------------------'")
        else:
            # Display while docked
            obj = self.caller.search(args, candidates=shipobj.location.contents)
            if obj:
                self.caller.msg(".----------------> Viewscreen <--------------------------------------------------------.")
                self.caller.msg(obj.return_appearance(shipobj))
                self.caller.msg("'--------------------------------------------------------------------------------------'")
            else:
                pass

class CmdHelmTactical(Command):
    """
    Usage:

        tactical - Display a two-dimentional slice of space around
                   the ship

        Switches:
        
        /r <int>   - Adjust the range for scanning. Defaults to the 
                     max_view_distance in km. Max range avaliable is
                     ship's max_sweep_distance.

        /p <x,y,z> - Adjust the linear plane being displayed. Defaults
                     to current velocity vector of the ship. At a dead
                     stop, it defaults to 0,0,0

        /s<slice>  - Slice the coords on either xy, xz, or yz

        Note:
        
        While in space, a tactical display at 100% will display all objects
        within 24.44 km (16 miles). While docked, tactical is not avaliable.
    """
    key = "tactical"
    aliases = ["tac"]
    locks = "read:all()"
    help_category = "Space"

    map_scale = 75 # 75x75 plus border

    def parse(self):
        args = self.args.strip()
        if not args:
            return # Nothing to parse
        
        arg_list = args.split(' ')
        switch = arg_list[0].strip().lower()

        if switch == '/r':
            if len(arg_list) != 2:
                self.caller.msg("Invalid range. Input ignored.")
                return
            try:
                tac_range = int(arg_list[1])
                if tac_range <= 0 or tac_range > int(self.obj.db.max_sweep_distance * (self.obj.db.power_to_tac/100)):
                    self.caller.msg(f"Range is out of avaliable scope (1-{int(self.obj.db.max_sweep_distance * (self.obj.db.power_to_tac/100))}). Input ignored.")
                else:
                    self.obj.ndb.tac_range = tac_range
            except ValueError:
                self.caller.msg("Invalid range. Input ignored.")
        # elif switch == '/p':
        #     if len(arg_list) != 2:
        #         self.caller.msg("Invalid plane coords. Input ignored.")
        #         return
        #     coords_list = arg_list[1].split(',')
        #     if len(coords_list) != 3:
        #         self.caller.msg("Invalid plane coords. Input ignored.")
        #         return
        #     try:
        #         self.obj.ndb.tac_plane = [int(coord) for coord in coords_list]
        #     except ValueError:
        #         self.caller.msg("Invalid plane coords. Input ignored.")
        elif switch == '/s':
            if arg_list[1].strip().lower() in ['xy', 'xz', 'yz']:
                self.obj.ndb.tac_slice = arg_list[1].strip().lower()
        else:
            self.caller.msg("Unknown switch. Input ignored.")
        
    def func(self):
        if not self.obj.db.ship_obj:
            self.caller.msg(f"No ship object has been associated with {self.obj.name}. Command failed.")
            return
        shipobj = self.obj.get_ship()
        
        if not self.obj.attributes.has("max_view_distance"):
            self.caller.msg("helm/max_view_distance is not set")
            return
        elif not self.obj.attributes.has("power_to_tac"):
            self.caller.msg("helm/power_to_tac is not set")
            return
        elif self.obj.db.power_to_tac <= 0:
            self.caller.msg("Cannot view. No power allocated to tactical.")
            return

        if shipobj.db_location_id == settings.SPACE_ROOM:
            self.display_space_tactical(shipobj)
        else:
            self.caller.msg("You are not in space. Command failed.")
                
    def display_space_tactical(self, shipobj):
        space_obj = space_utils.get_space_obj_from_obj(shipobj)
        if not space_obj:
            self.caller.msg("No space object found. Command failed.")
            return
        
        # Get all of the objects ship can see at max distance        
        max_display_distance = int(self.obj.db.max_view_distance * (self.obj.db.power_to_tac/100))
        # Get range. If none, use the max view distance
        tac_range = int(self.obj.ndb.tac_range) if self.obj.ndb.tac_range else max_display_distance
        # Get slice direction
        tac_slice = self.obj.ndb.tac_slice if self.obj.ndb.tac_slice else 'xy'
        # Get all visible objects based on tac_range
        objs = space_utils.get_visible_space_objects(shipobj, tac_range, reverse=True)
        # Get plane. If none set, use the ship's current velocity
        tac_plane = self.obj.ndb.tac_plane if self.obj.ndb.tac_plane else [ int(space_obj.db_x_vel), int(space_obj.db_y_vel), int(space_obj.db_z_vel) ]
        # Get point on plane
        tac_point = [ int(space_obj.db_x_coord), int(space_obj.db_y_coord), int(space_obj.db_z_coord) ]

        map = self.draw_objects_in_ascii(objs, tac_point, tac_range, self.map_scale, tac_slice)
        self.caller.msg(map)

    def draw_objects_in_ascii(self, objs, tac_point, tac_range, map_scale, slice):
        # Define the size of the map
        map_width = 85
        map_height = 40
        center_x = map_width // 2  # Center x-coordinate of the 75x40 grid
        center_y = map_height // 2  # Center y-coordinate of the 75x40 grid

        # Initialize the map with empty spaces
        grid = [[' ' for _ in range(map_width)] for _ in range(map_height)]

        # Calculate the offset from the tac_point
        tac_x, tac_y, tac_z = tac_point

        # Get the largest X, Y, and Z coords in our array
        max_coords = [0, 0, 0]
        for obj in objs:
            coords = [abs(int(float(obj['object'].db_x_coord) - tac_x)),
                    abs(int(float(obj['object'].db_y_coord) - tac_y)),
                    abs(int(float(obj['object'].db_z_coord) - tac_z))]
            max_coords = [max(a, b) for a, b in zip(max_coords, coords)]

        # Use max coords to determine actual scale
        largest_integer = max(max_coords)
        if largest_integer == 0:
            largest_integer = 1 # account for a ZeroVisionError

        adjusted_coords = []
        for obj in objs:
            # Translate the object's coordinates relative to tac_point
            obj_x, obj_y, obj_z = float(obj['object'].db_x_coord), float(obj['object'].db_y_coord), float(obj['object'].db_z_coord)
            trans_x = (((obj_x - tac_x) * (map_scale // 2)) // largest_integer)
            trans_y = (((obj_y - tac_y) * (map_scale // 2)) // largest_integer)
            trans_z = (((obj_z - tac_z) * (map_scale // 2)) // largest_integer)

            # Project onto the xy-plane (can be changed to xz or yz if needed)
            if 'xz' in slice:
                
                proj_x = trans_x
                proj_y = trans_z                  
            elif 'yz' in slice:
                proj_x = trans_y
                proj_y = trans_z   
            else:
                proj_x = trans_x
                proj_y = trans_y                

            # Convert to integer coordinates for the grid
            grid_x = int(center_x + proj_x)
            grid_y = int(center_y - proj_y)  # Invert y to match typical grid orientation
            
            adjusted_coords.append((grid_y, grid_x))
            if 0 <= grid_x < map_width and 0 <= grid_y < map_height:
                category = obj['object'].db_category.lower()
                symbols = {
                    'star': '|y*|n',
                    'planet': '|c@|n',
                    'station': '|r#|n',
                    'moon': '|Co|n',
                    'asteroid': '|Y.|n'
                }
                grid[grid_y][grid_x] = symbols.get(category, '|m?|n')

        # Mark the tac_point on the map
        grid[center_y][center_x] = '|bT|n'

        # Create the ASCII representation of the grid
        ascii_map = "." + "-"*map_width + "."
        for a in range(map_height):
            row = "\n!"
            for b in range(map_width):
                row += grid[a][b]
            row += "!"
            ascii_map += row
        ascii_map += "\n'" + "-"*map_width + "'"


        ascii_map += f"\n  |wRange:|n {tac_range} km"
        ascii_map += f"\n  |wSlice:|n {slice[0].upper()},{slice[1].upper()}"
        ascii_map += f"\n  |wScale:|n {map_scale}:1 km"
        ascii_map += f"\n|wObjects:|n {len(objs)}" 

        return ascii_map
