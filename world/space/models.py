from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from evennia.utils.idmapper.models import SharedMemoryModel


__all__ = ("SpaceDB",)

_GA = object.__getattribute__
_SA = object.__setattr__
_DA = object.__delattr__

# Create your models here.
"""
Notes:

    from world.space.models import SpaceContactDB

    droplet = ItemDB.objects.get(db_key="red_droplet")
    print(f'{droplet.obj_id} - {droplet.name} - {droplet.caption}') 

    CREATE RECORD
    @py from world.space.models import SpaceContactDB; mars=SpaceContactDB(db_key="mars"); mars.save()

    DELETE RECORD
    @py from world.space.models import SpaceContactDB; match=SpaceContactDB.objects.filter(db_key__exact="mars"); match.delete()

"""
class SpaceContactDB(SharedMemoryModel):
    """
    A model used to store data collected from ship scans. This data is not live
    """
    db_key = models.CharField(max_length=80, db_index=True)
    db_history_name = models.CharField(max_length=80, null=True, blank=True)
    db_date_updated  = models.CharField(max_length=80, null=True, blank=True)

    ########################################################
    # Space-specific attributes
    ########################################################

    db_helm = models.ForeignKey(
        "objects.ObjectDB",
        null=True,
        verbose_name="object",
        on_delete=models.SET_NULL,
        help_text="the object that this space entry represents in the evennia db",)
    
    db_mass = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_radius = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_attraction = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)

    db_x_coord = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_y_coord = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_z_coord = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)

    db_x_vel = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_y_vel = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_z_vel = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)

    db_distance = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_bearing = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_inclination = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_approach_bearing = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)

    db_space_obj = models.ForeignKey(
        "SpaceDB",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="spaceobject",
        help_text="the object that this space entry represents",
        default=None)
    
    class Meta:
        """Define Django meta options"""
        verbose_name = "SpaceContact"
        verbose_name_plural = "SpaceContacts"

"""
Notes:

    from world.space.models import SpaceDB

    droplet = ItemDB.objects.get(db_key="red_droplet")
    print(f'{droplet.obj_id} - {droplet.name} - {droplet.caption}') 

    CREATE RECORD
    @py from world.space.models import SpaceDB; mars=SpaceDB(db_key="mars"); mars.save()

    DELETE RECORD
    @py from world.space.models import SpaceDB; match=SpaceDB.objects.filter(db_key__exact="mars"); match.delete()

"""    
class SpaceDB(SharedMemoryModel):
    "A model used to store objects that will only exist inside the 'SPACE' room and be updated via scripts"
    db_key = models.CharField(max_length=80, db_index=True)
    db_category = models.CharField(max_length=80, null=True, blank=True)
    db_name = models.CharField(max_length=80, null=True, blank=True)
    db_desc = models.TextField(null=True, blank=True)
    db_item = models.ForeignKey(
        "objects.ObjectDB",
        null=True,
        verbose_name="object",
        on_delete=models.SET_NULL,
        help_text="the object that this space entry represents in the evennia db",)
    db_transmat = models.TextField(null=True, blank=True)

    db_dock_room = models.CharField(max_length=80, null=True, blank=True)
    
    ########################################################
    # Space-specific attributes
    ########################################################

    # This is how we will relate space objects like ships to objects in the SPACE room
    db_mass = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_radius = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)

    db_x_coord = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_y_coord = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_z_coord = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)

    db_x_vel = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_y_vel = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_z_vel = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)

    db_orbital_radius = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_orbital_period = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)
    db_inclination = models.DecimalField(max_digits=200, decimal_places=100, default=0.0)

    db_orbiting_body = models.ForeignKey(
        "SpaceDB",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="space object",
        help_text="the object that this space entry orbits",
        default=None)
    
    db_in_space = models.BooleanField(default=False)
    db_ascii_art = models.CharField(max_length=80, null=True, blank=True)
    
    db_date_created = models.DateTimeField('date created', editable=False,
                                            auto_now_add=True, db_index=True)
    
    def get_space_obj_from_obj(self, obj):
        # Function to return the space object connected to a given evennia object
        ref_obj = None
        if isinstance(obj, SpaceDB):
            ref_obj = obj
        else:
            ref_obj = SpaceDB.objects.filter(db_key__exact=f"#{obj.dbid}")
            if len(ref_obj) <= 1:
                ref_obj = ref_obj[0]
        return ref_obj

    def distance_between_space_objects(self, obj1):
        """
        Function to determine the spacial distance between this object and any given <obj>
        passed to it. Distance is in three-dimensions and is returned in kilometers (km).
        """
        ref_obj1 = self
        ref_obj2 = self.get_space_obj_from_obj(obj1)

        if ref_obj1 and ref_obj2:
            if ref_obj1 == ref_obj2:
                return None 
            else:
                import math
                # Distance in kilometers (km)
                try:
                    distance = math.sqrt((float(ref_obj2.db_x_coord) - float(ref_obj1.db_x_coord))**2 + (float(ref_obj2.db_y_coord) - float(ref_obj1.db_y_coord))**2 + (float(ref_obj2.db_z_coord) - float(ref_obj1.db_z_coord))**2)
                except:
                    distance = 0.0 # handle DIV 0 errors.
                if distance == 0.0:
                    distance = 0.000000000000000000001 # No two objects can be in the same place
                return distance
        else:
            return None
    
    class Meta:
        """Define Django meta options"""
        verbose_name = "SpaceObject"
        verbose_name_plural = "SpaceObjects"
        