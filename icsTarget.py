#!/usr/bin/python3
from config_reader import ConfigReader
from api_requester import ApiRequester

import sys

import target_run

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


if __name__ == "__main__":
    sys.stdout = Unbuffered(sys.stdout)
    progname = "icsTarget"

    print(progname + " started")

    # Arguments parsing.
    ##config_file = "config.cfg"
    ##if len(sys.argv) > 1:
    ##    config_file = sys.argv[1]
    ##else:
    ##    print("Config path was not specified in program args, defaulting to '%s'." % config_file)

    # Init.
    ##cfg = ConfigReader()
    ##cfg.load_config_from_file(config_file)
    ##api_req = ApiRequester(cfg)
    # Worker.
    # device_id = cfg.get_value("deviceID")
    # device_path = cfg.get_value("devicePath")
    # event_path = cfg.get_value("journalEvent")
    # event_path_sub = cfg.get_value("journalEventData")
    target = target_run.TargetExample(api_requester= None)##api_req)
    target.run()
    print(progname + " finished")
