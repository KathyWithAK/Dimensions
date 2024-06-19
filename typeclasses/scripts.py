"""
Scripts

Scripts are powerful jacks-of-all-trades. They have no in-game
existence and can be used to represent persistent game systems in some
circumstances. Scripts can also have a time component that allows them
to "fire" regularly or a limited number of times.

There is generally no "tree" of Scripts inheriting from each other.
Rather, each script tends to inherit from the base Script class and
just overloads its hooks to have it perform its function.

"""
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta, date
from pytz import timezone # importing timezone from pytz module
from django.conf import settings
import random, re

import evennia
from evennia.scripts.scripts import DefaultScript
from evennia import gametime

import world.utils.weather as weather_utils

class Script(DefaultScript):
    """
    A script type is customized by redefining some or all of its hook
    methods and variables.

    * available properties

     key (string) - name of object
     name (string)- same as key
     aliases (list of strings) - aliases to the object. Will be saved
              to database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     desc (string)      - optional description of script, shown in listings
     obj (Object)       - optional object that this script is connected to
                          and acts on (set automatically by obj.scripts.add())
     interval (int)     - how often script should run, in seconds. <0 turns
                          off ticker
     start_delay (bool) - if the script should start repeating right away or
                          wait self.interval seconds
     repeats (int)      - how many times the script should repeat before
                          stopping. 0 means infinite repeats
     persistent (bool)  - if script should survive a server shutdown or not
     is_active (bool)   - if script is currently running

    * Handlers

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this
                        self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not
                        create a database entry when storing data

    * Helper methods

     start() - start script (this usually happens automatically at creation
               and obj.script.add() etc)
     stop()  - stop script, and delete it
     pause() - put the script on hold, until unpause() is called. If script
               is persistent, the pause state will survive a shutdown.
     unpause() - restart a previously paused script. The script will continue
                 from the paused timer (but at_start() will be called).
     time_until_next_repeat() - if a timed script (interval>0), returns time
                 until next tick

    * Hook methods (should also include self as the first argument):

     at_script_creation() - called only once, when an object of this
                            class is first created.
     is_valid() - is called to check if the script is valid to be running
                  at the current time. If is_valid() returns False, the running
                  script is stopped and removed from the game. You can use this
                  to check state changes (i.e. an script tracking some combat
                  stats at regular intervals is only valid to run while there is
                  actual combat going on).
      at_start() - Called every time the script is started, which for persistent
                  scripts is at least once every server start. Note that this is
                  unaffected by self.delay_start, which only delays the first
                  call to at_repeat().
      at_repeat() - Called every self.interval seconds. It will be called
                  immediately upon launch unless self.delay_start is True, which
                  will delay the first call of this method by self.interval
                  seconds. If self.interval==0, this method will never
                  be called.
      at_stop() - Called as the script object is stopped and is about to be
                  removed from the game, e.g. because is_valid() returned False.
      at_server_reload() - Called when server reloads. Can be used to
                  save temporary variables you want should survive a reload.
      at_server_shutdown() - called at a full server shutdown.

    """

    pass

