import math
import decimal
from datetime import timedelta
import datetime

class space_math():

    def __init__(self):
        pass

    def __init__(self, helm_obj=None, engine_obj=None, ship_obj=None, ship=None):       
        self.helm_obj = helm_obj
        self.engine_obj = engine_obj
        self.ship_obj = ship_obj
        self.ship = ship

    # Property: total_mass
    @property
    def total_mass(self):
        try:
            return (float(self.ship.db_mass) + float(self.ship_obj.db.current_fuel_capacity))
        except:
            return 0.0
    
    # Property: orbital_radius
    @property
    def orbital_radius(self):
        try:
            return float(self.ship.db_orbital_radius)
        except:
            return 0.0

    @property
    def current_fuel_capacity(self):
        try:
            return (self.ship_obj.db.current_fuel_capacity)
        except:
            return 0.0

    @property
    def max_fuel_capacity(self):
        try:
            return (self.ship_obj.db.max_fuel_capacity)
        except:
            return 0.0
                    
    # Property: current_position
    @property
    def current_position(self):
        try:
            x, y, z = self.ship.db_x_coord, self.ship.db_y_coord, self.ship.db_z_coord
            return float(x), float(y), float(z)
        except AttributeError:
            return 0, 0, 0

    # Property: fuel_efficiency
    @property
    def fuel_efficiency(self):
        try:
            return (self.engine_obj.db.fuel_efficiency)
        except:
            return 0.0

    # Property: current_speed
    @property
    def current_speed(self):
        try:
            current_speed = (self.engine_obj.db.current_speed)
            return current_speed
        except:
            return 0.0

    # Property: max_speed
    @property
    def max_speed(self):
        try:
            maximum_speed = (self.engine_obj.db.maximum_speed)
            return maximum_speed
        except:
            return 0.0

    def convert_seconds(self, seconds):
        """
        Convert seconds to days, hours, minutes, and seconds.
        
        Parameters:
        seconds (int): The total number of seconds.
        
        Returns:
        tuple: A tuple containing days, hours, minutes, and seconds.
        """
        days = seconds // (24 * 3600)
        seconds %= (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return days, hours, minutes, seconds
    
    def convert_seconds_to_datetime(self, seconds):
        days = seconds // (24 * 3600)
        seconds %= (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        diff = timedelta(days=days, seconds=seconds, minutes=minutes, hours=hours)
        final_time = datetime.datetime.now() + diff
        return final_time.strftime("%m/%d/%Y, %H:%M:%S")

    def calculate_distance(self, origin, destination):
        x1, y1, z1 = origin
        x2, y2, z2 = destination
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        return distance

    def calculate_fuel_cost(self, distance, fuel_efficiency):
        fuel_cost = distance / fuel_efficiency
        return math.ceil(fuel_cost) # round up to nearest whole number

    def calculate_travel_time(self, distance, max_speed):
        travel_time = distance / max_speed
        return travel_time
    
    def calculate_destination_based_on_coords(self, destination):
        x1, y1, z1 = list(map(float, self.current_position))
        x2, y2, z2 = list(map(float, destination))

        # 1, Calculate distance between current and destination
        distance = self.calculate_distance(self.current_position, destination) # in km
        # 2. Calculate fuel cost
        fuel_cost = self.calculate_fuel_cost(distance, self.fuel_efficiency) # in kg
        # 3. Calculate the travel time at max speed
        travel_time = self.calculate_travel_time(distance, self.max_speed) # in km/s

        return distance, fuel_cost, travel_time

    def get_bearing(self, destination):
        """
        Calculate bearing: with destination coords, func can determine the bearing between source
        and destination. Destination should be in [ X, y, z] format.
        """
        # Calculate deltas
        delta_x = destination[0] - self.current_position[0]
        delta_y = destination[1] - self.current_position[1]
        delta_z = destination[2] - self.current_position[2]
        # Calculate bearing
        bearing = math.degrees(math.atan2(delta_y, delta_x))

        if bearing < 0:
            bearing += 360 # Normalize bearing to be between 0 and 360 degrees
        return math.radians(bearing)
    
    def get_approach_bearing(self, destination):
        """
        Calculate approach bearing: with destination coords, func can determine the bearing between
        source and destination. Destination should be in [ X, y, z] format.
        """
        # Calculate deltas
        delta_x = destination[0] - self.current_position[0]
        delta_y = destination[1] - self.current_position[1]
        delta_z = destination[2] - self.current_position[2]
        # Calculate horizontal distance
        horizontal_distance = math.sqrt(delta_x**2 + delta_y**2)
        # Calculate hypotenuse 
        hypotenuse = math.sqrt(horizontal_distance**2 + delta_z**2)
        # Calculate approach bearing
        try:
            approach_bearing = math.degrees(math.asin(delta_z / hypotenuse))
        except:
            # Incase objects are ontop of each other
            approach_bearing = 0
        return math.radians(approach_bearing)

    def get_pitch(self, destination):
        """
        Calculate pitch: with destination coords, func can determine the pitch between between source
        and destination. Destination should be in [ X, y, z] format.
        """        
        # Calculate pitch
        delta_x = destination[0] - self.current_position[0]
        delta_y = destination[1] - self.current_position[1]
        delta_z = destination[2] - self.current_position[2]
        horizontal_distance = math.sqrt(delta_x**2 + delta_y**2)
        pitch = math.degrees(math.atan2(horizontal_distance, delta_z))
        return math.radians(pitch)

    def get_roll(self, destination, bearing, pitch):
        """
        Calculate roll: with destination coords, func can determine the roll between source
        and destination. Destination should be in [ x, y, z] format.
        """
        bearing = float(bearing)
        pitch = float(pitch)          
        # Calculate the direction cosins using bearing and pitch
        cosine_x = math.cos(bearing) * math.cos(pitch)
        cosine_y = math.sin(bearing) * math.cos(pitch)
        cosine_z = math.sin(pitch)
        # Calculate the roll (bank) angle
        roll = math.degrees(math.atan2(cosine_y, cosine_x))
        return math.radians(roll)

    def calculate_interpolate_position(self, fraction, destination):
        xf = self.current_position[0] + (fraction * (destination[0] - self.current_position[0]))
        yf = self.current_position[1] + (fraction * (destination[1] - self.current_position[1]))
        zf = self.current_position[2] + (fraction * (destination[2] - self.current_position[2]))
        return math.ceil(xf), math.ceil(yf), math.ceil(zf)

    def calculate_velocity(self, bearing, pitch, origin=None, speed=None):
        if not origin:
            origin = self.current_position
        if not speed:
            speed = self.current_speed

        # 1. Calculate the direction cosines
        cx = math.cos(bearing) * math.cos(pitch)
        cy = math.sin(bearing) * math.cos(pitch)
        cz = math.sin(pitch)
        # 2. Calculate the velocity vector
        vx = speed * cx
        vy = speed * cy
        vz = speed * cz

        return float(vx), float(vy), float(vz)
    

    def calculate_velocity_orbitting(self, mass, orbital_radius, position):
        gravitational_constant = 6.67430e-11
        # Calculate orbital speed
        try:
            orbital_speed = math.sqrt(gravitational_constant * float(self.total_mass) / orbital_radius)
        except:
            orbital_speed = 0
        # Calculate Theta
        try:
            theta = math.atan(position[0] / position[1])
        except:
            theta = 0
        # Calculate Phi 
        try:
            phi = math.atan(math.sqrt(position[0]**2 + position[1]**2) / position[2])
        except:
            phi = 0
        # Calculate velocity vector
        vx = orbital_speed * math.cos(theta) * math.cos(phi)
        vy = orbital_speed * math.cos(theta) * math.sin(phi)
        vz = orbital_speed * math.sin(theta)
        
        return vx, vy, vz


    def calculate_time_to_travel_distance(self, distance, bearing, pitch):
        bearing = float(bearing)
        pitch = float(pitch)
        distance = float(distance)
        # 1. Calculate time to travel distance
        total_time = self.calculate_travel_time(float(distance), float(self.max_speed)) # in seconds
        # 2. Calculate fuel consumption
        fuel_cost = self.calculate_fuel_cost(float(distance), self.fuel_efficiency) # in kg
        # 3. Calculate direction cosines
        cx = math.cos(bearing) * math.sin(pitch)
        cy = math.sin(bearing) * math.sin(pitch)
        cz = math.cos(pitch)
        # 4. Calculate final position corrds
        final_location = [ 
            self.current_position[0] + (cx * distance),
            self.current_position[1] + (cy * distance),
            self.current_position[2] + (cz * distance)
        ]
        return total_time, fuel_cost, final_location    
    
    def calculate_trajectory(self, destination, distance, travel_time, seconds=0):
        # 1. Calculate speed
        speed = float(distance) / float(travel_time)
        # 2. Calculate directional cosines
        dx = destination[0] - self.current_position[0]
        dy = destination[1] - self.current_position[1]
        dz = destination[2] - self.current_position[2]
        horizontal_distance = math.sqrt((dx**2 + dy**2))
        hypotenuse = math.sqrt((horizontal_distance**2 + dz**2))
        cx = dx / horizontal_distance
        cy = dy / horizontal_distance
        cz = dz / hypotenuse
        # 4. Calculate trajectory coords
        trajectory_x = float((speed * seconds * cx) + self.current_position[0])
        trajectory_y = float((speed * seconds * cy) + self.current_position[1])
        trajectory_z = float((speed * seconds * cz) + self.current_position[2])

        return math.ceil(trajectory_x), math.ceil(trajectory_y), math.ceil(trajectory_z)

    