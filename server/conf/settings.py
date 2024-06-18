r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Dimensions"

# ID of the "Space" room
SPACE_ROOM = 4

# Enable built in functions (in-game)
FUNCPARSER_PARSE_OUTGOING_MESSAGES_ENABLED = True

# Installed apps
# Global and Evennia-specific apps. This ties everything together so we can
# refer to app models and perform DB syncs.
INSTALLED_APPS += ['world.space',]

# A list of Django apps (see INSTALLED_APPS) that will be listed first (if present)
# in the Django web Admin page.
DJANGO_ADMIN_APP_ORDER += [
    "space",
]

DEFAULT_CHANNELS = [ 
	{
        "key": "SpaceInfo",
        "aliases": ("sinfo",),
        "desc": "Space system-related communication",
        "locks": "control:perm(Admin);listen:all();send:perm(Admin)",
    },
]

GLOBAL_SCRIPTS = {
    'weather_script': {
        'typeclass': 'typeclasses.scripts.WeatherScript',
        'interval': 60,
        'repeats': 0,
        'desc': 'Weather Script',
    },
    "storagescript": {}
}

DEFAULT_LATITUDE = 42.3555363911012
DEFAULT_LONGITUDE = -71.06054679461245

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
