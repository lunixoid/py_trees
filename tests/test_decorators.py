#!/usr/bin/env python
#
# License: BSD
#   https://raw.githubusercontent.com/stonier/py_trees/devel/LICENSE
#

##############################################################################
# Imports
##############################################################################

import py_trees
import py_trees.console as console

from nose.tools import assert_raises
import time

##############################################################################
# Logging Level
##############################################################################

py_trees.logging.level = py_trees.logging.Level.DEBUG
logger = py_trees.logging.Logger("Nosetest")

##############################################################################
# Classes
##############################################################################

class InvalidSetup(py_trees.behaviour.Behaviour):
    def setup(self, timeout):
        # A common mistake is to forget to return a boolean value
        # Composite behaviours will at least check to make sure that
        # their children do so and raise TypeError's if they fail
        # to do so.
        pass

class DummyDecorator(py_trees.decorators.Decorator):
    def __init__(self, child, name=py_trees.common.Name.AUTO_GENERATED):
        super(DummyDecorator, self).__init__(name=name, child=child)

##############################################################################
# Tests
##############################################################################

def test_set_name():
    console.banner("Set Name")
    child = py_trees.behaviours.Success(name="Woohoo")
    named_decorator = DummyDecorator(name="Foo", child=child)
    no_named_decorator = DummyDecorator(child=child)
    print("\n--------- Assertions ---------\n")
    print("named_decorator.name == Foo")
    assert(named_decorator.name == "Foo")
    print("no_named_decorator.name == DummyDecorator\\n[Woohoo]")
    assert(no_named_decorator.name == "DummyDecorator\n[Woohoo]")

def test_invalid_child():
    console.banner("Invalid Child")
    print("\n--------- Assertions ---------\n")
    print("TypeError is raised")
    assert_raises(TypeError, DummyDecorator.__init__, child=5)

def test_invalid_setup():
    console.banner("Invalid Setup")
    parent = py_trees.decorators.Decorator(
        name="Decorator",
        child=InvalidSetup(name="Invalid Setup")
    )
    print("\n--------- Assertions ---------\n")
    print("TypeError is raised")
    with assert_raises(TypeError) as context:
        parent.setup(timeout=15)
    print("TypeError has message with substring 'NoneType'")
    assert("NoneType" in str(context.exception))

