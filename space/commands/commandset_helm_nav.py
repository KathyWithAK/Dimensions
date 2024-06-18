from django.conf import settings
import re
import math

import evennia 
from evennia import CmdSet, Command
from evennia.utils.evmenu import EvMenu
from evennia import EvForm
from evennia.contrib.rpg.health_bar import display_meter
from typeclasses.objects import Object

from space.typeclasses.shipmenu_library import titlecase, node_formatter, options_formatter
from world.space.models import SpaceDB
from space.utils.space_math import space_math
from space.utils import space_utils

###### NAVIGATION CONTROLS ################################################

class CmdHelmNavDock(Command):
    """
    Usage:

        Dock <obj>

        This will engage the automatic docking arm, to pull a space-bound object
        into a designated docking bay. In order for this to be successful, the
        following conditions must be met:

            1)  ship_obj attribue on the Helm you are using must be set to a 
                ship object (#<dbref>). The power_to_nav and max_dock_distance 
                attributes must also be set on the Helm.

            2)  the ship_obj must be in the SPACE_ROOM (in settings)

            3)  the space-bound object we are attempting to dock with needs to be
                linked to a room via db_dock_room.

        When successfully docked, a ship_obj will have its x,y,z coords reset to
        0,0,0, the velocity, heading, and roll will be set to 0, and the in_space
        flag for the ship_obj will be set to False.

    """
    key = "dock"
    help_category = "Space"

    def power_down_object(self, obj):        
        # Set the coords of ship_obj to 0
        obj.db_x_coord = 0
        obj.db_y_coord = 0
        obj.db_z_coord = 0
        # Set ship_obj speed to 0
        obj.db_x_vel = 0
        obj.db_y_vel = 0
        obj.db_z_vel = 0
        # Remove ship_obj from space
        obj.db_in_space = False
        #shipobj.save()

    def func(self):
        args = self.args.strip()

        if not args:
            self.caller.msg("What would you like to dock?")
        else:
            shipobj = self.obj.get_ship()
            
            if not shipobj:
                self.caller.msg(f"No ship object has been associated with {self.obj.name}|n. Command failed.")
                return
            else:
                if not shipobj.db_location_id == settings.SPACE_ROOM:
                    self.caller.msg("You are not in space. Command failed.")
                    return
                elif not self.obj.attributes.has("max_dock_distance"):
                    self.caller.msg("helm/max_dock_distance not set. Command failed.")
                    return
                elif not self.obj.attributes.has("power_to_nav"):
                    self.caller.msg("helm/power_to_nav not set. Command failed.")
                    return      
                elif self.obj.db.power_to_nav <= 0:
                    self.caller.msg("Cannot dock. No power allocated to navigation.")                              
                else:
                    dock_distance = self.obj.db.max_dock_distance * (self.obj.db.power_to_nav/100)
                    objs = space_utils.get_visible_space_objects(shipobj, dock_distance)
                    matches = []                    
                    for o in objs:
                        if o['object'].db_key.upper().__contains__(args.upper()):
                            matches.append(o)

                    if len(matches) == 0:
                            self.caller.msg(f"Could not find '{args}'.")
                    elif len(matches) > 1:
                        self.caller.msg(f"Multiple matches found for '{args}'.")
                    else:
                        dockobj = matches[0]['object']
                        ship_obj = shipobj.get_space_object(shipobj.dbid)
                        if not dockobj.db_dock_room:
                            self.caller.msg(f"{dockobj.db_name} is not dockable. Command failed.")
                        if not ship_obj.db_item_id:
                            self.caller.msg(f"No evennia object has been associated with {ship_obj.db_name}|n. Command failed.")                             
                        else:
                            dock = evennia.search_object(f"#{dockobj.db_dock_room}")
                            if len(dock) == 1:
                                dock=dock[0]
                            else:
                                self.caller.msg("Dock evennia room was not found. Command failed.")
                                return                            
                            ship = evennia.search_object(f"#{ship_obj.db_item_id}")
                            if len(ship) == 1:
                                ship=ship[0]
                            else:
                                self.caller.msg("Ship evennia object was not found. Command failed.")
                                return
 
                            self.obj.location.msg_contents(f"Docking to {dockobj.db_name}...")
                            self.power_down_object(ship_obj)    

                            # Send messages to everybody 
                            self.obj.location.msg_contents(
                                f"{ship.name}|n is moving through the {dockobj.db_name}|n docking bay.")
                            dock.msg_contents(
                                f"{ship.name}|n is moving through the {dockobj.db_name}|n docking bay.")
                            
                            # Move the ship object to dock
                            shipobj.move_to(dock, move_type="dock")
                            ship_obj.db_in_space = False
                            ship_obj.save()

