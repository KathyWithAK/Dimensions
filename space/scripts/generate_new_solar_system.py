import random
import string
import math

###############
#
# Usage:
#   @py import space.scripts.generate_new_solar_system
#
# Example usage:
#   random_system = generate_random_system(0, 0, 0, num_planets=5, max_moons_per_planet=3, max_space_stations=10, max_space_rocks=3)
#
# Specify the coords of the star at the center of the system, how many planets, moons, and stations you want and
# script will randomly generate a dataset of the complete solar system.
#
###############

class CelestialBody:
    def __init__(self, name, mass, radius, x, y, z, orbiting_body=None, orbital_radius=0, orbital_period=0, inclination=0, obj_type=None):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = (x, y, z)
        self.orbiting_body = orbiting_body
        self.orbital_radius = orbital_radius
        self.orbital_period = orbital_period
        self.inclination = math.radians(inclination)  # Convert inclination to radians
        self.object_type = obj_type # star, planet, moon, station, etc
        self.orbiters = []

def generate_random_system(star_x, star_y, star_z, num_planets, max_moons_per_planet, max_space_stations, max_space_rocks):
    celestial_objects = []

    # Generate random star
    star_name = 'Star-' + ''.join(random.choices(string.ascii_uppercase, k=5))
    star_mass = random.uniform(1e30, 1e32)  # Random mass between 1e30 and 1e32 kg
    star_radius = random.uniform(500000, 2000000)  # Random radius between 500,000 km and 2,000,000 km
    star_orbital_radius = 0
    star_orbital_period = 0
    star_inclination = 0
    celestial_objects.append(CelestialBody(star_name, star_mass, star_radius, star_x, star_y, star_z, orbital_radius=star_orbital_radius, orbital_period=star_orbital_period, inclination=star_inclination, obj_type='star'))

    # Generate random planets
    for i in range(num_planets):
        planet_name = 'Planet-' + ''.join(random.choices(string.ascii_uppercase, k=5))
        planet_mass = random.uniform(1e24, 1e28)  # Random mass between 1e24 and 1e28 kg
        planet_radius = random.uniform(1000, 60000)  # Random radius between 1,000 km and 60,000 km
        planet_orbital_radius = random.uniform(1e8, 1e10)  # Random orbital radius between 100,000,000 km and 10,000,000,000 km
        planet_orbital_period = random.uniform(100, 10000)  # Random orbital period between 100 days and 10,000 days
        planet_inclination = random.uniform(0, 180)  # Random inclination between 0 and 180 degrees
        planet_x = star_x + planet_orbital_radius
        planet_y = star_y
        planet_z = star_z
        celestial_objects.append(CelestialBody(planet_name, planet_mass, planet_radius, planet_x, planet_y, planet_z, orbiting_body=celestial_objects[0], orbital_radius=planet_orbital_radius, orbital_period=planet_orbital_period, inclination=planet_inclination, obj_type='planet'))

        # Generate random moons
        num_moons = random.randint(0, max_moons_per_planet)
        for j in range(num_moons):
            moon_name = 'Moon-' + ''.join(random.choices(string.ascii_uppercase, k=5))
            moon_mass = random.uniform(1e20, 1e24)  # Random mass between 1e20 and 1e24 kg
            moon_radius = random.uniform(100, 3000)  # Random radius between 100 km and 3,000 km
            moon_orbital_radius = random.uniform(1000, 50000)  # Random orbital radius between 1,000 km and 50,000 km
            moon_orbital_period = random.uniform(10, 1000)  # Random orbital period between 10 days and 1,000 days
            moon_inclination = random.uniform(0, 180)  # Random inclination between 0 and 180 degrees
            moon_x = planet_x + moon_orbital_radius
            moon_y = planet_y
            moon_z = planet_z
            celestial_objects.append(CelestialBody(moon_name, moon_mass, moon_radius, moon_x, moon_y, moon_z, orbiting_body=celestial_objects[-1], orbital_radius=moon_orbital_radius, orbital_period=moon_orbital_period, inclination=moon_inclination, obj_type='moon'))

    # Generate random space stations
    for k in range(max_space_stations):
        station_name = 'SpaceStation-' + ''.join(random.choices(string.ascii_uppercase, k=5))
        station_mass = random.uniform(1e15, 1e18)  # Random mass between 1e15 and 1e18 kg
        station_radius = random.uniform(1, 100)  # Random radius between 1 km and 100 km
        orbiting_body = random.choice(celestial_objects[1:])  # Randomly select a planet or moon to orbit
        station_orbital_radius = random.uniform(1000, 50000)  # Random orbital radius between 1,000 km and 50,000 km
        station_orbital_period = random.uniform(1, 100)  # Random orbital period between 1 day and 100 days
        station_inclination = random.uniform(0, 180)  # Random inclination between 0 and 180 degrees
        station_x = orbiting_body.position[0] + station_orbital_radius
        station_y = orbiting_body.position[1]
        station_z = orbiting_body.position[2]
        celestial_objects.append(CelestialBody(station_name, station_mass, station_radius, station_x, station_y, station_z, orbiting_body=orbiting_body, orbital_radius=station_orbital_radius, orbital_period=station_orbital_period, inclination=station_inclination, obj_type='station'))

    # Generate random space rocks
    for k in range(max_space_rocks):
        station_name = 'SpaceRock-' + ''.join(random.choices(string.ascii_uppercase, k=5))
        station_mass = random.uniform(1e15, 1e18)  # Random mass between 1e15 and 1e18 kg
        station_radius = random.uniform(0.01, 1)  # Random radius between 0.01 km and 1 km
        orbiting_body = random.choice(celestial_objects[1:])  # Randomly select a planet or moon to orbit
        station_orbital_radius = random.uniform(100, 5000)  # Random orbital radius between 100 km and 5000 km
        station_orbital_period = random.uniform(1, 100)  # Random orbital period between 1 day and 100 days
        station_inclination = random.uniform(0, 180)  # Random inclination between 0 and 180 degrees
        station_x = orbiting_body.position[0] + station_orbital_radius
        station_y = orbiting_body.position[1]
        station_z = orbiting_body.position[2]
        celestial_objects.append(CelestialBody(station_name, station_mass, station_radius, station_x, station_y, station_z, orbiting_body=orbiting_body, orbital_radius=station_orbital_radius, orbital_period=station_orbital_period, inclination=station_inclination, obj_type='asteroid'))

    return celestial_objects

############################################################

random_system = generate_random_system(0, 0, 11812129476, num_planets=8, max_moons_per_planet=7, max_space_stations=3, max_space_rocks=5)

for obj in random_system:

    if obj.orbiting_body:
        orb_obj = obj.orbiting_body.name
    else:
        orb_obj = ""
        
    #print(f"{obj.name}: Mass = {obj.mass}, Orbiting Body = {orb_obj}, Radius = {obj.radius}, Position = {obj.position}, Orbital Radius = {obj.orbital_radius}, Orbital Period = {obj.orbital_period}, Inclination = {obj.inclination}")
    print(f"('{obj.name}', {obj.mass}, {obj.radius}, {obj.position}, {orb_obj}, orbital_radius={obj.orbital_radius}, orbital_period={obj.orbital_period}, inclination={obj.inclination}, obj_type='{obj.object_type}'),")
    