class WeatherScript(Script):
    """
    A script that collects and stores weather-related data to feed into the different zones.
    All that is required is a zone name, and LAT/LONG geo corrds. The script will then use
    several public APIs to collect data on weather, sun, and moon data.
    """

    MESSAGE_FREQUENCY = 50 # random selection between 1 and #. 0 to stop

    def at_script_creation(self):
        """
        An array of dict holding zones and their collected weather data
        Use this format:
            
            [ { 'zone_name': '', 'latitude': '', 'longitude': '', last_update: ''} ]
        """
        self.key = "weather_script"
        self.desc = "Collects weeather data"
        self.db.weather_zones = [{'zone_name': 'default', 'latitude': settings.DEFAULT_LATITUDE, 'longitude': settings.DEFAULT_LONGITUDE, 'data': None, 'last_update': None}]
    
    def at_repeat(self):
        # Build up the weather data for each of the zones listed
        if self.db.weather_zones:
            for w in self.db.weather_zones:
                            
                # Attempt to collect general weather data
                try:
                    weather_data = weather_utils.get_weather_data(latitude=w['latitude'], 
                                                                  longitude=w['longitude'])

                    # Attempt to collect Sol data, for use on Earth only
                    sun_data = weather_utils.get_sun_data(latitude=w['latitude'],
                                                          longitude=w['longitude'], 
                                                          tzid=weather_data['timeZone'])

                    # Attempt to collect Moon data, for use on Earth only
                    moon_data = weather_utils.get_moon_data(latitude=w['latitude'],
                                                            longitude=w['longitude'])
                                        
                    w['weather_data'] = weather_data
                    w['sun_data'] = sun_data
                    w['moon_data'] = moon_data

                    current_datetime = None

                    if w['longitude'] and w['latitude']:
                        tf = TimezoneFinder()
                        tzone = tf.timezone_at(lng=w['longitude'], lat=w['latitude'])

                        current_datetime = datetime.now(timezone(tzone))
                        timestamp = current_datetime.timestamp()
                    else:
                        timestamp = gametime.gametime(absolute=True)
                        current_datetime = datetime.utcfromtimestamp(float(timestamp))

                    w['updated'] = current_datetime
                    
                except Exception as ex:
                    print(f"Error reading weather data: {ex}")

            self.room_weather_message()

    def str_to_date(self, datestr):
        match = re.search("(\d{1,2}):(\d{2}):(\d{2})\s([AMPamp]{2})", datestr)
        if match:
            time_str = f"{int(match.group(1)):02d}:{match.group(2)}:{match.group(3)} {match.group(4)}"          
            time_str = datetime.strptime(time_str, '%I:%M:%S %p').time()
            if isinstance(time_str, type(datetime.now().time())):
                return time_str
            else:
                return None
        return None
    
    def is_sunrise(self, room):
        room_time = room.get_room_time()
        if room.isEarth and room.isOutside:
            weather_data_block = room.get_weather_from_script()
            sunrise = self.str_to_date(weather_data_block['sun_data']['sunrise'])
            if sunrise:
                current_time = room_time.time()
                time_d = datetime.combine(date.min, current_time) - datetime.combine(date.min, sunrise)
                if timedelta(seconds=-1 * (self.interval + 1)) <= time_d <= timedelta(seconds=(self.interval + 1)):
                    return True     
        return False
    
    def is_sunset(self, room):
        room_time = room.get_room_time()
        if room.isEarth and room.isOutside:
            weather_data_block = room.get_weather_from_script()
            sunset = self.str_to_date(weather_data_block['sun_data']['sunset'])
            if sunset:
                current_time = room_time.time()
                time_d = datetime.combine(date.min, current_time) - datetime.combine(date.min, sunset)
                if timedelta(seconds=-1 * (self.interval + 1)) <= time_d <= timedelta(seconds=(self.interval + 1)):
                    return True    
        return False

    # def room_weather_message(self):
    #     """
    #     Returns a random weather message based on the given season, time of day, and current weather.
    #     """    
    #     rooms = evennia.search_tag(key=('outside'), category='location')
    #     for r in rooms:
    #         if self.is_sunrise():
    #             r.msg_contents(random.choice(self.weather_messages['sunrise']))
    #         elif self.is_sunset():
    #             r.msg_contents(random.choice(self.weather_messages['sunset']))
    #         elif random. randint(1, self.MESSAGE_FREQUENCY) == 1:
    #             season = r.get_season()
    #             time_of_day = r.get_time_of_day()
    #             curr_weather = r.get_curr_weather()
    #             if curr_weather:
    #                 curr_weather = curr_weather.replace(' ','').lower()

    #             messages = []
    #             if season in self.weather_messages.keys():
    #                 messages += self.weather_messages[season]
    #             if time_of_day in self.weather_messages.keys():
    #                 messages += self.weather_messages[time_of_day]
    #             if curr_weather in self.weather_messages.keys():
    #                 messages += self.weather_messages[curr_weather]
    #             if f"{season}.{time_of_day}" in self.weather_messages.keys():
    #                 messages += self.weather_messages[f"{season}.{time_of_day}"]
    #             if f"{season}.{curr_weather}" in self.weather_messages.keys():
    #                 messages += self.weather_messages[f"{season}.{curr_weather}"]
    #             if f"{time_of_day}.{curr_weather}" in self.weather_messages.keys():
    #                 messages += self.weather_messages[f"{time_of_day}.{curr_weather}"]
    #             if f"{season}.{time_of_day}.{curr_weather}" in self.weather_messages.keys():
    #                 messages += self.weather_messages[f"{season}.{time_of_day}.{curr_weather}"]

    #             print(season + '.' + time_of_day + '.' + curr_weather)
    #             msg = random.choice(messages)
    #             if len(msg) > 0:
    #                 r.msg_contents(random.choice(messages))
    
    def room_weather_message(self):
      """
      Returns a random weather message based on the given season, time of day, and current weather.
      """
      rooms = evennia.search_tag(key=('outside'), category='location')
      for r in rooms:
          if self.is_sunrise(r):
              r.msg_contents(random.choice(self.weather_messages['sunrise']))
              return
          elif self.is_sunset(r):
              r.msg_contents(random.choice(self.weather_messages['sunset']))
              return
          elif random. randint(0, self.MESSAGE_FREQUENCY) == 1:
              season = r.get_season()
              time_of_day = r.get_time_of_day()
              curr_weather = r.get_curr_weather().replace(' ', '').lower()

              messages = self.get_weather_messages(season, time_of_day, curr_weather)
              if messages:
                  message = random.choice(messages)
                  r.msg_contents(message)

    def get_weather_messages(self, season, time_of_day, curr_weather):
        messages = []
        for key in [season, time_of_day, curr_weather, f"{season}.{time_of_day}", f"{season}.{curr_weather}", f"{time_of_day}.{curr_weather}", f"{season}.{time_of_day}.{curr_weather}"]:
            if key in self.weather_messages:
                messages.extend(self.weather_messages[key])
        return messages

    weather_messages = {
        'sunrise': [
            "|rWelcome the dawn, where new beginnings unfold beneath the gentle embrace of the rising sun.|n",
        ],
        'sunset': [
            "|rEmbrace the tranquility as the sun sets, knowing tomorrow holds new promises and possibilities.|n",
        ],
        'summer.morning': [
            "The warmth of the sun shines down, promising a bright day ahead.", 
            "The warmth of the early sun kisses the dewy grass.",
            "The warmth of the early sun kisses the dewy grass, as birdsong fills the fresh morning air.",
        ],
        'summer.afternoon': [
            "Various clouds float across the sky above, casting fleeting shadows as they drift in front of the sun.",
            "The scorching sun bathes the landscape in a golden hue.",
            "The scorching sun bathes the landscape in a golden hue, while a gentle breeze rustles through the leaves of sun-dappled trees.",
        ],
        'summer.evening': [
            "A few more clouds begin to cover the moon in the darkening sky, casting eerie images over the ground.",
            "A symphony of crickets accompanies the vivid sunset, painting the sky with hues of orange and pink over the tranquil horizon.",
        ],
        'summer.night': [
            "A vast array of stars sparkle above you, illuminating the serene night.",
            "A symphony of crickets accompanies the twinkling stars above.",
            "A vast array of stars sparkle above you, illuminating the serene night, while distant laughter drifts from a bonfire under the moonlit sky.",
        ],

        'summer.morning.mostlycloudy': [
            "The warmth of the early sun gently filters through gaps in the dense cloud cover, creating a soft, diffused light over the dewy grass.",
        ],
        'summer.afternoon.mostlycloudy': [
            "Despite the clouds, the afternoon heat still manages to break through intermittently, casting shifting patterns of light and shadow across the landscape.",
        ],
        'summer.evening.mostlycloudy': [
            "As the sun sets behind the thickening clouds, a soft glow emerges on the horizon, painting the sky with hues of muted gold and lavender.",
        ],
        'summer.night.mostlycloudy': [
            "Despite the cloud cover, the occasional break reveals a glimmering tapestry of stars above, lending a mystical aura to the serene night.",
        ],

    }