class CmdHelmNavUndock(Command):
    """
    Usage:

        Undock / Launch

        This will undock a ship from a docking bay. In order for this to be 
        successful, the following conditions must be met:

            1)  ship_obj attribute on the Helm you are using must set to a ship 
                object (#<dbref>)

            2)  the ship_obj cannot already be in the SPACE_ROOM (in settings)

            3)  the ship_obj location must be linked to a space object 
                via SpaceDB.db_dock_room (#)

        When successfully undocked, a ship_obj will be set to the x,y,z coords
        of the dock_room space object, with velocity set to 0.
        
    """
    key = "undock"
    aliases = ["launch"]
    help_category = "Space"

    def func(self):
        shipobj = self.obj.get_ship()

        if not shipobj:
            self.caller.msg(f"No ship object has been associated with {self.obj.name}|n. Command failed.")
        else:
            if shipobj.db_location_id == settings.SPACE_ROOM:
                self.caller.msg("You are already in space. Command failed.")
            else:
                # Determine if there is a space object linked to the shipobj location
                dockobj = SpaceDB.objects.filter(db_dock_room__exact=shipobj.db_location_id)
                if len(dockobj) < 1:
                    self.caller.msg(f"No space object has been associated with {shipobj.location}|n. Command failed.")
                else:
                    # We now know the dock object, the ship object, and the helm. let's go to space
                    dockobj = dockobj[0]
                    self.do_undock(shipobj, dockobj, helmobj=self.obj)

    def build_space_obj(self, dbref, name, dbid):
        spaceobj=SpaceDB(db_key=dbref, db_category='object', db_name=name, 
        db_desc="A space object.", 
        db_mass="{:.50f}".format(float('50000000.0')), # standard starship weight
        db_radius="{:.50f}".format(float('0.0')),

        db_x_coord=int(float('0.0')), 
        db_y_coord=int(float('0.0')), db_z_coord=int(float('0.0')),
        db_x_vel=0, db_y_vel=0, db_z_vel=0,

        orbiting_body=None, 
        orbital_radius="{:.50f}".format(float(str('0.0'))), 
        orbital_period="{:.50f}".format(float(str('0.0'))),
        db_inclination = "{:.50f}".format(float(str('0.0'))),
        db_item_id = dbid,        
        ) # Mass in kg
        return spaceobj

    def do_undock(self, shipobj, dockobj, helmobj):
        # Determine if there is a ship object in the database representing ship_obj
        spaceobj = SpaceDB.objects.filter(db_item_id__exact=shipobj.id)
        if len(spaceobj) < 1:
            # We need to add a record to the space database and link it to our shipobj
            spaceobj=self.build_space_obj(shipobj.dbref, shipobj.name, shipobj.dbid)
            spaceobj.save()
        else:
            spaceobj = spaceobj[0]
            
        # Set the coords of the ship to match the coords of the dockobj
        spaceobj.db_x_coord = dockobj.db_x_coord
        spaceobj.db_y_coord = dockobj.db_y_coord
        spaceobj.db_z_coord = dockobj.db_z_coord
        # Set ship speed to 0
        spaceobj.db_x_vel=0
        spaceobj.db_y_vel=0
        spaceobj.db_z_vel=0
        # Put ship in space
        spaceobj.db_in_space = True
        spaceobj.db_desc=shipobj.db.desc
        spaceobj.save()

        # Send messages to everyone on ship
        helmobj.location.msg_contents(
            f"{shipobj.name}|n is moving through the {dockobj.db_name}|n docking bay.")
        shipobj.location.msg_contents(
            f"{shipobj.name}|n is moving through the {dockobj.db_name}|n docking bay.")
            
        # Locate space and Move the ship object to SPACEROOM
        SPACE_ROOM = evennia.search_object(f"#{settings.SPACE_ROOM}")[0]
        shipobj.move_to(SPACE_ROOM, move_type="undock")

