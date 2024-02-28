
import udi_interface
import sys
import time
import requests
import urllib3

LOGGER = udi_interface.LOGGER


class BodyNode(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name, status, number, apiBaseUrl):
        super(BodyNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.status = status
        self.number = number
        self.apiBaseUrl = apiBaseUrl
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

        self.setDriver('GV1', airTemp)
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
                self.setDriver('ST', status)
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

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2, 'name': "Online"},
        {'driver': 'GV0', 'value': 0, 'uom': 25, 'name': "Heat Mode"},
        {'driver': 'GV1', 'value': 0, 'uom': 17, 'name': "Outside Air Temp"},
        {'driver': 'GV2', 'value': 0, 'uom': 17, 'name': "Pool Temp"},
        {'driver': 'GV3', 'value': 0, 'uom': 17, 'name': "Pool Setpoint"},
        {'driver': 'GV4', 'value': 0, 'uom': 25, 'name': "Spa Status"},
        {'driver': 'GV5', 'value': 0, 'uom': 17, 'name': "Spa Temp"},
        {'driver': 'GV6', 'value': 0, 'uom': 17, 'name': "Spa Setpoint"}
    ]

    id = 'BODY'

    commands = {
        'QUERY': query
    }