"""
The sky clears up, and the warmth of the sun shines down.
Various clouds float across the sky above. The light dims occasionally as they drift in front of the sun.
A few more clouds begin to cover the moon in the darkening sky, casting eerie night time images over the ground.
The sky clears up, and a vast array of stars sparkle above you.
The warmth of the early sun kisses the dewy grass.
The warmth of the sun shines down, promising a bright day ahead.
Various clouds float across the sky above, casting fleeting shadows as they drift in front of the sun.
The scorching sun bathes the landscape in a golden hue.
A few more clouds begin to cover the moon in the darkening sky, casting eerie images over the lands.
A vast array of stars sparkle above you, illuminating the serene night.
A symphony of crickets accompanies the twinkling stars above.

Chatgpt, using the above as a format, generate one unique sentence for each of the following:

summer.morning.mostlyclear
summer.afternoon.mostlyclear
summer.evening.mostlyclear
summer.night.mostlyclear

"""
"""
SUNSET
As the last rays of the setting sun vanish beneath the horizon, shadows appear throughout the land as its long lasting peace turns to the evil, cursed realm of darkness.
"""

"""
Possible weather conditions from the API

chancerainshowers
chanceshowersandthunderstorms
clear
isolatedrainshowers
isolatedshowersandthunderstorms
mostlyclear
mostlycloudy
mostlysunny
partlycloudy
partlysunny
rainshowers
rainshowerslikely
scatteredrainshowers
scatteredshowersandthunderstorms
showersandthunderstormslikely
showersandthunderstorms
slightchancerainshowers
slightchanceshowersandthunderstorms
sunny
slightchancerainandsnowshowers
slightchancesnowshowers
chancelightsnow
scatteredsnowshowers
isolatedsnowshowers
chancesnowshowers

"""