class CmdHelmPlotCourse(Command):
    """
    Usage:

        plot

        Allow navigator to plot different courses before engaging a given course
        Possible plot options:

            /COORD -   Specify x,y,x - returns bearing, roll, speed, fuel needed
            /DEST  -   Specify distance, travel time, bearing, pitch 

    """
    key = "plot"
    help_category = "Space"

    def parse(self):
        # Handle the plot switches ( /coord, )
        self.option = self.args.strip()
    def func(self):
        # Get the necessary objects for calculations
        helm_obj = self.obj
        ship_obj = None
        ship = None

        # Check if a ship object has been associated with the helm
        if not helm_obj.attributes.has("ship_obj"):
            self.caller.msg(f"No ship object has been associated with {self.obj.name}. Command failed.")
            return

        # Search for the ship object
        ship_result = evennia.search_object(helm_obj.db.ship_obj)
        if not ship_result:
            self.caller.msg(f"No ship object has been associated with {self.obj.name}. Command failed.")
            return
        else:
            ship_obj = ship_result[0]

        # Get the space object associated with the ship
        ref_obj = space_utils.get_space_obj_from_obj(ship_obj)
        if ref_obj:
            ship = ref_obj
        else:
            self.caller.msg(f"No ship object has been associated with {self.obj.name}. Command failed.")
            return

        # Check if an engine object has been associated with the helm
        if not helm_obj.attributes.has("engine_obj"):
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return

        # Search for the engine object
        engine_result = evennia.search_object(helm_obj.db.engine_obj)
        if not engine_result:
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return
        else:
            engine_obj = engine_result[0]

        if engine_obj.engine_status['status'] == -1:
            self.caller.msg(f"The engine is not running. Command failed.")
            return

        # If we get here, then we have identified all of the objects we require
        sm = space_math(helm_obj, engine_obj, ship_obj, ship)

        if '/COORD' in self.option.upper():
            destination = yield("Please enter destination as x,y,z:")
            try:
                dest_coord = [float(x) for x in destination.split(",")]

                if len(dest_coord) == 3:
                    self.do_plot_coords(sm, dest_coord)
                else:
                    raise ValueError("Invalid number of coordinates. Please enter exactly three coordinates.")
            except ValueError as e:
                self.caller.msg(f"Invalid coordinates. Please enter a valid set of coordinates: {e}")

        elif '/DEST' in self.option.upper():
            distance = yield("Please enter total distance to travel (in kilometers):")
            if not distance.replace('.','',1).isdigit():
                self.caller.msg("Invalid distance. Command failed.")
                return
            bearing = yield("Please enter bearing (in radians):")
            bearing_deg = math.degrees(float(bearing))
            if not bearing.replace('.','',1).isdigit() and (bearing_deg > 0 and bearing_deg < 360):
                self.caller.msg("Invalid bearing. Command failed.")   
                return         
            pitch = yield("Please enter pitch (in radians):")
            pitch_deg = math.degrees(float(pitch))
            if not pitch.replace('.','',1).isdigit() and (pitch_deg > 0 and pitch_deg < 360):
                self.caller.msg("Invalid pitch. Command failed.")
                return            

            self.do_plot_dist(sm, distance, bearing, pitch)                   
        else:
            self.caller.msg(f"Unknown switch '{self.option}'.")
    
    def format_time(self, seconds: int) -> str:
        # Calculate days, hours, minutes, and remaining seconds
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)

        # Format the time string
        if days > 0:
            return f"{days}d {hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{hours:02}:{minutes:02}:{seconds:02}"

    def do_plot_coords(self, sm, destination):
        distance, fuel_cost, travel_time = sm.calculate_destination_based_on_coords(destination)
        
        bearing  = sm.get_bearing(destination)
        pitch = sm.get_pitch(destination)
        roll = sm.get_roll(destination, bearing, pitch)

        #trajectory = sm.calculate_trajectory(destination, distance, travel_time, seconds=0)
        display_bar = display_meter(cur_value=sm.current_fuel_capacity, 
                                    max_value=sm.max_fuel_capacity, 
                                    empty_color="x", show_values=True, 
                                    length=29, align="right")

        # Calculate trajectories / times
        trajectory = []
        for i in [0, 0.25, 0.5, 0.75, 1]:
            # Calculate time diff
            time = sm.convert_seconds_to_datetime(travel_time * i)
            # Calculate Interpolate Positions
            traj = str(sm.calculate_interpolate_position(i, destination))
            trajectory.append({"time": time, "traj": traj})

        form = EvForm("space.forms.form_plot_results")
        try:
            form.map(cells=
                {
                    1:  f"{int(sm.current_position[0]):+}",
                    2:  f"{int(sm.current_position[1]):+}",
                    3:  f"{int(sm.current_position[2]):+}",
                    4:  f"{int(destination[0]):+}",
                    5:  f"{int(destination[1]):+}",
                    6:  f"{int(destination[2]):+}",
                    7:  display_bar,
                    8:  f"{sm.fuel_efficiency} km/kg",
                    9:  f"{float(fuel_cost):3.0f} kg",
                    10: f"{float(distance):3.0f} km",
                    11: self.format_time(travel_time),
                    12: f"{float(bearing):+3.1f} r",
                    13: f"{float(roll):+3.1f} r", 
                    14: f"{float(pitch):+3.1f} r",
                    15: f"{sm.max_speed} km/s",
                    16: trajectory[0]['time'],
                    17: trajectory[0]['traj'],
                    18: trajectory[1]['time'],
                    19: trajectory[1]['traj'],
                    20: trajectory[2]['time'],
                    21: trajectory[2]['traj'],
                    22: trajectory[3]['time'],
                    23: trajectory[3]['traj'],
                    24: trajectory[4]['time'],
                    25: trajectory[4]['traj'],
                }
            )
            self.caller.msg(form)
        except Exception as ex:
            self.caller.msg(f"Error: {ex}")

    def do_plot_dist(self, sm, distance, bearing, pitch):        
        travel_time, fuel_cost, destination = sm.calculate_time_to_travel_distance(distance, bearing, pitch)
        roll = sm.get_roll(destination, bearing, pitch)

        #trajectory = sm.calculate_trajectory(destination, distance, travel_time, seconds=0)
        display_bar = display_meter(cur_value=sm.current_fuel_capacity, 
                                    max_value=sm.max_fuel_capacity, 
                                    empty_color="x", show_values=True, 
                                    length=29, align="right")

        # Calculate trajectories / times
        trajectory = []
        for i in [0, 0.25, 0.5, 0.75, 1]:
            # Calculate time diff
            time = sm.convert_seconds_to_datetime(travel_time * i)
            # Calculate Interpolate Positions
            traj = str(sm.calculate_interpolate_position(i, destination))
            trajectory.append({"time": time, "traj": traj})

        form = EvForm("space.forms.form_plot_results")
        form.map(cells=
                {
                    1:  f"{int(sm.current_position[0]):+}",
                    2:  f"{int(sm.current_position[1]):+}",
                    3:  f"{int(sm.current_position[2]):+}",
                    4:  f"{int(destination[0]):+}",
                    5:  f"{int(destination[1]):+}",
                    6:  f"{int(destination[2]):+}",
                    7:  display_bar,
                    8:  f"{sm.fuel_efficiency} km/kg",
                    9:  f"{float(fuel_cost):3.0f} kg",
                    10: f"{float(distance):3.0f} km",
                    11: self.format_time(travel_time),
                    12: f"{float(bearing):+3.1f} r",
                    13: f"{float(roll):+3.1f} r",
                    14: f"{float(pitch):+3.1f} r",
                    15: f"{sm.max_speed} km/s",
                    16: trajectory[0]['time'],
                    17: trajectory[0]['traj'],
                    18: trajectory[1]['time'],
                    19: trajectory[1]['traj'],
                    20: trajectory[2]['time'],
                    21: trajectory[2]['traj'],
                    22: trajectory[3]['time'],
                    23: trajectory[3]['traj'],
                    24: trajectory[4]['time'],
                    25: trajectory[4]['traj'],
                }
            )
        self.caller.msg(form)

