
import udi_interface
import sys
import time
import requests
import urllib3

LOGGER = udi_interface.LOGGER


class PoolNode(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name, allData):

        super(PoolNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

        apiBaseUrl = self.apiBaseUrl

    def start(self):

        allData = requests.get(
            url='{}/state/all'.format(self.apiBaseUrl))

        if allData.status_code == 200:
            self.setDriver('ST', 1)
        else:
            self.setDriver('ST', 0)

        self.allDataJson = allData.json()
        # LOGGER.info(self.allDataJson)

        LOGGER.info("Pool Running  {}".format(
            self.allDataJson["temps"]["bodies"][0]["isOn"]))

        isON = self.allDataJson["temps"]["bodies"][0]["isOn"]
        LOGGER.info(isON)
        if isON == True:
            self.setDriver('GV0', 1)
        if isON == False:
            self.setDriver('GV0', 0)

        LOGGER.info("Air Temp  {}".format(self.allDataJson["temps"]["air"]))
        self.setDriver('GV1', self.allDataJson["temps"]["air"])

        LOGGER.info("Setpoint Temp  {}".format(
            self.allDataJson["temps"]["bodies"][0]["setPoint"]))
        self.setDriver(
            'GV2', self.allDataJson["temps"]["bodies"][0]["setPoint"])

        LOGGER.info("Pool Temp  {}".format(
            self.allDataJson["temps"]["bodies"][0]["temp"]))
        self.setDriver('GV3', self.allDataJson["temps"]["bodies"][0]["temp"])
        self.http = urllib3.PoolManager()

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            LOGGER.debug('shortPoll (node)')
            self.start()
            self.query()

            LOGGER.debug('%s: get ST=%s', self.lpfx, self.getDriver('ST'))

    def cmd_on(self, command):

        self.setDriver('ST', 1)

    def cmd_off(self, command):

        self.setDriver('ST', 0)

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'GV0', 'value': 0, 'uom': 2, 'name': "Pool Running"},
        {'driver': 'GV1', 'value': None, 'uom': 17, 'name': "Air Temp"},
        {'driver': 'GV2', 'value': None, 'uom': 17, 'name': "Setpoint"},
        {'driver': 'GV3', 'value': None, 'uom': 17, 'name': "Pool Temp"},
        {'driver': 'CLISPH', 'value': 0, 'uom': 17, 'name': "Setpoint adj"},
        {'driver': 'ST', 'value': 0, 'uom': 2, 'name': "Online"},
    ]

    id = 'poolnode'

    commands = {
        'DON': cmd_on,
        'DOF': cmd_off,
        'QUERY': query
    }
