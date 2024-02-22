
import udi_interface
import sys
import time
import requests
import copy
import urllib3

LOGGER = udi_interface.LOGGER

_ISY_BOOL_UOM = 2  # Used for reporting status values for Controller node
# Index UOM for custom states (must match editor/NLS in profile):
_ISY_INDEX_UOM = 25
_ISY_TEMP_F_UOM = 17  # UOM for temperatures
_ISY_THERMO_MODE_UOM = 67  # UOM for thermostat mode
_ISY_THERMO_HCS_UOM = 66  # UOM for thermostat heat/cool state


class CircuitNode(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name, status, number, apiBaseUrl):
        super(CircuitNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.status = status
        self.number = number
        self.apiBaseUrl = apiBaseUrl

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

    def start(self):
        circuitData = requests.get(
            url='{0}/circuit/{1}'.format(self.apiBaseUrl, self.number))
        circuitDataJson = circuitData.json()
        status = circuitDataJson['status']
        self.setDriver('ST', status)

        self.http = urllib3.PoolManager()

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            LOGGER.debug('shortPoll (node)')

    def cmd_on(self, command):
        requests.get(
            url='{0}/circuit/{1}/toggle'.format(self.apiBaseUrl, self.number))
        self.update()
        print(self.name + ' turned on')

    def cmd_off(self, command):
        requests.get(
            url='{0}/circuit/{1}/toggle'.format(self.apiBaseUrl, self.number))
        self.update()
        print(self.name + ' turned off')

    def query(self, command=None):
        self.reportDrivers()

    drivers = [{'driver': 'ST', 'value': 0, 'uom':  _ISY_INDEX_UOM}]

    id = 'CIRCUIT'

    commands = {
        'DON': cmd_on,
        'DOF': cmd_off,

    }