class CmdHelmSetBearing(Command):
    """
    Usage:

        bearing <#>

        Set the ship's navigational bearing. Value must be a number 
        between 0 and 359.
    """
    key = "bearing"
    help_category = "Space"

    def func(self):
        if not self.args:
            self.caller.msg(f"Current bearing is set to {self.obj.db.ship_bearing:+} degrees.")
            return
        try:
            bearing = float(self.args)
            if 0 <= bearing <= 359:
                self.obj.db.ship_bearing = bearing
                self.caller.msg(f"Ship's bearing set to: {bearing:+} degrees.")
            else:
                self.caller.msg("Bearing value must be between 0 and 359.")
        except ValueError:
            self.caller.msg("Bearing value must be numeric.")

class CmdHelmSetPitch(Command):
    """
    Usage:

        pitch <#>

        Set the ship's navigational pitch. Value must be a number 
        between 0 and 359.
    """
    key = "pitch"
    help_category = "Space"

    def func(self):
        if not self.args:
            self.caller.msg(f"Current pitch is set to {self.obj.db.ship_pitch:+} degrees.")
            return        
        try:
            pitch = float(self.args)
            if 0 <= pitch <= 359:
                self.obj.db.ship_pitch = pitch
                self.caller.msg(f"Ship's pitch set to: {pitch:+} degrees.")
            else:
                self.caller.msg("Pitch value must be between 0 and 359.")
        except ValueError:
            self.caller.msg("Pitch value must be numeric.")

