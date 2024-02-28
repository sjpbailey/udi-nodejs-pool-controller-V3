
import udi_interface
import sys
import time
import requests
import copy
import urllib3

LOGGER = udi_interface.LOGGER


class CircuitNode(udi_interface.Node):

    def __init__(self, polyglot, primary, address, id, name, isOn, allDataJson):
        super(CircuitNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (id, name)
        self.id = id
        self.name = name
        self.isOn = isOn

        self.number = id
        self.allDataJson = allDataJson

        self.poly.subscribe(self.poly.START, self.start, id)
        self.poly.subscribe(self.poly.POLL, self.poll)

    def start(self):
        if self.isOn == True:
            self.setDriver('GV1', 1)
        else:
            self.setDriver('GV1', 0)

        """for i in self.allDataJson["circuits"]:
            name = i(["name"])
            LOGGER.info(i["name"])  # , i["id"], i['isOn'])
            address = i(["id"])
            id = i(["id"])
            LOGGER.info(i["id"])"""

        """circuitData = requests.get(
            url='{0}/circuit/{1}'.format(self.apiBaseUrl, self.number))
        circuitDataJson = circuitData.json()
        status = circuitDataJson['status']
        """

        self.http = urllib3.PoolManager()

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            LOGGER.debug('shortPoll (node)')

    def cmd_on(self, command):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        json_data = {
            'id': 2,
            'isOn': 1,
        }

        response = requests.put(
            'http://192.168.1.53:4200/state/circuit/setState/', headers=headers, json=json_data)

        """requests.get(
            url='{0}/circuit/{1}/toggle'.format(self.apiBaseUrl, self.number))
        self.update()
        print(self.name + ' turned on')"""

    def cmd_off(self, command):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        json_data = {
            'id': 2,
            'isOn': 0,
        }

        response = requests.put(
            'http://192.168.1.53:4200/state/circuit/setState/', headers=headers, json=json_data)

        """requests.get(
            url='{0}/circuit/{1}/toggle'.format(self.apiBaseUrl, self.number))
        self.update()
        print(self.name + ' turned off')"""

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2, 'name': "Online"},
        {'driver': 'GV1', 'value': 0, 'uom': 2, 'name': "Online"}
    ]

    id = 'CIRCUIT'

    commands = {
        'DON': cmd_on,
        'DOF': cmd_off,
        'QUERY': query,

    }
