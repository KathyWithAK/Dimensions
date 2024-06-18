"""
Room

Rooms are simple containers that has no location of their own.

"""

from collections import defaultdict

from evennia.objects.objects import DefaultRoom
from evennia.utils.utils import (
    #class_from_module,
    #is_iter,
    iter_to_str,
    #lazy_property,
    #make_iter,
    #to_str,
    #variable_from_module,
)
from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """

    appearance_template = """
{header}
|c{name}|n{caption}|n
{desc}
{objects}{exits}
{footer}
    """    

    def return_appearance(self, looker, **kwargs):
        """
        Main callback used by 'look' for the object to describe itself.
        This formats a description. By default, this looks for the `appearance_template`
        string set on this class and populates it with formatting keys
            'name', 'desc', 'exits', 'characters', 'things' as well as
            (currently empty) 'header'/'footer'. Each of these values are
            retrieved by a matching method `.get_display_*`, such as `get_display_name`,
            `get_display_footer` etc.

        Args:
            looker (Object): Object doing the looking. Passed into all helper methods.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call. This is passed into all helper methods.

        Returns:
            str: The description of this entity. By default this includes
                the entity's name, description and any contents inside it.

        Notes:
            To simply change the layout of how the object displays itself (like
            adding some line decorations or change colors of different sections),
            you can simply edit `.appearance_template`. You only need to override
            this method (and/or its helpers) if you want to change what is passed
            into the template or want the most control over output.

        """

        if not looker:
            return ""
        
        # populate the appearance_template string.
        return self.format_appearance(
            self.appearance_template.format(
                name=self.get_display_name(looker, **kwargs),
                caption=self.get_display_caption(looker, **kwargs),
                desc=self.get_display_desc(looker, **kwargs),
                header=self.get_display_header(looker, **kwargs),
                footer=self.get_display_footer(looker, **kwargs),                
                #characters=self.get_display_characters(looker, **kwargs),
                #things=self.get_display_things(looker, **kwargs),
                objects=self.get_display_objects(looker, **kwargs),
                exits=self.get_display_exits(looker, **kwargs),                
            ),
            looker,
            **kwargs,
        )        
    
    def get_display_name(self, looker=None, **kwargs):
        """
        Displays the name of the object in a viewer-aware manner.

        Args:
            looker (TypedObject): The object or account that is looking
                at/getting inforamtion for this object. If not given, `.name` will be
                returned, which can in turn be used to display colored data.

        Returns:
            str: A name to display for this object. This can contain color codes and may
                be customized based on `looker`. By default this contains the `.key` of the object,
                followed by the DBREF if this user is privileged to control said object.

        Notes:
            This function could be extended to change how object names appear to users in character,
            but be wary. This function does not change an object's keys or aliases when searching,
            and is expected to produce something useful for builders.

        """
        if looker and self.locks.check_lockstring(looker, "perm(Builder)"):
            return "{}(#{})".format(self.name, self.id)
        return self.name

    def get_display_caption(self, looker=None, **kwargs):
        """
        Get the 'caption' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The caption display data.

        """
        if looker and self.db.caption:
            return " |b~-~-~[|y {} |b]~-~-~|n".format(self.db.caption)
        return ""
    
    def get_display_header(self, looker=None, **kwargs):
        return ""
    
    def get_display_footer(self, looker=None, **kwargs):
        return ""
    
    def get_display_characters(self, looker=None, **kwargs):
        """
        Get the 'characters' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The character display data.

        """
        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        def _get_conditions(obj, thing_name):
            thing_conditions = ""
            if obj.tags.get(category='condition'):
                thing_conditions = iter_to_str(obj.tags.get(category='condition'))
                if len(thing_conditions.strip()) > 0:
                    thing_name = "{}({})".format(thing_name, thing_conditions)
            return thing_name
        
        characters = _filter_visible(self.contents_get(content_type="character"))
        character_names = ""
        for char in characters:

            character_caption = ""
            if char.db.caption:
                character_caption = " {}".format(char.db.caption)
            character_name = "{}|n{}".format(char.get_display_name(looker, **kwargs),
                                           char.get_extra_display_name_info(looker, **kwargs))
            character_name = " {}|n{} ".format(character_name, character_caption)
            
            # display conditions on an object, if any            
            character_name = _get_conditions(char, character_name)

            character_names = "{}{}\n".format(character_names, character_name)
        
        return f"{character_names}" if character_names else ""
    
    def get_display_things_grouped(self, looker=None, **kwargs):
        """
        Get the 'things' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The things display data.

        """
        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        def _get_conditions(obj, thing_name):
            thing_conditions = ""
            if obj.tags.get(category='condition'):
                thing_conditions = iter_to_str(obj.tags.get(category='condition'))
                if len(thing_conditions.strip()) > 0:
                    thing_name = "{}({})".format(thing_name, thing_conditions)
            return thing_name
        
        # sort and handle same-named things
        things = _filter_visible(self.contents_get(content_type="object"))

        grouped_things = defaultdict(list)
        for thing in things:
            grouped_things[thing.get_display_name(looker, **kwargs)].append(thing)

        thing_names = ""
        for thingname, thinglist in sorted(grouped_things.items()):

            thing_caption = ""
            if thinglist[0].db.caption:
                thing_caption = " {}".format(thinglist[0].db.caption)
            thing_name = " {}|n{} ".format(thingname, thing_caption)   

            # display conditions on an object, if any            
            thing_name = _get_conditions(thinglist[0], thing_name)

            thing_names = "{}{}\n".format(thing_names, thing_name)
        
        return f"{thing_names}" if thing_names else ""

    def get_display_things(self, looker, **kwargs):
        """
        Get the 'things' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The things display data.

        """
        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        def _get_conditions(obj, thing_name):
            thing_conditions = ""
            if obj.tags.get(category='condition'):
                thing_conditions = iter_to_str(obj.tags.get(category='condition'))
                if len(thing_conditions.strip()) > 0:
                    thing_name = "{}({})".format(thing_name, thing_conditions)
            return thing_name
        
        # sort and handle same-named things
        things = _filter_visible(self.contents_get(content_type="object"))
        thing_names = ""

        for thing in things:

            thing_caption = ""
            if thing.db.caption:
                thing_caption = " {}".format(thing.db.caption)
            thing_name = "{}|n{}".format(thing.get_display_name(looker, **kwargs),
                                           thing.get_extra_display_name_info(looker, **kwargs))
            thing_name = " {}|n{} ".format(thing_name, thing_caption)
            
            # display conditions on an object, if any            
            thing_name = _get_conditions(thing, thing_name)

            thing_names = "{}{}\n".format(thing_names, thing_name)
        
        return f"{thing_names}" if thing_names else ""

    def get_display_objects(self, looker=None, **kwargs):
        if looker:
            characters=self.get_display_characters(looker, **kwargs)
            things=self.get_display_things(looker, **kwargs)
            objects=f"{characters}{things}"
            return f"|wContents:|n\n{objects}" if objects else ""
    
    def get_display_exits(self, looker=None, **kwargs):
        """
        Get the 'exits' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The exits display data.

        """
        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        exits = _filter_visible(self.contents_get(content_type="exit"))
        exit_names = ""

        for exi in exits:
            
            exit_name = " {}|n".format(
                exi.get_display_name(looker, **kwargs))
            exit_names = "{}{}".format(exit_names, exit_name)

        #exit_names = iter_to_str(exi.get_display_name(looker, **kwargs) for exi in exits)
        return f"|wObvious Exits:\n|n{exit_names}" if exit_names else ""    

    