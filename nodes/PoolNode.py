
import udi_interface
import sys
import time
import requests
import urllib3

LOGGER = udi_interface.LOGGER


class PoolNode(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name, allData, apiBaseUrl):

        super(PoolNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

        self.allData = allData
        self.apiBaseUrl = apiBaseUrl

    def start(self):

        self.allData = requests.get(
            url='{}/state/all'.format(self.apiBaseUrl))

        if self.allData.status_code == 200:
            self.setDriver('ST', 1)
        else:
            self.setDriver('ST', 0)

        self.allDataJson = self.allData.json()
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

        LOGGER.info("Pump Status  {}".format(
            self.allDataJson["pumps"][0]["circuits"][0]["circuit"]["isOn"]))
        pisOn = self.allDataJson["pumps"][0]["circuits"][0]["circuit"]["isOn"]
        if pisOn == True:
            self.setDriver('GV4', 1)
        if pisOn == False:
            self.setDriver('GV4', 0)

        LOGGER.info("Pump Watts  {}".format(
            self.allDataJson["pumps"][0]["watts"]))
        self.setDriver('GV5', self.allDataJson["pumps"][0]["watts"])

        LOGGER.info("Pump RPM  {}".format(
            self.allDataJson["pumps"][0]["rpm"]))
        self.setDriver('GV6', self.allDataJson["pumps"][0]["rpm"])

        LOGGER.info("Pump GPM  {}".format(
            self.allDataJson["pumps"][0]["flow"]))
        self.setDriver('GV7', self.allDataJson["pumps"][0]["flow"])

        LOGGER.info("Filter PSI  {}".format(
            self.allDataJson["filters"][0]["refPressure"]))
        self.setDriver('GV8', self.allDataJson["filters"][0]["refPressure"])

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
        json_data = {"id": 6, "state": True}  # True-Start False-Stop

        response = requests.put(
            'http://192.168.1.53:4200/state/circuit/setState', json=json_data)

        self.setDriver('ST', 1)

    def cmd_off(self, command):
        json_data = {"id": 6, "state": False}  # True-Start False-Stop

        response = requests.put(
            'http://192.168.1.53:4200/state/circuit/setState', json=json_data)

        self.setDriver('ST', 0)

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'GV0', 'value': 0, 'uom': 2, 'name': "Pool Running"},
        {'driver': 'GV1', 'value': None, 'uom': 17, 'name': "Air Temp"},
        {'driver': 'GV2', 'value': None, 'uom': 17, 'name': "Setpoint"},
        {'driver': 'GV3', 'value': None, 'uom': 17, 'name': "Pool Temp"},
        {'driver': 'GV4', 'value': None, 'uom': 2, 'name': "Pump Status"},
        {'driver': 'GV5', 'value': None, 'uom': 73, 'name': "Pump Watts"},
        {'driver': 'GV6', 'value': None, 'uom': 89, 'name': "Pump RPM"},
        {'driver': 'GV7', 'value': None, 'uom': 69, 'name': "Pump GPM"},
        {'driver': 'GV8', 'value': None, 'uom': 52, 'name': "Pump GPM"},
        {'driver': 'CLISPH', 'value': 0, 'uom': 17, 'name': "Setpoint adj"},
        {'driver': 'ST', 'value': 0, 'uom': 2, 'name': "Online"},
    ]

    id = 'poolnode'

    commands = {
        'DON': cmd_on,
        'DOF': cmd_off,
        'QUERY': query
    }