class CmdHelmCourse(Command):
    """
    Usage:

        course x,y,z
        
        Set a course to a specific destination. Ship's computer will then convert the
        course into heading, bearing, & pitch. In order to actually            
    """
    key = "course"
    help_category = "Space"

    def func(self):
        if not self.args:
            self.get_current_heading()
        else:
            parts = self.args.split(",")
            if len(parts) != 3:
                self.caller.msg("Invalid course format. Command failed.")
                return      
            destination = []      
            for part in parts:
                try:
                    destination.append(float(part))
                except ValueError:
                    self.caller.msg("Invalid course. Command failed.")
                    return
            
            ship = self.obj.get_ship()
            if not ship:
                self.caller.msg(f"No space object has been associated with {self.obj.name}|n. Command failed.")
                return
            engine_obj = self.obj.get_engine()
            if not engine_obj:
                self.caller.msg(f"No engine object has been associated with {self.obj.name}|n. Command failed.")
                return                
            ship_result = evennia.search_object(self.obj.db.ship_obj)
            ship_obj = None
            if not ship_result:
                self.caller.msg(f"No ship object has been associated with {self.obj.name}. Command failed.")
                return
            else:
                ship_obj = ship_result[0]

            if not ship_obj.db_location_id == settings.SPACE_ROOM:
                self.caller.msg("You are not in space. Command failed.")
                return            

            self.set_current_heading(engine_obj, ship_obj, ship, destination)

    def set_current_heading(self, engine_obj, ship_obj, ship, destination):
        sm = space_math(self.obj, engine_obj, ship_obj, ship)
        try:
            bearing = sm.get_bearing(destination)
            pitch = sm.get_pitch(destination)
            roll = sm.get_roll(destination, bearing, pitch)
        except Exception as ex:
            self.caller.msg("Error calculating course.")
        
        self.obj.db.ship_bearing = float(bearing)
        self.obj.db.ship_pitch = float(pitch)
        self.obj.db.ship_roll = float(roll)

        self.caller.msg(f"Setting course to: {destination}")

    def get_current_heading(self):
        pass

