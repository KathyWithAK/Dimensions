######
# 
# Ticker to move celestial bodies in space, other than things that can enter/leave regular game areas
#
#
# Usage:
#  @py evennia.create_script('space.scripts.space_ticker.SpaceTicker')
#
#  @py scr=evennia.search_script("spaceticker"); print(scr[0].start())
#  @py scr=evennia.search_script("spaceticker"); print(scr[0].stop())
#  @py scr=evennia.search_script("spaceticker"); print(scr[0].pause())
#  @py scr=evennia.search_script("spaceticker"); print(scr[0].unpause())
#
#  scripts/delete <script dbref>
#
#######################

import math

import evennia
from typeclasses.scripts import Script
from typeclasses.characters import Character

from world.space.models import SpaceDB
from space.utils import space_utils

class SpaceTicker(Script):

    def at_script_creation(self):
        self.key = "spaceticker"
        self.desc= "Ticker for moving celestial bodies"
        self.interval = 60 # Fire once a minute
        self.persistent = True

        self.repeats = 10 # After 10 cycles, stop script. 0 for infinite

    def update_celestial_body_position(self, obj, god):

        if obj.db_orbiting_body:
            
            # Calculate the angle of the orbiting body at time t
            time = self.interval
            orbital_radius = float(str(obj.db_orbital_radius))
            orbital_period = float(str(obj.orbital_period))
            inclination = float(str(obj.db_inclination))
            angle = 2 * math.pi * (time % orbital_period) / orbital_period

            obj.db_x_coord = float(obj.db_x_coord) + orbital_radius * math.cos(angle)
            obj.db_y_coord = float(obj.db_y_coord) + orbital_radius * math.sin(angle) * math.cos(inclination)
            obj.db_z_coord = float(obj.db_z_coord) + orbital_radius * math.sin(angle) * math.sin(inclination)
            obj.db_in_space = True

            # Save changes to database
            obj.save()

        # Do updates for everything orbiting this object
        orbiting_objects = SpaceDB.objects.filter(db_in_space__exact=1, db_orbiting_body__exact=obj)
        for oo in orbiting_objects:
            self.update_celestial_body_position(oo, god)

    def update_ship_position(self, obj, god):        
        if obj.db_in_space and obj.db_orbiting_body is None:
            if obj.db_item_id:
                # Get the helm object
                results = evennia.search_object(f"{obj.db_key}", attribute_name="ship_obj")
                if len(results) > 0:
                    helm_obj = results[0]
                    
                    # Get Ship_Obj object
                    ship_obj = helm_obj.get_ship()
                    if ship_obj:
                    
                        # Get the engine object
                        engine_obj = helm_obj.get_engine()
                        if engine_obj:

                            # We have everything we need. Let's calculate movement
                            self.calculate_ship_movement(obj, ship_obj, helm_obj, engine_obj, god)
                        
                        else:
                            space_utils(f"Engine not found for {helm_obj.get_display_name()}")
                    else:
                        space_utils(f"Ship_obj not found for {helm_obj.get_display_name()}")
                else:
                    space_utils(f"Helm not found for {obj.db_name|n}")

            else:
                # There is no helm. Just use SpaceDB info to move
                pass
    
    def calculate_ship_movement(self, ship, ship_obj, helm_obj, engine_obj, god):
        #god.msg("Made it here")
        """
        ship.db_x_coord = 10
        ship.db_y_coord = 20
        ship.db_z_coord = 30
        ship.db_x_vel = 0
        ship.db_y_vel = 0
        ship.db_z_vel = 0
        ship.db_mass = 50000000

        ship_obj.db.current_fuel_capacity = 100000

        engine_obj.db.output = 100
        engine_obj.db.maximum_speed = 5 km
        engine_obj.db.current_speed = 0 km
        engine_obj.db.fuel_efficiency = 10 km/s
        engine_obj.db.burn = 10000 newtons per update
        engine_obj.db.retro = 0 newtons per update
        engine_obj.db.status = 1 (online)

        helm_obj.db.ship_bearing = 0.8760580505981935
        helm_obj.db.ship_pitch = 0.8400523908061999
        helm_obj.db.ship_roll = 0.8760580505981935

        """
        # 1. Calculate thrust and acceleration
        net_thrust = float(engine_obj.db.burn) - float(engine_obj.db.retro)
        acceleration = net_thrust / ( float(ship.db_mass) + float(ship_obj.db.current_fuel_capacity) )

        # 2. Calculate the components of the acceleration
        ax = acceleration * math.cos(float(helm_obj.db.ship_pitch)) * math.cos(float(helm_obj.db.ship_roll))
        ay = acceleration * math.sin(float(helm_obj.db.ship_pitch))
        az = acceleration * math.cos(float(helm_obj.db.ship_pitch)) * math.sin(float(helm_obj.db.ship_roll))

        # 3. Calculate new velocities
        vx_new = float(ship.db_x_vel) + (ax * self.interval)
        ship.db_x_vel = vx_new
        vy_new = float(ship.db_y_vel) + (ay * self.interval)
        ship.db_y_vel = vy_new
        vz_new = float(ship.db_z_vel) + (az * self.interval)
        ship.db_z_vel = vz_new

        # 4. Calculate new coordinates
        x_new = float(ship.db_x_coord) + (vx_new * self.interval)
        ship.db_x_coord = x_new
        y_new = float(ship.db_y_coord) + (vy_new * self.interval)
        ship.db_y_coord = y_new
        z_new = float(ship.db_z_coord) + (vz_new * self.interval)
        ship.db_z_coord = z_new
        ship.save()

        # 5. Calculate increase/decrease in speed
        initial_speed = float(engine_obj.db.current_speed)
        new_speed = math.sqrt((vx_new**2) + (vy_new**2) + (vz_new**2))
        speed_diff = new_speed - initial_speed
        average_speed = (initial_speed + new_speed) / 2
        final_speed = float(engine_obj.db.current_speed) + speed_diff
        if final_speed < 0.0:
            # Never reduce speed below 0
            final_speed = 0.0
        elif final_speed > float(engine_obj.db.maximum_speed):
            # Never exceed maximum speed
            final_speed = float(engine_obj.db.maximum_speed)
        engine_obj.db.current_speed = final_speed

        # 6. Calculate fuel used
        distance_traveled = average_speed * self.interval
        #fuel_used = float(engine_obj.db.burn) * self.interval
        fuel_used = ((distance_traveled * float(engine_obj.db.burn)) + (distance_traveled * float(engine_obj.db.retro))) / float(engine_obj.db.fuel_efficiency)
        ship_obj.db.current_fuel_capacity = float(ship_obj.db.current_fuel_capacity) - fuel_used
        if float(ship_obj.db.current_fuel_capacity) <= 0:
            # Engine stalls because there is no fuel
            ship_obj.db.current_fuel_capacity = 0

            engine_obj.engine_stop()
            engine_obj.location.msg_contents(f"The engine has stalled due to lack of fuel.")
            helm_obj.location.msg_contents(f"The engine has stalled due to lack of fuel.")

    def at_repeat(self, **kwargs):

        # Get the god character for messaging
        char=Character.objects.filter(id=1)

        # Get a list of the different solar systems so we can loop through them       
        #solar_systems = SpaceDB.objects.order_by().values('db_solar_system').distinct()

        #for s in solar_systems:
        #    # Select everything from one solar system that is (1) in space and (2) has an orbital period
        #    celestial_bodies = SpaceDB.objects.filter(db_in_space__exact=1, db_solar_system__exact=s['db_solar_system']).exclude(db_orbital_period = 0)
        #    for body in celestial_bodies:
        #        self.update_celestial_body_position(body, god)             

        #        char[0].msg(f"{body.name}: x={body.x_coord}, y={body.y_coord}, z={body.z_coord}")

        # Get a list of the objects orbiting nothing but exclude 'objects' (ships) that are not orbitting
        celestial_bodies = SpaceDB.objects.filter(db_in_space__exact=1, db_orbiting_body=None).exclude(db_category='object')
        for c in celestial_bodies:
            self.update_celestial_body_position(c, char[0])
        
        # Get a list of the 'objects' (ships) not orbitting anything
        ships = SpaceDB.objects.filter(db_in_space__exact=1, db_orbiting_body=None, db_category='object')
        for s in ships:
            self.update_ship_position(s, char)
