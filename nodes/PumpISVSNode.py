''' Intelliflo VS Pump '''
import udi_interface
import sys
import time
import requests
import urllib3

LOGGER = udi_interface.LOGGER


class PumpISVSNode(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name, allData, apiBaseUrl, api_url):

        super(PumpISVSNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

        # self.allData = allData
        self.apiBaseUrl = apiBaseUrl
        self.api_url = api_url

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

        LOGGER.info("Pump Status  {}".format(
            self.allDataJson["pumps"][0]["circuits"][0]["circuit"]["isOn"]))
        pisOn = self.allDataJson["pumps"][0]["circuits"][0]["circuit"]["isOn"]
        if pisOn == True:
            self.setDriver('GV1', 1)
        if pisOn == False:
            self.setDriver('GV1', 0)

        LOGGER.info("Pump Watts  {}".format(
            self.allDataJson["pumps"][0]["watts"]))
        self.setDriver('GV2', self.allDataJson["pumps"][0]["watts"])

        LOGGER.info("Pump RPM  {}".format(
            self.allDataJson["pumps"][0]["rpm"]))
        self.setDriver(
            'GV3', self.allDataJson["pumps"][0]["circuits"][0]['units']['val'])

        LOGGER.info("Pump GPM  {}".format(
            self.allDataJson["pumps"][0]["flow"]))
        self.setDriver('GV4', self.allDataJson["pumps"][0]["flow"])
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
            self.api_url + '/state/circuit/setState', json=json_data)

    def cmd_off(self, command):
        json_data = {"id": 6, "state": False}  # True-Start False-Stop

        response = requests.put(
            self.api_url + '/state/circuit/setState', json=json_data)

    def query(self, command=None):
        self.reportDrivers()

    def cmd_set_sped(self, command):
        value = int(command.get('value'))
        json_data = {"id": 50, "circuits": [
            {"relay": value, "units": {"val": 1}, "id": 1, "circuit": 6}]}

        response = requests.put(
            self.api_url + '/config/pump', json=json_data)

    drivers = [
        {'driver': 'GV0', 'value': 0, 'uom': 25, 'name': "Pool Running"},
        {'driver': 'GV1', 'value': None, 'uom': 25, 'name': "Pump Status"},
        {'driver': 'GV2', 'value': None, 'uom': 73, 'name': "Pump Watts"},
        {'driver': 'GV3', 'value': None, 'uom': 89, 'name': "Pump RPM"},
        {'driver': 'GV4', 'value': None, 'uom': 69, 'name': "Pump GPM"},
        {'driver': 'SPDSPH', 'value': 0, 'uom': 25, 'name': "Speed Relays"},
        {'driver': 'ST', 'value': 0, 'uom': 25, 'name': "Online"},
    ]

    id = 'pumpIvf'

    commands = {
        'DON': cmd_on,
        'DOF': cmd_off,
        'SET_SPEED': cmd_set_sped,
        'QUERY': query
    }
