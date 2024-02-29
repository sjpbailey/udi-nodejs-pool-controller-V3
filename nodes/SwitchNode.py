
import udi_interface
import json
import requests
import sys
import time
import urllib3

LOGGER = udi_interface.LOGGER


class SwitchNode(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name, id, allDataJson):

        super(SwitchNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.address = address
        self.name = name
        self.allDataJson = allDataJson
        self.id = self.id

    def start(self):
        LOGGER.info(self.address)
        self.http = urllib3.PoolManager()

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            LOGGER.debug('shortPoll (node)')
            # self.setDriver('ST', 1)

    def cmd_on(self, command):
        json_data = {
            'id': self.id,
            'isOn': 1,
        }

        response = requests.put(
            'http://192.168.1.53:4200/state/circuit/setState/',  json=json_data)

        self.setDriver('ST', 1)

    def cmd_off(self, command):
        json_data = {
            'id': self.id,
            'isOn': 0,
        }

        response = requests.put(
            'http://192.168.1.53:4200/state/circuit/setState/',  json=json_data)

        self.setDriver('ST', 0)

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': 2}
    ]

    id = 'switchnodeid'

    commands = {
        'DON': cmd_on,
        'DOF': cmd_off,
        'QUERY': query
    }
