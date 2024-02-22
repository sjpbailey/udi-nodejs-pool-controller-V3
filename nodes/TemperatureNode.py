
import udi_interface
import sys
import time
import urllib3
import requests

LOGGER = udi_interface.LOGGER

_ISY_BOOL_UOM = 2  # Used for reporting status values for Controller node
# Index UOM for custom states (must match editor/NLS in profile):
_ISY_INDEX_UOM = 25
_ISY_TEMP_F_UOM = 17  # UOM for temperatures
_ISY_THERMO_MODE_UOM = 67  # UOM for thermostat mode
_ISY_THERMO_HCS_UOM = 66  # UOM for thermostat heat/cool state


class TemperatureNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, type, temperatureDataJson, apiBaseUrl):

        super(TemperatureNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.name = name
        self.type = type
        self.temperatureDataJson = temperatureDataJson
        self.apiBaseUrl = apiBaseUrl

    def start(self, report=True):
        temperatureData = requests.get(
            url='{}/temperatures'.format(self.apiBaseUrl))
        temperatureDataJson = temperatureData.json()['temperature']
        if self.type == 'spa':
            status = temperatureDataJson['spaHeatMode']
            temperature = temperatureDataJson['spaTemp']
            setPoint = temperatureDataJson['spaSetPoint']
        else:
            status = temperatureDataJson['poolHeatMode']
            temperature = temperatureDataJson['poolTemp']
            setPoint = temperatureDataJson['poolSetPoint']

        self.setDriver('ST', status, report)
        self.setDriver('CLISPH', setPoint, report)
        self.setDriver('CLITEMP', temperature, report)

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            LOGGER.debug('shortPoll (node)')

    def cmd_don(self, command):
        temperatureData = requests.get(
            url='{}/temperatures'.format(self.apiBaseUrl))
        temperatureDataJson = temperatureData.json()['temperature']
        if self.type == 'spa':
            status = temperatureDataJson['spaHeatMode']
            if status == 0:
                requests.get(url='{}/spaheat/mode/1'.format(self.apiBaseUrl))
        else:
            status = temperatureDataJson['poolHeatMode']
            if status == 0:
                requests.get(url='{}/poolheat/mode/1'.format(self.apiBaseUrl))

    def cmd_dof(self, command):
        temperatureData = requests.get(
            url='{}/temperatures'.format(self.apiBaseUrl))
        temperatureDataJson = temperatureData.json()['temperature']
        if self.type == 'spa':
            status = temperatureDataJson['spaHeatMode']
            if status == 1:
                requests.get(url='{}/spaheat/mode/0'.format(self.apiBaseUrl))
        else:
            status = temperatureDataJson['poolHeatMode']
            if status == 1:
                requests.get(url='{}/poolheat/mode/0'.format(self.apiBaseUrl))

    def cmd_set_temp(self, command):
        value = int(command.get('value'))
        if self.type == 'spa':
            requests.get(
                url='{0}/spaheat/setpoint/{1}'.format(self.apiBaseUrl, value))
            self.update()
        else:
            requests.get(
                url='{0}/poolheat/setpoint/{1}'.format(self.apiBaseUrl, value))
            self.update()

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': _ISY_INDEX_UOM},
        {'driver': 'CLISPH', 'value': 0, 'uom': _ISY_TEMP_F_UOM},
        {'driver': 'CLITEMP', 'value': 0, 'uom': _ISY_TEMP_F_UOM},
        {'driver': 'CLIMD', 'value': 0, 'uom': _ISY_THERMO_MODE_UOM},
        {'driver': 'CLIHCS', 'value': 0, 'uom': _ISY_THERMO_HCS_UOM},
        {'driver': 'CLISPC', 'value': 0, 'uom': _ISY_TEMP_F_UOM}
    ]

    id = 'TEMPERATURE'

    """
    This is a dictionary of commands. If ISY sends a command to the NodeServer,
    this tells it which method to call. DON calls setOn, etc.
    """
    commands = {
        'DON': cmd_don,
        'DOF': cmd_dof,
        'SET_TEMP': cmd_set_temp
    }