class CmdHelmSetBurn(Command):
    """
    Usage:

        burn <#>

        Fire the ship's main engines to increase the ship's forward thrust. Setting
        burn to 0 will reduce the thrust to zero (although the engines will technically
        remain 'on')
    """
    key = "burn"
    help_category = "Space"

    def func(self):

        # Check if a engine object has been associated with the helm
        if not self.obj.attributes.has("engine_obj"):
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return
        
        # Search for the engine object
        engine_result = evennia.search_object(self.obj.db.engine_obj)
        if not engine_result:
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return        
        else:
            engine_obj = engine_result[0]   

        if not engine_obj.attributes.has("current_speed"):
            self.caller.msg("engine/current_speed not set. Command failed.")
            return
        if not engine_obj.attributes.has("maximum_speed"):
            self.caller.msg("engine/maximum_speed not set. Command failed.")
            return
        if not engine_obj.attributes.has("minimum_burn"):
            self.caller.msg("engine/minimum_burn not set. Command failed.")
            return        
        if not engine_obj.attributes.has("maximum_burn"):
            self.caller.msg("engine/maximum_burn not set. Command failed.")
            return        
        if engine_obj.engine_status['status'] == -1:
            self.caller.msg("Engine is offline. Command failed.")
            return

        if not self.args:
            self.caller.msg(f"Current burn is set to {engine_obj.db.burn} npu (Newtons per Update).")
            return        
        try:
            burn = float(self.args)
            if engine_obj.db.minimum_burn <= burn <= engine_obj.db.maximum_burn:
                engine_obj.db.burn = burn
                self.caller.msg(f"Ship's burn set to: {burn:+} npu (Newtons per Update).")
            elif burn == 0:
                engine_obj.db.burn = burn
                self.caller.msg(f"Ship's burn set to: {burn:+} npu (Newtons per Update).")                
            else:
                self.caller.msg(f"Burn value must be between {engine_obj.db.minimum_burn} npu and {engine_obj.db.maximum_burn} npu.")
        except ValueError:
            self.caller.msg("Burn value must be numeric.")

class CmdHelmSetRetro(Command):
    """
    Usage:

        retro <#>

        Retro rockets are small rockets that face the opposite direction from the ship's
        main engines. 
    """
    key = "retro"
    help_category = "Space"

    def func(self):

        # Check if a engine object has been associated with the helm
        if not self.obj.attributes.has("engine_obj"):
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return
        
        # Search for the engine object
        engine_result = evennia.search_object(self.obj.db.engine_obj)
        if not engine_result:
            self.caller.msg(f"No engine object has been associated with {self.obj.name}. Command failed.")
            return        
        else:
            engine_obj = engine_result[0]   

        if not engine_obj.attributes.has("current_speed"):
            self.caller.msg("engine/current_speed not set. Command failed.")
            return
        if not engine_obj.attributes.has("maximum_speed"):
            self.caller.msg("engine/maximum_speed not set. Command failed.")
            return
        if not engine_obj.attributes.has("minimum_retro"):
            self.caller.msg("engine/minimum_retro not set. Command failed.")
            return        
        if not engine_obj.attributes.has("maximum_retro"):
            self.caller.msg("engine/maximum_retro not set. Command failed.")
            return        
        if engine_obj.engine_status['status'] == -1:
            self.caller.msg("Engine is offline. Command failed.")
            return

        if not self.args:
            self.caller.msg(f"Current retro is set to {engine_obj.db.retro} npu (Newtons per Update).")
            return        
        try:
            retro = float(self.args)
            if engine_obj.db.minimum_retro <= retro <= engine_obj.db.maximum_retro:
                engine_obj.db.retro = retro
                self.caller.msg(f"Ship's retro set to: {retro:+} npu (Newtons per Update).")
            elif retro == 0:
                engine_obj.db.retro = retro
                self.caller.msg(f"Ship's retro set to: {retro:+} npu (Newtons per Update).")                
            else:
                self.caller.msg(f"Retro value must be between {engine_obj.db.minimum_retro} npu and {engine_obj.db.maximum_retro} npu.")
        except ValueError:
            self.caller.msg("Retro value must be numeric.")
