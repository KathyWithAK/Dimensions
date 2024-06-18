from django.conf import settings

"""

Lockfuncs

Lock functions are functions available when defining lock strings,
which in turn limits access to various game systems.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See the
Evennia documentation for more info on locks.

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled with *args, **kwargs. The lock function
should handle all eventual tracebacks by logging the error and
returning False.

Lock functions in this module extend (and will overload same-named)
lock functions from evennia.locks.lockfuncs.

"""

# def myfalse(accessing_obj, accessed_obj, *args, **kwargs):
#    """
#    called in lockstring with myfalse().
#    A simple logger that always returns false. Prints to stdout
#    for simplicity, should use utils.logger for real operation.
#    """
#    print "%s tried to access %s. Access denied." % (accessing_obj, accessed_obj)
#    return False

# Custom lock test for objects in space
# Uses:
#    @lock <door>=traverse:inspace(#<dbref to test>)
#
#    If debref is not included, lock will test the obj that triggered the lock
#
def inspace(accessing_obj, accessed_obj, *args, **kwargs):
    try:
        if len(args) > 0:
            ship_obj = accessed_obj.search(args[0], global_search=True, use_dbref=True)
            if (ship_obj.location.id == settings.SPACE_ROOM):
                return True
            else:
                return False
        else:
            if (accessing_obj.location.id == settings.SPACE_ROOM):
                return True
            else:
                return False
    except:
        raise Exception("SPACE_ROOM not set!")
