import jsoncfg

# dict of available parameters with their types
CONFIG_ENTRIES = {"deviceID": int,
                  "deviceHost": str,
                  "address": str,
                  "port": int,
                  "username": str,
                  "password": str,
                  "nodeID": int,
                  "devicePath": str,
                  "authTokenPath": str,
                  "deviceDevice": str,
                  "deviceMonitor": str,
                  "journalEvent": str,
                  "journalEventData": str,
                  "journalSystemEvent": str,
                  "pcapDumps": str,
                  "pcapLocalDir": str,
                  "serverDoesNotRespondTimeout": int,
                  "physicalInterfacesPath": str,
                  "nodeMonitorPath": str,
                  "saMonitorSendPeriod": int,
                  "appProtoEventsInterval": int,
                  "websocketPath": str,
                  "printHeartbeat": bool,
                  "appProtoFileSize": int,
                  "appProtoFiles": int,
                  }


class ConfigReader:
    def __init__(self, config_entries=None):
        if not config_entries:
            config_entries = CONFIG_ENTRIES

        self.config_entries = config_entries

        self.filename = ""
        self.config = None

    def load_config_from_file(self, filename):
        try:
            self.config = jsoncfg.load_config(filename)

            for entry in self.config_entries:
                if entry not in self.config:
                    print("Error parsing config, parameter '%s' was not specified, exiting." % entry)
                    exit(4)
            self.filename = filename
        except (IOError, UnicodeDecodeError) as err:
            print("Can not read config file '%s': %s" % (filename, err))
            return exit(4)

    def get_value(self, parameter):
        if parameter not in self.config:
            print("Wrong configuration parameter '%s' requested. Exiting." % parameter)
            exit(4)

        value = self.config[parameter]()
        if not isinstance(value, self.config_entries[parameter]):
            print("Config error, parameter '%s' has unexpected value type '%s'. Expected: %s, exiting."
                  % (parameter, type(value), self.config_entries[parameter]))
            exit(4)
        return value

    def check_options_types(self):
        for entry in self.config_entries:
            self.get_value(entry)
