#import cpu_load_counter
#import memory_usage
#import systemd_parser
#import netflow_sender
#import interfaces_monitor

import time
import threading
#import modbus_server
from Server import run_server

class TargetExample:
    def __init__(self, api_requester, ):
        #self._modbus = systemd_parser.SystemdParser()
        self._api_req = api_requester
        # self._device_id = device_id
        # self._device_path = device_path
        # self._event_path = event_path
        # self._event_path_sub = event_path_sub
        #self.path = None
        ##self.path = ""
        ##self._api_req.get_token()  # to avoid race condition

    def run(self):
        target_thread = threading.Thread(target=run_server()) #(value_value_value_api_requester=self._api_req, value_value_value_path=self.path))
        target_thread.setDaemon(True)
        target_thread.start()
        #while target_thread.is_alive():
        #    time.sleep(0.1)
        print("One of threads have unexpectedly finished, exiting...")
        exit(1)
        #while target_thread.is_alive():
        #    time.sleep(0.1)

    """
    self._api_req.server_request(self, path, scheme=None, address=None, port=None, data=None, put=False, eid=None, method=None)
    def _target(self):
        ip = self._api_req.get_public_ip()
        print("target ip:", ip)
        self._target_mb = modbus_server.ModbusTcpServer(ip)
        while True:
            # todo:
            time.sleep(0.1)
            
    def run(self):
        target_thread = threading.Thread(target=self._target)
        target_thread.setDaemon(True)
        target_thread.start()
        while target_thread.is_alive():
            time.sleep(0.1)
    """




