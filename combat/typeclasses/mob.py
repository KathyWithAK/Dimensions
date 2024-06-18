import random

from evennia import CmdSet, Command, TICKER_HANDLER
from evennia.utils import lazy_property

from typeclasses.objects import Object

from combat.typeclasses.traits import TraitHandler

"""

Wandering Mob 

1) create mob: @create <obj>:combat.typeclasses.mob.Mob
2) to enable the mob to wander:
    a) @set <obj>/wandering_pace=# -- How many seconds between wandering
    b) @set <obj>/irregular_msgs=[] -- messages to randomly emote when moving
3) start or stop wandering: mob/on <obj> or mob/off <obj>

"""
damage_thrust_table = ['0', '1D-6', '1D-6', '1D-5', '1D-5', '1D-4', '1D-4', '1D-3', '1D-3', 
    '1D-2', '1D-2', '1D-1', '1D-1', '1D', '1D', '1D+1', '1D+1', '1D+2', '1D+2', '2D-1', '2D-1']
damage_swing_table =  ['0', '1D-5', '1D-5', '1D-4', '1D-4', '1D-3', '1D-3', '1D-2', '1D-2', '1D-1', 
    '1D', '1D+1', '1D+2', '2D-1', '2D', '2D+1', '2D+2', '3D-1', '3D', '3D+1', '3d+2']

class CmdMobSwitch(Command):
    """
    Use to start/stop a mob from wandering.

    Usage:
        mob/off <mob>
        mob/on <mob>
    
    This will enable/disable the random wandering function of
    the object.
    """

    key="mob/on"
    aliases=["mob/off"]
    locks = "cmd:superuser()"

    def func(self):
        """
        Uses the mob's enable/disable methods
        to turn on/off the mob's wandering function.
        """
        if not self.args:
            self.caller.msg("Usage: mob <mob>")
            return
        mob = self.caller.search(self.args)
        if not mob:
            return
        if self.cmdstring == "mob/on":
            mob.start()
            self.caller.msg("Mob functions on {} have been enabled.".format(mob.name))
        else:
            mob.stop()
            self.caller.msg("Mob functions on {} have been disabled.".format(mob.name))

class MobCmdSet(CmdSet):
    """
    Holds the commands related to controlling the basic mob object
    """
    def at_cmdset_creation(self):
        self.add(CmdMobSwitch)

