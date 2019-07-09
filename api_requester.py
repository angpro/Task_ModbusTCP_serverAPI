from api_requester_common import *

import json
import datetime
from threading import RLock


class ApiRequester(ApiRequesterCommon):
    """Sends requests to REST API server"""

    def __init__(self, cfg):
        """
        :param cfg: ConfigReader instance, used to load configuration from config file
        :return: None
        """
        ApiRequesterCommon.__init__(self, cfg)

        self._node_id = cfg.get_value("nodeID")
        # self._netflowPath = cfg.get_value("netflowPath")
        self._sa_monitor_path = cfg.get_value("nodeMonitorPath").format(node_id=str(self._node_id))

        self._device_id = cfg.get_value("deviceID")
        self._device_path = cfg.get_value("devicePath")
        self._event_path = cfg.get_value("journalEvent")
        self._event_path_sub = cfg.get_value("journalEventData")

        self._lock = RLock()

    # TODO: needs refactoring for the new server_request api
    def _blocking_server_request(self, path, data=None, eid=None, method=None):
        acquired = self._lock.acquire(timeout=5)
        if not acquired:
            print("Error: timeout when tried to acquire lock for api. Request was not sent")
            return None

        server_reply = self.server_request(path=path, data=data, eid=eid, method=method)
        self._lock.release()
        return server_reply

    def send_monitor(self, cpu_usage, ram_usage, disk_usage, services):
        d = {
            "current_time": datetime.datetime.now().strftime("%FT%TZ"),
            "cpu": cpu_usage,
            "RAM": ram_usage,
            "hdd": disk_usage,
            "services": services
        }
        try:
            print(d)
            data = json.dumps(d)
            answer = self._blocking_server_request(path=self._sa_monitor_path, data=data)
            if not answer:
                return None

            # TODO: make it optional. DEBUG level or smthing like that
            print('Sent to server: ', data)
            return json.loads(answer)

        except KeyError as err:
            print_unexpected_json_error_key(err, str(d), self._device_path)
        except (TypeError, ValueError) as err:
            print_unexpected_json_error(err, str(d), self._device_path)

    def get_interfaces(self):
        return json.loads(self._blocking_server_request(self._device_path, method="GET"))['results']

    def patch_interface(self, iface_id, data):
        self._blocking_server_request(path=self._device_path, eid=iface_id, data=json.dumps(data), method="PATCH")
