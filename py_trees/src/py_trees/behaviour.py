#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/yujinrobot/gopher_crazy_hospital/license/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
.. module:: behaviour
   :platform: Unix
   :synopsis: The core behaviour template.

----

"""

##############################################################################
# Imports
##############################################################################

import uuid

from . import logging
from .common import Status

##############################################################################
# Behaviour BluePrint
##############################################################################


class Behaviour(object):
    """ A node in a behavior tree that uses coroutines in its tick function """

    def __init__(self, name="", *args, **kwargs):
        self.id = uuid.uuid4()  # used to uniquely identify this node (helps with removing children from a tree)
        self.name = name
        self.status = Status.INVALID
        self.iterator = self.tick()
        self.parent = None  # will get set if a behaviour is added to a composite
        self.children = []  # only set by composite behaviours
        self.logger = logging.get_logger("Behaviour")
        self.feedback_message = ""  # useful for debugging, or human readable updates, but not necessary to implement

    ############################################
    # User Defined Functions (virtual)
    ############################################

    def initialise(self):
        self.logger.debug("  %s [initialise()]" % self.name)

    def terminate(self, new_status):
        """
        User defined terminate (cleanup) function. For comparison tests, it is
        often useful to check if the current status is Status.RUNNING and
        the new status is different to trigger appropriate cleanup actions.

        :param Status new_status: compare with current status for decision logic.

        """
        self.logger.debug("  %s [terminate()]" % self.name)

    def update(self):
        """
        User customisable update function called on by the :py:meth:`tick() <py_trees.behaviours.Behaviour.tick>` method.

        :return: the behaviour's current :py:class:`Status <py_trees.common.Status>`
        """
        self.logger.debug("  %s [update()]" % self.name)
        return Status.INVALID

    ############################################
    # Workers
    ############################################

    def visit(self, visitor):
        """
        This is functionality permitting
        visitors to run over the running part of
        a behaviour tree.
        :param visitor: the visiting class, must have a run(Behaviour) method.
        """
        visitor.run(self)

    def tick(self):
        """
        The update mechanism for the behaviour. Customisation goes
        into the update() function.

        :return Status: resulting state after the tick is completed
        """
        self.logger.debug("  %s [tick()]" % self.name)
        if self.status != Status.RUNNING:
            self.initialise()
        # don't set self.status yet, terminate() may need to check what the current state is first
        new_status = self.update()
        if new_status not in list(Status):
            self.logger.error("A behaviour returned an invalid status, setting to INVALID [%s][%s]" % (new_status, self.name))
            new_status = Status.INVALID
        if new_status != Status.RUNNING:
            self.abort(new_status)
        self.status = new_status
        yield self

    def iterate(self):
        """
        Generator that provides iteration over this behaviour and all its children.
        """
        for child in self.children:
            for node in child.iterate():
                yield node
        yield self

    def abort(self, new_status=Status.INVALID):
        """
        :param Status new_status: set the status to this once done.

        This calls the user defined terminate() method and also resets the
        generator. The specified status can be used to compare with the
        current status field for decision making within the terminate function
        itself.

        Do not think of this as an abort only for shutdown and invalid state setting
        (though this is the default argument). Abort is also the proper call when
        the behaviour returns success at which point the behaviour must abort
        any processing and do any required cleanup so it doesn't sit around
        consuming resources awaiting the next time it must be called (initialisation
        should not be done here - it could be a long time before the behaviour gets
        called again, and you shouldn't consume those resources in the meantime).
        """
        self.logger.debug("  %s [abort()]" % self.name)
        self.terminate(new_status)
        self.status = new_status
        self.iterator = self.tick()

    ############################################
    # Status
    ############################################

    def get_status(self):
        return self.status

    def set_status(self, s):
        self.status = s

    def is_running(self):
        return self.status == Status.RUNNING

    def is_terminated(self):
        return (self.status == Status.SUCCESS) or (self.status == Status.FAILURE)