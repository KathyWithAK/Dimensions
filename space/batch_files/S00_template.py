#
# To load the file, use: 
#     reload
#     @py from space.batch_files import 01_Initial_Solar_System; 01_Initial_Solar_System.initialize()
#
#

from world.space.models import SpaceDB
from decimal import Decimal

def create_celestial_body(key, category, name, 
                        mass, # kg
                        radius, # km
                        x, y, z, 
                        orbiting_body,
                        orbital_radius=0.0, #km
                        orbital_period=0.0, #days
                        inclination=0.0, #degrees
                        desc="A space object."):

    body=SpaceDB(db_key=key, db_category=category, db_name=name, 
                db_desc=desc, 
                db_mass="{:.50f}".format(float(mass)),
                db_radius="{:.50f}".format(float(radius)),

                db_x_coord=int(float(x)), 
                db_y_coord=y, db_z_coord=z,
                db_x_vel=0, db_y_vel=0, db_z_vel=0,

                orbiting_body=orbiting_body, 
                orbital_radius="{:.50f}".format(float(str(orbital_radius))), 
                orbital_period="{:.50f}".format(float(str(orbital_period))),
                db_inclination = "{:.50f}".format(float(str(inclination))),
                db_in_space = True,
                ) # Mass in kg
    return body
    
def initialize():
    print(" ")
    print("Initializing planets.")

    # Clear the existing data
    try:
        for o in SpaceDB.objects.all():
            o.delete()
    except:
        pass


    ### ADD SUNS / STARS #############################################

    ### ADD PLANETS ##################################################

    ### ADD MOONS ####################################################

    ### ADD SPACE STATIONS AND OTHER ORBITTING DEBRIS ################


    print(" ")
    print("Finished generating space objects.")
