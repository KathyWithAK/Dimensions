from collections import defaultdict
from datetime import datetime
from pytz import timezone # importing timezone from pytz module
import random
from timezonefinder import TimezoneFinder

from evennia.contrib.grid.extended_room import ExtendedRoom
from evennia.objects.objects import DefaultRoom
from typeclasses.rooms import Room
from evennia import EvForm
from evennia import GLOBAL_SCRIPTS
from evennia.typeclasses.attributes import AttributeProperty
from evennia.utils.utils import (
    #class_from_module,
    #is_iter,
    iter_to_str,    
    #lazy_property,
    #make_iter,
    #to_str,
    #variable_from_module,
    list_to_string,
    repeat
)
from evennia import (
    CmdSet,
    Command,
    EvForm,
    #FuncParser,
    #InterruptCommand,
    #default_cmds,
    gametime,
    #utils,
)

import world.utils.weather as weather_utils

class MyExtendedRoom(Room, ExtendedRoom):
    """
    An Extended Room

    Room states:
        A room state is set as a Tag with category "roomstate" and tagkey "on_fire" or "flooded"
        etc).

    Alternative descriptions:
    - Add an Attribute `desc_<roomstate>` to the room, where <roomstate> is the name of the
        roomstate to use this for, like `desc_on_fire` or `desc_flooded`. If not given, seasonal
        descriptions given in desc_spring/summer/autumn/winter will be used, and last the
        regular `desc` Attribute.

    Alternative text sections
    - Used to add alternative text sections to the room description. These are embedded in the
        description by adding `$state(roomstate, txt)`. They will show only if the room is in the
        given roomstate. These are managed via the add/remove/get_alt_text methods.

    Details:
    - This is set as an Attribute `details` (a dict) on the room, with the detail name as key.
        When looking at this room, the detail name can be used as a target to look at without having
        to add an actual database object for it. The `detail` command is used to add/remove details.

    Room messages
    - Set `room_message_rate > 0` and add a list of `room_messages`. These will be randomly
        echoed to the room at the given rate.

    Weather
    - Tag a room with a zone matching one listed on the WeatherScript, or leave for default weather
        @tag room=<zone>:RoomZone

        WeatherScript will load new weather daya every few minutes, based on provided coords. To add
        a new zone to the WeatherScript, use the following:

        @py from evennia import GLOBAL_SCRIPTS; w=GLOBAL_SCRIPTS.weather_script; w.db.weather_zones = [{'zone_name': '<zone>', 'latitude': ##.####, 'longitude': ##.####}]                
    """

    # Minneapolis, MN - 44.984268, -93.267922
    # Denver, CO - 39.740632, -105.013338
    # Houston, TX - 29.809683, -95.406470
    # Orlando, FL - 28.537281, -81.371945
    # Boston, MA - 42.3555363911012, -71.06054679461245
    # Blackstone, ma - 42.015698098181836, -71.55024468781203

    appearance_template = """
{header}
|c{name}|n{caption}|n
{desc}
{objects}{exits}
{footer}
    """    

    def at_object_creation(self):
        super(MyExtendedRoom, self).at_object_creation()

        self.db.desc = ""

        # Add commands to the room
        self.cmdset.add_default(MyExtendedRoomCmdSet)

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
    
    def get_display_caption(self, looker, **kwargs):
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
            
    def get_display_exits(self, looker, **kwargs):
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
    
    def get_display_characters(self, looker, **kwargs):
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

    def get_display_things_grouped(self, looker, **kwargs):
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

    def get_display_objects(self, looker, **kwargs):
        if looker:
            characters=self.get_display_characters(looker, **kwargs)
            things=self.get_display_things(looker, **kwargs)
            objects=f"{characters}{things}"
            return f"|wContents:|n\n{objects}" if objects else ""

    def get_weather_from_script(self):
        if self.tags.get(category="roomzone"):
            room_zone = self.tags.get(category="roomzone")
        else:
            room_zone = 'default'        

        weather_data_array = GLOBAL_SCRIPTS.weather_script.db.weather_zones
        try:
            return next(item for item in weather_data_array if item['zone_name'].upper() == room_zone.upper())
        except Exception as ex:
            # Default if zone isn't found
            try:
                return next(item for item in weather_data_array if item['zone_name'].upper() == 'DEFAULT'.upper())
            except Exception as ex:
                return None
            
    def get_weather_data(self):
        weather_data = None
        weather_last_updated = None

        weather_data_block = self.get_weather_from_script()
        if not weather_data_block:
            return None, None
        
        weather_last_updated = weather_data_block['updated']
        if 'weather_data' in weather_data_block.keys():
            weather_data = weather_data_block['weather_data']

        return weather_data, weather_last_updated             

    def get_season(self):
        """
        Get the current season.

        Overridden to account for lat/long timezone.

        Returns:
            str: The season, such as 'spring', 'summer', 'autumn' or 'winter'.

        """
        weather_data, weather_last_updated = self.get_weather_data()
        if weather_last_updated:
            timestamp = weather_last_updated.timestamp()
        else:
            timestamp = gametime.gametime(absolute=True)

        datestamp = datetime.fromtimestamp(timestamp)
        timeslot = float(datestamp.month) / self.months_per_year

        for season_of_year, (start, end) in self.seasons_per_year.items():
            if start < end and start <= timeslot < end:
                return season_of_year
        return season_of_year  # final step is back to beginning

    def get_time_of_day(self):
        """
        Get the current time of day.

        Overridden to account for lat/long timezone.

        Returns:
            str: The time of day, such as 'morning', 'afternoon', 'evening' or 'night'.

        """
        weather_data, weather_last_updated = self.get_weather_data()
        if weather_last_updated:
            timestamp = weather_last_updated.timestamp()
        else:
            timestamp = gametime.gametime(absolute=True)

        datestamp = datetime.fromtimestamp(timestamp)
        timeslot = float(datestamp.hour) / self.hours_per_day

        for time_of_day, (start, end) in self.times_of_day.items():
            if start < end and start <= timeslot < end:
                return time_of_day
        return time_of_day  # final back to the beginning

    def get_room_time(self):
        """
        Get the current time of room.

        Returns:
            datetime respresenting current room time, adjusted by tz

        """
        weather_data, weather_last_updated = self.get_weather_data()
        if weather_last_updated:
            timestamp = weather_last_updated.timestamp()
        else:
            timestamp = gametime.gametime(absolute=True)

        datestamp = datetime.fromtimestamp(timestamp)

        return datestamp

    def get_curr_weather(self):
        """
        Get the current weather

        Returns:
            str: weather
        """
        weather_data, weather_last_updated = self.get_weather_data()
        if weather_last_updated:
            weather = weather_data['weatherPeriods'][0]['shortForecast']
        else:
            weather = None

        return weather  # final back to the beginning        

    def isEarth(self):
        return self.tags.get("Earth", category="location")

    def isOutside(self):
        return self.tags.get("outside", category="location")

