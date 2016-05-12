from lettuce import *
from config import *
import logging
import os
import ConfigParser

GLOBALS = {"resultdir" : "result"}
def wrt(string):
    world.log.info(string.encode('utf-8'))

@before.all
def before_all():
    os.system("rm -rf %s" % GLOBALS["resultdir"])
    os.system("mkdir -p %s" % GLOBALS["resultdir"])

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M%S',
                        filename=GLOBALS["resultdir"] + '/restCall.log', filemode='w')
    world.log = logging.getLogger()
    world.log.info("Test framework initialization")


@before.each_scenario
def before_each_scenario(scenario):
        world.log.info("****Started the Scenario - '%s'", scenario.name)

@after.each_scenario
def after_each_scenario(step):
    world.log.info("*** Finished the Scenario....\n\n")