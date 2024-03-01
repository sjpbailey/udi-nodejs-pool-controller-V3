
import udi_interface
import json
import requests
import sys
import time
import urllib3

LOGGER = udi_interface.LOGGER


class BodyNode(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name, allDataJson):

        super(BodyNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.address = address
        LOGGER.info(self.address)
        self.name = name
        LOGGER.info(name)
        self.allDataJson = allDataJson
        id = address.strip('zone_')
        id1 = id
        LOGGER.info(id1)
        self.id1 = id1

    def start(self):
        LOGGER.info(self.address)
        self.http = urllib3.PoolManager()
        self.allDataJson = self.allDataJson
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
        self.setDriver(
            'GV3', self.allDataJson["temps"]["bodies"][0]["temp"])

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            LOGGER.debug('shortPoll (node)')
            self.reportDrivers()
            self.start

    def cmd_on(self, command):

        json_data = {
            'id': self.id1,
            'isOn': 1,
        }

        response = requests.put(
            'http://192.168.1.53:4200/state/circuit/setState/',  json=json_data)

        # self.setDriver('ST', 1)

    def cmd_off(self, command):

        json_data = {
            'id': self.id1,
            'isOn': 0,
        }

        response = requests.put(
            'http://192.168.1.53:4200/state/circuit/setState/',  json=json_data)

        # self.setDriver('ST', 0)

    def query(self, command=None):
        self.reportDrivers()

    drivers = [
        {'driver': 'GV0', 'value': 0, 'uom': 2, 'name': "Pool Running"},
        {'driver': 'GV1', 'value': None, 'uom': 17, 'name': "Air Temp"},
        {'driver': 'GV2', 'value': None, 'uom': 17, 'name': "Setpoint"},
        {'driver': 'GV3', 'value': None, 'uom': 17, 'name': "Pool Temp"},
        {'driver': 'CLISPH', 'value': 0, 'uom': 17, 'name': "Setpoint adj"},
    ]

    id = 'bodynodeid'

    commands = {
        # 'DON': cmd_on,
        # 'DOF': cmd_off,
        'QUERY': query
    }