class MyExtendedRoomOutside(MyExtendedRoom):
    def at_object_creation(self):
        super(MyExtendedRoom, self).at_object_creation()

        self.tags.add("outside", category="location")

        # Add commands to the room
        self.cmdset.add_default(MyExtendedRoomCmdSet)        

class MyExtendedRoomCmdSet(CmdSet):
    key = "MyExtendedRoomCmdSet"
    priority = 1

    def at_cmdset_creation(self):
        self.add(MyExtendedRoomWeather)

class MyExtendedRoomWeather(Command):
    """
    weather

    Display the current weather condition in the area. Will display
    both indoor and outdoor weather displays, based on how the room is tagged.

    To tag a room as "outside" use:
        self.location.tags.add("outside", category="location")
        self.location.tags.remove("outside", category="location")

    To tag a room as "Earth" use:
        self.location.tags.add("Earth", category="location")
        self.location.tags.remove("Earth", category="location")

    Also set room.db.latitude and room.db.longitude to customize weather origin

    """
    key = "weather"
    aliases = ["we"]
    help_category = "General"

    def func(self):

        weather_data_block = self.obj.get_weather_from_script()
        weather_data, weather_last_updated = self.obj.get_weather_data()
            
        current_datetime  = datetime.now()

        if weather_data:
            current_datetime = datetime.now(timezone(weather_data['timeZone']))
            date_format = "%A, %B %d, %Y - %I:%M:%S %p"

            timezone_location = ""
            if self.caller.permissions.check("Developer"):
                timezone_location = f"{weather_data['city']}, {weather_data['state']}"

            # Build data for the forms
            weather_period = weather_data['weatherPeriods'][0]
            conditions = weather_period['shortForecast']
            wind_speed = f"{weather_period['windSpeed']}, {weather_period['windDirection']}"
                
            air_temp_c, air_temp_f = weather_utils.get_celcius_fahrenheit(
                weather_period['temperature'], weather_period['temperatureUnit'])
            dew_temp_c, dew_temp_f = weather_utils.get_celcius_fahrenheit(
                weather_period['dewpoint']['value'], weather_period['dewpoint']['unit'])

            change_of_rain = weather_period['probabilityOfPrecipitation']['value'] or "0"
            relative_humidity = weather_period['relativeHumidity']['value'] or "-"
            humidity = weather_data['humidity'] or "-"
            visibility = weather_data['visibility'] or "-"
            visibility_scale = weather_data['visibility_scale'] or ""
            pressure = weather_data['pressure'] or "-"

            predictions = []
            for wp in weather_data['weatherPeriods']:
                weather_period = {}
                weather_period['c'], weather_period['f'] = weather_utils.get_celcius_fahrenheit(
                    wp['temperature'], wp['temperatureUnit'])
                weather_period['name'] = wp['name']
                weather_period['desc'] = wp['shortForecast']
                predictions.append(weather_period)

            updated_date = weather_last_updated
            if updated_date:
                updated_date = updated_date.strftime(date_format)

            if self.caller.location.isEarth() and self.caller.location.isOutside():
                # Display Earth weather, with moon and sun
                #sun_data = weather_utils.get_sun_data(latitude=self.obj.db.latitude, 
                #                            longitude=self.obj.db.longitude, tzid=weather_data['timeZone'])
                sun_data = weather_data_block['sun_data']
                #moon_data = weather_utils.get_moon_data(latitude=self.obj.db.latitude, 
                #                            longitude=self.obj.db.longitude)
                moon_data = weather_data_block['moon_data']

                form = EvForm("world.forms.form_weather_earth_outside")
                form.map(cells=
                {
                    1:  f"{current_datetime.strftime(date_format)}",
                    2:  f"{timezone_location}",
                    3:  f"{conditions}",
                    4:  f"{wind_speed}",
                    5:  f"{air_temp_f:.1f}^F",
                    6:  f"{air_temp_c:.1f}^C",
                    7:  f"{dew_temp_f:.1f}^F",
                    8:  f"{dew_temp_c:.1f}^C",
                    9:  f"{change_of_rain} %",
                    10: f"{relative_humidity} %", 
                    11: f"{predictions[1]['name']}",
                    12: f"{predictions[1]['desc']}",
                    13: f"{predictions[1]['f']:.1f}^F",
                    14: f"{predictions[1]['c']:.1f}^C",
                    15: f"{predictions[2]['name']}",
                    16: f"{predictions[2]['desc']}",
                    17: f"{predictions[2]['f']:.1f}^F",
                    18: f"{predictions[2]['c']:.1f}^C",
                    19: f"{sun_data['sunrise']}",
                    20: f"{sun_data['solar_noon']}",
                    21: f"{sun_data['sunset']}",
                    22: f"{sun_data['day_length']}",
                    23: f"{moon_data['moon']}",
                    24: f"{moon_data['age']:.1f} days",
                    25: f"{moon_data['angularDiameter']:.2f} deg",
                    26: f"{moon_data['phase']}",
                    27: f"{moon_data['distance']:.1f} million mi",
                    28: f"{moon_data['illumination'] * 100} %",
                    29: f"{updated_date}",
                    30: f"{predictions[3]['name']}",
                    31: f"{predictions[3]['desc']}",
                    32: f"{predictions[3]['f']:.1f}^F",
                    33: f"{predictions[3]['c']:.1f}^C",
                    34: f"{predictions[4]['name']}",
                    35: f"{predictions[4]['desc']}",
                    36: f"{predictions[4]['f']:.1f}^F",
                    37: f"{predictions[4]['c']:.1f}^C",
                    38: f"{predictions[5]['name']}",
                    39: f"{predictions[5]['desc']}",
                    40: f"{predictions[5]['f']:.1f}^F",
                    41: f"{predictions[5]['c']:.1f}^C",
                    42: f"{humidity} %",
                    43: f"{visibility} {visibility_scale}",
                    44: f"{pressure} 'Hg",
                    45: f"{sun_data['sunrise_degrees']}' {sun_data['sunrise_direction']}",
                    46: f"{sun_data['sunset_degrees']}' {sun_data['sunset_direction']}",
                    47: f"{sun_data['sun_distance']}",
                    48: f"{sun_data['sun_direction_degrees']}' {sun_data['sun_direction_direction']}",
                    49: f"{sun_data['sun_altitude']} deg",
                    50: f"{sun_data['next_solstice']}",
                } )
                    
                # Manually adjust cell justification
                #form.mapping['19'].reformat(align='r')
                #form.mapping['20'][4].align = 'r'
                #form.mapping['21'][4].align = 'r'
                #form.mapping['22'][4].align = 'r'

                self.caller.msg(form)

            elif self.caller.location.isOutside():
                # Display outside weather
                form = EvForm("world.forms.form_weather_outside")
                form.map(cells=
                {
                    1:  f"{current_datetime.strftime(date_format)}",
                    2:  f"{timezone_location}",
                    3:  f"{conditions}",
                    4:  f"{wind_speed}",
                    5:  f"{air_temp_f:.1f}^F",
                    6:  f"{air_temp_c:.1f}^C",
                    7:  f"{dew_temp_f:.1f}^F",
                    8:  f"{dew_temp_c:.1f}^C",
                    9:  f"{change_of_rain} %",
                    10: f"{relative_humidity} %", 
                    11: f"{predictions[1]['name']}",
                    12: f"{predictions[1]['desc']}",
                    13: f"{predictions[1]['f']:.1f}^F",
                    14: f"{predictions[1]['c']:.1f}^C",
                    15: f"{predictions[2]['name']}",
                    16: f"{predictions[2]['desc']}",
                    17: f"{predictions[2]['f']:.1f}^F",
                    18: f"{predictions[2]['c']:.1f}^C",
                    19: f"{updated_date}",
                    20: f"{predictions[3]['name']}",
                    21: f"{predictions[3]['desc']}",
                    22: f"{predictions[3]['f']:.1f}^F",
                    23: f"{predictions[3]['c']:.1f}^C",
                    24: f"{predictions[4]['name']}",
                    25: f"{predictions[4]['desc']}",
                    26: f"{predictions[4]['f']:.1f}^F",
                    27: f"{predictions[4]['c']:.1f}^C",
                    28: f"{predictions[5]['name']}",
                    29: f"{predictions[5]['desc']}",
                    30: f"{predictions[5]['f']:.1f}^F",
                    31: f"{predictions[5]['c']:.1f}^C",
                    32: f"{humidity} %",
                    33: f"{visibility} {visibility_scale}",
                    34: f"{pressure} 'Hg",
                } )
                self.caller.msg(form)

            else:
                # Display default weather
                form = EvForm("world.forms.form_weather_inside")
                form.map(cells=
                {
                    1:  f"{current_datetime.strftime(date_format)}",
                    2:  f"{timezone_location}",
                    3:  f"{updated_date}",
                } )
                self.caller.msg(form)

        else:
            self.caller.msg("Weather data failed to load. Try again.")