# def test_failure_is_success_tree():
#     console.banner("Failure is Success Tree")
#     root = py_trees.composites.Selector(name="Root")
#     failure = py_trees.behaviours.Failure(name="Failure")
#     goon = MustGoOnRegardless(name="DontBeAfraidToBeTheGoon")
#     root.add_child(failure)
#     root.add_child(goon)
#     py_trees.display.print_ascii_tree(root)
#     visitor = py_trees.visitors.DebugVisitor()
#     py_trees.tests.tick_tree(root, visitor, 1, 1)
# 
#     print("\n--------- Assertions ---------\n")
#     print("root.status == py_trees.common.Status.SUCCESS")
#     assert(root.status == py_trees.common.Status.SUCCESS)
#     print("failure.status == py_trees.common.Status.FAILURE")
#     assert(failure.status == py_trees.common.Status.FAILURE)
#     print("goon.status == py_trees.common.Status.SUCCESS")
#     assert(goon.status == py_trees.common.Status.SUCCESS)
# 
# 
# def test_success_is_failure_tree():
#     console.banner("Success is Failure Tree")
#     root = py_trees.composites.Selector("Root")
#     failure = py_trees.behaviours.Failure(name="Failure")
#     going_down = py_trees.meta.success_is_failure(py_trees.behaviours.Success)(name="Going Down")
#     root.add_child(failure)
#     root.add_child(going_down)
#     py_trees.display.print_ascii_tree(root)
#     visitor = py_trees.visitors.DebugVisitor()
#     py_trees.tests.tick_tree(root, visitor, 1, 1)
# 
#     print("\n--------- Assertions ---------\n")
#     print("failure.status == py_trees.common.Status.FAILURE")
#     assert(failure.status == py_trees.common.Status.FAILURE)
#     print("going_down.status == py_trees.common.Status.FAILURE")
#     assert(going_down.status == py_trees.common.Status.FAILURE)
#     print("root.status == py_trees.common.Status.FAILURE")
#     assert(root.status == py_trees.common.Status.FAILURE)
# 
# 
# def test_inverter_tree():
#     console.banner("Inverter Tree")
#     root = py_trees.composites.Sequence(name="Root")
#     selector = py_trees.composites.Selector(name="Selector")
#     failure = py_trees.behaviours.Failure(name="Failure")
#     failure2 = py_trees.meta.inverter(py_trees.behaviours.Success)(name="Failure2")
#     success = py_trees.behaviours.Success(name="Success")
#     success2 = py_trees.meta.inverter(py_trees.behaviours.Failure)(name="Success2")
#     selector.add_child(failure)
#     selector.add_child(failure2)
#     selector.add_child(success)
#     root.add_child(selector)
#     root.add_child(success2)
#     py_trees.display.print_ascii_tree(root)
#     visitor = py_trees.visitors.DebugVisitor()
#     py_trees.tests.tick_tree(root, visitor, 1, 1)
# 
#     print("\n--------- Assertions ---------\n")
#     print("success.status == py_trees.common.Status.SUCCESS")
#     assert(success.status == py_trees.common.Status.SUCCESS)
#     print("success2.status == py_trees.common.Status.SUCCESS")
#     assert(success2.status == py_trees.common.Status.SUCCESS)
#     print("root.status == py_trees.common.Status.SUCCESS")
#     assert(root.status == py_trees.common.Status.SUCCESS)
#     print("failure.status == py_trees.common.Status.FAILURE")
#     assert(failure.status == py_trees.common.Status.FAILURE)
#     print("failure2.status == py_trees.common.Status.FAILURE")
#     assert(failure2.status == py_trees.common.Status.FAILURE)
# 
# 
# def test_running_is_failure_tree():
#     console.banner("Running is Failure Tree")
#     root = py_trees.composites.Selector(name="Root")
#     running = py_trees.meta.running_is_failure(py_trees.behaviours.Running)(name="Running")
#     failure = py_trees.meta.running_is_failure(py_trees.behaviours.Failure)(name="Failure")
#     success = py_trees.meta.running_is_failure(py_trees.behaviours.Success)(name="Success")
#     root.add_child(running)
#     root.add_child(failure)
#     root.add_child(success)
#     py_trees.display.print_ascii_tree(root)
#     visitor = py_trees.visitors.DebugVisitor()
#     py_trees.tests.tick_tree(root, visitor, 1, 1)
# 
#     print("\n--------- Assertions ---------\n")
#     print("running.status == py_trees.common.Status.FAILURE")
#     assert(running.status == py_trees.common.Status.FAILURE)
#     print("failure.status == py_trees.common.Status.FAILURE")
#     assert(failure.status == py_trees.common.Status.FAILURE)
#     print("success.status == py_trees.common.Status.SUCCESS")
#     assert(success.status == py_trees.common.Status.SUCCESS)
#     print("root.status == py_trees.common.Status.SUCCESS")
#     assert(root.status == py_trees.common.Status.SUCCESS)
# 
# 
# def test_inverter_sequence():
#     console.banner("Inverter Sequence Tree")
#     root = py_trees.meta.inverter(py_trees.composites.Sequence)(name="Root")
#     selector = py_trees.composites.Selector(name="Selector")
#     failure = py_trees.behaviours.Failure(name="Failure")
#     success = py_trees.behaviours.Success(name="Success")
#     selector.add_child(failure)
#     selector.add_child(success)
#     success2 = py_trees.behaviours.Success(name="Success2")
#     root.add_child(selector)
#     root.add_child(success2)
#     py_trees.display.print_ascii_tree(root)
#     visitor = py_trees.visitors.DebugVisitor()
#     py_trees.tests.tick_tree(root, visitor, 1, 1)
# 
#     print("\n--------- Assertions ---------\n")
#     print("root.status == py_trees.common.Status.FAILURE")
#     assert(root.status == py_trees.common.Status.FAILURE)
#     print("success.status == py_trees.common.Status.SUCCESS")
#     assert(success.status == py_trees.common.Status.SUCCESS)
#     print("success2.status == py_trees.common.Status.SUCCESS")
#     assert(success2.status == py_trees.common.Status.SUCCESS)
#     print("failure.status == py_trees.common.Status.FAILURE")
#     assert(failure.status == py_trees.common.Status.FAILURE)
#     print("selector.status == py_trees.common.Status.SUCCESS")
#     assert(selector.status == py_trees.common.Status.SUCCESS)


