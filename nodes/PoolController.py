
import udi_interface
import requests
import logging
import json

# My Template Node
from nodes import PoolNode
from nodes import SwitchNode
from nodes import PoolBodyNode
from nodes import TemplateNode

LOGGER = udi_interface.LOGGER
LOG_HANDLER = udi_interface.LOG_HANDLER
Custom = udi_interface.Custom
ISY = udi_interface.ISY

# IF you want a different log format than the current default
LOG_HANDLER.set_log_format(
    '%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')


class PoolController(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name):

        super(PoolController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = 'Pool Controller'  # override what was passed in
        self.hb = 0

        # Create data storage classes to hold specific data that we need
        # to interact with.
        self.Parameters = Custom(polyglot, 'customparams')
        self.Notices = Custom(polyglot, 'notices')
        self.TypedParameters = Custom(polyglot, 'customtypedparams')
        self.TypedData = Custom(polyglot, 'customtypeddata')

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.poly.ready()
        self.poly.addNode(self)

    def start(self):
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()
        self.discover()

    def parameterHandler(self, params):
        self.Parameters.load(params)
        LOGGER.debug('Loading parameters now')
        self.check_params()

    def poll(self, flag):
        if 'longPoll' in flag:
            LOGGER.debug('longPoll (controller)')
        else:
            LOGGER.debug('shortPoll (controller)')
            # self.discover()
            self.reportDrivers()
            self.query()

    def query(self, command=None):
        nodes = self.poly.getNodes()
        for node in nodes:
            nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        LOGGER.info('Starting Pool Controller')

        if self.api_url:
            self.apiBaseUrl = self.api_url
            # Get all data from nodejs pool controller api
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

            LOGGER.info("Air Temp  {}".format(
                self.allDataJson["temps"]["air"]))
            self.setDriver('GV1', self.allDataJson["temps"]["air"])

            LOGGER.info("Setpoint Temp  {}".format(
                self.allDataJson["temps"]["bodies"][0]["setPoint"]))
            self.setDriver(
                'GV2', self.allDataJson["temps"]["bodies"][0]["setPoint"])

            LOGGER.info("Pool Temp  {}".format(
                self.allDataJson["temps"]["bodies"][0]["temp"]))
            self.setDriver(
                'GV3', self.allDataJson["temps"]["bodies"][0]["temp"])

            # LOGGER.info("Temperatures {}".format(self.allDataJson["temps"]))
            # LOGGER.info("Pumps {}".format(self.allDataJson["pumps"]))
            # LOGGER.info("Filters {}".format(self.allDataJson["filters"]))
            # LOGGER.info("Valves {}".format(self.allDataJson["valves"]))
            # LOGGER.info("Virtual Circuits {}".format(
            #    self.allDataJson["virtualCircuits"]))
            LOGGER.info("Heaters {}".format(self.allDataJson["heaters"]))
            # LOGGER.info("Schedules {}".format(self.allDataJson["schedules"]))

        for i in self.allDataJson["circuits"]:
            name = i["name"]
            id = i["id"]
            isOn = i["isOn"]
            LOGGER.info(i["name"])  # , i["id"], i['isOn'])
            LOGGER.info(i["id"])
            LOGGER.info(i["isOn"])
            self.allDataJson = self.allDataJson
            address = 'zone_{}'.format(id)
            LOGGER.info(address)
            self.poly.addNode(SwitchNode(
                self.poly, self.address, address, name, self.allDataJson))
            # LOGGER.info('Found {} Circuits'.format(len(self.circuits)))
            self.poly.addNode(TemplateNode(
                self.poly, self.address, 'templateaddr', 'Template Node Name', self.allDataJson))
            self.poly.addNode(PoolBodyNode(
                self.poly, self.address, "body_1", "Pool Body", self.allDataJson))

    def delete(self):
        LOGGER.info('Oh God I\'m being deleted. No.')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def set_module_logs(self, level):
        logging.getLogger('urllib3').setLevel(level)

    def check_params(self):
        self.Notices.clear()
        default_api_url = "http://localhost:4200"

        self.api_url = self.Parameters.api_url
        if self.api_url is None:
            self.api_url = default_api_url
            LOGGER.error(
                'check_params: user not defined in customParams, please add it.  Using {}'.format(default_api_url))
            self.api_url = default_api_url

        # Add a notice if they need to change the user/circuits from the default.
        if self.api_url == default_api_url:
            self.Notices['auth'] = 'Please set proper api_url and circuits in configuration page'
            # self.Notices['test'] = 'This is only a test'

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

    id = 'controller'
    commands = {
        'QUERY': query,
        'SET_TEMP': cmd_set_temp,
    }
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2, 'name': "Online"},
        {'driver': 'GV0', 'value': 0, 'uom': 2, 'name': "Pool Running"},
        {'driver': 'GV1', 'value': None, 'uom': 17, 'name': "Air Temp"},
        {'driver': 'GV2', 'value': None, 'uom': 17, 'name': "Setpoint"},
        {'driver': 'GV3', 'value': None, 'uom': 17, 'name': "Pool Temp"},
        {'driver': 'CLISPH', 'value': 0, 'uom': 17, 'name': "Setpoint adj"},
    ]
