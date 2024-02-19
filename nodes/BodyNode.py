
import udi_interface
import sys
import time
import requests
import urllib3

LOGGER = udi_interface.LOGGER
_ISY_BOOL_UOM = 2  # Used for reporting status values for Controller node
# Index UOM for custom states (must match editor/NLS in profile):
_ISY_INDEX_UOM = 25
_ISY_TEMP_F_UOM = 17  # UOM for temperatures
_ISY_THERMO_MODE_UOM = 67  # UOM for thermostat mode
_ISY_THERMO_HCS_UOM = 66  # UOM for thermostat heat/cool state


class BodyNode(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name, status, number, apiBaseUrl):
        super(BodyNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

    def start(self):
        # Get temperatures
        temperatureData = requests.get(
            url='{}/temperatures'.format(self.apiBaseUrl))
        temperatureDataJson = temperatureData.json()['temperature']
        airTemp = temperatureDataJson['airTemp']
        poolTemp = temperatureDataJson['poolTemp']
        poolSetpoint = temperatureDataJson['poolSetPoint']
        spaTemp = temperatureDataJson['spaTemp']
        spaSetpoint = temperatureDataJson['spaSetPoint']
        poolHeatMode = temperatureDataJson['poolHeatMode']
        spaHeatMode = temperatureDataJson['spaHeatMode']

        self.setDriver('CLITEMP', airTemp)
        self.setDriver('GV2', poolTemp)
        self.setDriver('GV3', poolSetpoint)
        self.setDriver('GV5', spaTemp)
        self.setDriver('GV6', spaSetpoint)

        # Get specific circuit statuses
        allData = requests.get(url='{}/all'.format(self.apiBaseUrl))
        allDataJson = allData.json()
        circuits = allDataJson['circuit']
        for circuit in circuits:
            circuitType = circuits[circuit].get('circuitFunction')
            if circuitType == 'Pool':
                status = circuits[circuit].get('status')
                self.setDriver('GV1', status)
                if poolHeatMode and status == 1:
                    self.setDriver('GV0', 1)
            if circuitType == 'Spa':
                status = circuits[circuit].get('status')
                self.setDriver('GV4', status)
                if spaHeatMode and status == 1:
                    self.setDriver('GV0', 1)

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            LOGGER.debug('shortPoll (node)')
            if int(self.getDriver('ST')) == 1:
                self.setDriver('ST', 0)
            else:
                self.setDriver('ST', 1)
            LOGGER.debug('%s: get ST=%s', self.lpfx, self.getDriver('ST'))

    def cmd_on(self, command):
        """
        Example command received from ISY.
        Set DON on TemplateNode.
        Sets the ST (status) driver to 1 or 'True'
        """
        self.setDriver('ST', 1)

    def cmd_off(self, command):
        """
        Example command received from ISY.
        Set DOF on TemplateNode
        Sets the ST (status) driver to 0 or 'False'
        """
        self.setDriver('ST', 0)

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': _ISY_BOOL_UOM},
        {'driver': 'GV0', 'value': 0, 'uom': _ISY_INDEX_UOM},
        {'driver': 'CLITEMP', 'value': 0, 'uom': _ISY_TEMP_F_UOM},
        {'driver': 'GV1', 'value': 0, 'uom': _ISY_INDEX_UOM},
        {'driver': 'GV2', 'value': 0, 'uom': _ISY_TEMP_F_UOM},
        {'driver': 'GV3', 'value': 0, 'uom': _ISY_TEMP_F_UOM},
        {'driver': 'GV4', 'value': 0, 'uom': _ISY_INDEX_UOM},
        {'driver': 'GV5', 'value': 0, 'uom': _ISY_TEMP_F_UOM},
        {'driver': 'GV6', 'value': 0, 'uom': _ISY_TEMP_F_UOM}
    ]

    id = 'BODY'

    commands = {
        'DON': cmd_on,
        'DOF': cmd_off,
        'QUERY': query
    }