def test_timeout():
    console.banner("Timeout")
    running = py_trees.behaviours.Running(name="Running")
    timeout = py_trees.decorators.Timeout(child=running, duration=0.2)
    py_trees.display.print_ascii_tree(timeout)
    visitor = py_trees.visitors.DebugVisitor()
    
    # Test that it times out and re-initialises properly
    for i in range(0,2):
        py_trees.tests.tick_tree(timeout, 2*i+1, 2*i+1, visitor)

        print("\n--------- Assertions ---------\n")
        print("timeout.status == py_trees.common.Status.RUNNING")
        assert(timeout.status == py_trees.common.Status.RUNNING)
        print("running.status == py_trees.common.Status.RUNNING")
        assert(running.status == py_trees.common.Status.RUNNING)

        time.sleep(0.3)
        py_trees.tests.tick_tree(timeout, 2*i+2, 2*i+2, visitor)

        print("\n--------- Assertions ---------\n")
        print("timeout.status == py_trees.common.Status.FAILURE")
        assert(timeout.status == py_trees.common.Status.FAILURE)
        print("running.status == py_trees.common.Status.INVALID")
        assert(running.status == py_trees.common.Status.INVALID)

    # test that it passes on success
    count = py_trees.behaviours.Count(name="Count", fail_until=0, running_until=1, success_until=10, reset=False)
    timeout = py_trees.decorators.Timeout(child=count, duration=0.2)
    py_trees.display.print_ascii_tree(timeout)

    py_trees.tests.tick_tree(timeout, 1, 1, visitor)

    print("\n--------- Assertions ---------\n")
    print("timeout.status == py_trees.common.Status.RUNNING")
    assert(timeout.status == py_trees.common.Status.RUNNING)
    print("count.status == py_trees.common.Status.RUNNING")
    assert(count.status == py_trees.common.Status.RUNNING)

    py_trees.tests.tick_tree(timeout, 2, 2, visitor)

    print("\n--------- Assertions ---------\n")
    print("timeout.status == py_trees.common.Status.SUCCESS")
    assert(timeout.status == py_trees.common.Status.SUCCESS)
    print("count.status == py_trees.common.Status.SUCCESS")
    assert(count.status == py_trees.common.Status.SUCCESS)

    # test that it passes on failure
    failure = py_trees.behaviours.Failure()
    timeout = py_trees.decorators.Timeout(child=failure, duration=0.2)
    py_trees.display.print_ascii_tree(timeout)

    py_trees.tests.tick_tree(timeout, 1, 1, visitor)

    print("\n--------- Assertions ---------\n")
    print("timeout.status == py_trees.common.Status.FAILURE")
    assert(timeout.status == py_trees.common.Status.FAILURE)
    print("failure.status == py_trees.common.Status.FAILURE")
    assert(failure.status == py_trees.common.Status.FAILURE)

# def test_condition():
#     console.banner("Condition")
# 
#     Conditional = py_trees.meta.condition(py_trees.behaviours.Count, py_trees.common.Status.SUCCESS)
#     condition = Conditional(name="D", fail_until=2, running_until=2, success_until=10, reset=False)
# 
#     visitor = py_trees.visitors.DebugVisitor()
#     py_trees.tests.tick_tree(condition, 1, 1, visitor)
# 
#     print("\n--------- Assertions ---------\n")
#     print("condition.original.status == py_trees.common.Status.FAILURE")
#     assert(condition.original.status == py_trees.common.Status.FAILURE)
#     print("condition.status == py_trees.common.Status.RUNNING")
#     assert(condition.status == py_trees.common.Status.RUNNING)
# 
#     py_trees.tests.tick_tree(condition, 2, 2, visitor)
# 
#     print("\n--------- Assertions ---------\n")
#     print("condition.original.status == py_trees.common.Status.FAILURE")
#     assert(condition.original.status == py_trees.common.Status.FAILURE)
#     print("condition.status == py_trees.common.Status.RUNNING")
#     assert(condition.status == py_trees.common.Status.RUNNING)
# 
#     py_trees.tests.tick_tree(condition, 3, 3, visitor)
# 
#     print("\n--------- Assertions ---------\n")
#     print("condition.original.status == py_trees.common.Status.SUCCESS")
#     assert(condition.original.status == py_trees.common.Status.SUCCESS)
#     print("condition.status == py_trees.common.Status.SUCCESS")
#     assert(condition.status == py_trees.common.Status.SUCCESS)