class Mob(Object):
    """
    This is a state-machine AU mobile (mob). It has several states which
    are controlled from setting various Attributes.

        wandering: if set, mob will wander randomly from room to room.
        wandering_pace: interval for triggering movement
        irregular_echoes: list of strings that the mob generates as
            irregular intervals.
    
    """
    @property
    def basic_lift(self):
        return (self.traits.ST.value * self.traits.ST.value) / (5 * 15)

    @property
    def basic_speed(self):
        return (self.traits.HT.value * self.traits.DX.value) / 4

    @property
    def dodge(self):
        return (self.basic_speed + 3)

    @lazy_property
    def traits(self):
        return TraitHandler(self)
    
    @lazy_property
    def skills(self):
        return TraitHandler(self, db_attribute='skills')
    
    def at_init(self):
        """
        When initialized croim cache (after a server reboot), set up
        the AI state.
        """
        self.ndb.is_wandering = self.db.wandering

    def at_object_creation(self):
        """
        Called when the object is first created. We use this
        to set up the base properties and flags.
        """
        super().at_object_creation()
        
        self.cmdset.add(MobCmdSet, persistent=True)
        # Main flags
        self.db.wandering = True
        self.db.wandering_pace = 30 # num seconds between ticks

        self.db.irregular_msgs = ["irregular msg 1", "irregular msg 2"]

        self.db.race = "Human"
        self.db.character_points = 0
        self.db.level = 1
        self.db.chapter = 1
        self.db.deaths = 0
        self.db.experience = 0

        # Primary Traits
        self.traits.add("ST", "Strength",        trait_type="static", base=10)
        self.traits.add("DX", "Dexterity",       trait_type="static", base=10)
        self.traits.add("IQ", "IQ",              trait_type="static", base=10)
        self.traits.add("HT", "Health",          trait_type="static", base=10)
        # Secondary Traits
        self.traits.add("HP", "Hit Points",      trait_type="gauge", base=0)
        self.traits.add("WP", "Willpower",       trait_type="gauge", base=0)
        self.traits.add("PER","Perception",      trait_type="static", base=0)
        self.traits.add("FP", "Fatigue",         trait_type="gauge", base=0)

        self.instantiate_secondary_traits()

    def instantiate_secondary_traits(self):
        # Use to set/reset all of the secondary traits based on the initial four base traits
        self.traits.HP.base = self.traits.HT.value # equals HT
        self.traits.WP.base = self.traits.IQ.value # equals IQ
        self.traits.PER.base = self.traits.IQ.value # equals IQ
        self.traits.FP.base = self.traits.HT.value # equals HT

    def get_damage_thrust(self):
        return list(damage_thrust_table)[int(self.traits.ST.value)]

    def get_damage_swing(self):
        return list(damage_swing_table)[int(self.traits.ST.value)]

    def _set_ticker(self, interval, hook_key, stop=False):
        """
        Set how often the given hook key should
        be "ticked".

        Args:
            interval (int or None): The number of seconds
                between ticks
            hook_key (str or None): The name of the method
                (on this mob) to call every interval
                seconds.
            stop (bool, optional): Just stop the
                last ticker without starting a new one.
                With this set, the interval and hook_key
                arguments are unused.

        In order to only have one ticker
        running at a time, we make sure to store the
        previous ticker subscription so that we can
        easily find and stop it before setting a
        new one. The tickerhandler is persistent so
        we need to remember this across reloads.
        """
        idstring = "mob_ticker_{}".format(self.dbid)
        last_interval = self.db.last_ticker_interval
        last_hook_key = self.db.last_hook_key
        if last_interval and last_hook_key:
            # kill the previous ticker before starting a new one
            TICKER_HANDLER.remove(
                interval=last_interval, callback=getattr(self, last_hook_key), idstring=idstring
            )
        self.db.last_ticker_interval = interval
        self.db.last_hook_key = hook_key
        if not stop:
            # start a new ticker
            TICKER_HANDLER.add(
                interval=interval, callback=getattr(self, hook_key), idstring=idstring
            )

    def start_idle(self):
        """
        This will kill the ticker for random wandering.        
        """
        self._set_ticker(None, None, stop=True)

    def start_wandering(self):
        """
        Start the wandering state by registering a ticket-handler
        """
        if not self.db.wandering:
            self.start_idle()
            return
        self._set_ticker(self.db.wandering_pace, "do_wander")
        self.ndb.is_wandering = True

    def do_wander(self, *args, **kwargs):
        """
        Called repeatedly during the wandering mode. In this mode, the
        mob will look at all of the viable exits and randomly choose one
        to go through. One should lock exits with 'transverse:has_account()' 
        lock in order to block the mob from moving outside its area while
        allowing account-controlled characters to move through the doors as normal.
        """
        randnum = random.random()
        if randnum < 0.5:
            if self.db.irregular_msgs:
                self.location.msg_contents(random.choice(self.db.irregular_msgs))
        
        # look for an exit
        exits = [exi for exi in self.location.exits if exi.access(self, "traverse")]
        if exits:
            #randomly pick an exit
            exit = random.choice(exits)
            # now move there
            self.move_to(exit.destination)
        else:
            # no exist were found. Go home instead
            self.move_to(self.home)

    def start(self):
        self.ndb.is_wandering = self.db.wandering
        if not self.location:
            self.move_to(self.home)
        if self.db.wandering:
            self.start_wandering()

    def stop(self):
        """
        This will kill the ticker for random wandering.       
        """
        self.location = self.home
        self.ndb.is_wandering = False
        self._set_ticker(None, None, stop=True)

    def get_attack_power(self):
        return self.items.total_item_attack_power()

    def get_defense_power(self):
        return self.items.total_item_defense_power()
    
    def get_condition(self):
        conditions = self.tags.get(category="condition")
        if conditions:
            if str(type(conditions)) == "<class 'str'>":
                condition_list = conditions
            else:
                condition_list = ", ".join(conditions)
        else:
            condition_list = "normal"
        return condition_list
    
    # Combat-Related Hooks
    def at_pre_attack(self):
        # Called before an attack and returns bool. If False, attack is cancelled
        pass

    def at_post_attach(self):
        # Always called after an attack has been successfully performed
        pass

    def at_pre_defend(self):
        # Called before a defend and returns bool. If False, defense is cancelled
        pass

    def at_post_defend(self):
        # Alway called after a defend has been successfully performed
        pass
    