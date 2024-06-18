
from django.conf import settings

from evennia.commands.default.system import CmdAbout
from evennia.utils import utils

from space.utils.about import get_version_space
from combat.utils.about import get_version_combat

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)


class CmdAbout(CmdAbout):
    """
    show Evennia info

    Usage:
      about

    Display info about the game engine.
    """

    key = "@about"
    aliases = "@version"
    locks = "cmd:all()"
    help_category = "System"

    def func(self):
        """Display information about server or target"""

        super(CmdAbout, self).func()

        self.caller.msg(get_version_space())
        self.caller.msg(get_version_combat())
