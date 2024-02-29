
import udi_interface
import requests
import logging
import json

# My Template Node
from nodes import PoolNode
from nodes import SwitchNode
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

        # Subscribe to various events from the Interface class.  This is
        # how you will get information from Polyglog.  See the API
        # documentation for the full list of events you can subscribe to.
        #
        # The START event is unique in that you can subscribe to
        # the start event for each node you define.

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)
        self.poly.subscribe(self.poly.POLL, self.poll)

        # Tell the interface we have subscribed to all the events we need.
        # Once we call ready(), the interface will start publishing data.
        self.poly.ready()

        # Tell the interface we exist.
        self.poly.addNode(self)

    def start(self):

        # Send the profile files to the ISY if neccessary. The profile version
        # number will be checked and compared. If it has changed since the last
        # start, the new files will be sent.
        self.poly.updateProfile()

        # Send the default custom parameters documentation file to Polyglot
        # for display in the dashboard.
        self.poly.setCustomParamsDoc()

        # Device discovery. Here you may query for your device(s) and
        # their capabilities.  Also where you can create nodes that
        # represent the found device(s)
        self.discover()

        # Here you may want to send updated values to the ISY rather
        # than wait for a poll interval.  The user will get more
        # immediate feedback that the node server is running

    """NOTE: Be careful to not change parameters here. Changing
    parameters will result in a new event, causing an infinite loop.
    """

    def parameterHandler(self, params):
        self.Parameters.load(params)
        LOGGER.debug('Loading parameters now')
        self.check_params()

    def poll(self, flag):
        if 'longPoll' in flag:
            LOGGER.debug('longPoll (controller)')
            # self.reportDrivers()
        else:
            LOGGER.debug('shortPoll (controller)')

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
            self.allDataJson = allData.json()
            # LOGGER.info(self.allDataJson)

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

            LOGGER.info("Temperatures {}".format(self.allDataJson["temps"]))
            LOGGER.info("Pumps {}".format(self.allDataJson["pumps"]))
            LOGGER.info("Filters {}".format(self.allDataJson["filters"]))
            LOGGER.info("Valves {}".format(self.allDataJson["valves"]))
            LOGGER.info("Virtual Circuits {}".format(
                self.allDataJson["virtualCircuits"]))
            LOGGER.info("Heaters {}".format(self.allDataJson["heaters"]))
            LOGGER.info("Schedules {}".format(self.allDataJson["schedules"]))

        for i in self.allDataJson["circuits"]:
            name = i["name"]
            id = i["id"]
            isOn = i["isOn"]
            LOGGER.info(i["name"])  # , i["id"], i['isOn'])
            LOGGER.info(i["id"])
            LOGGER.info(i["isOn"])
            LOGGER.info(i["id"])
            self.allDataJson = self.allDataJson
            address = id
            address = 'zone_{}'.format(address)
            self.poly.addNode(SwitchNode(
                self.poly, self.address, address, name, self.allDataJson, id))

            # self.poly.addNode(TemplateNode(
            #    self.poly, self.address, address, name))

            # self.poly.addNode(node)
            # Discover pool circuit nodes
            # LOGGER.info('Found {} Circuits'.format(len(self.circuits)))

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

    def remove_notice_test(self, command):
        LOGGER.info('remove_notice_test: notices={}'.format(self.Notices))
        # Remove the test notice
        self.Notices.delete('test')

    def remove_notices_all(self, command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.Notices))
        # Remove all existing notices
        self.Notices.clear()

    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'REMOVE_NOTICE_TEST': remove_notice_test,
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2, 'name': "Online"},
        {'driver': 'GV1', 'value': None, 'uom': 17, 'name': "Air Temp"},
        {'driver': 'GV2', 'value': None, 'uom': 17, 'name': "Setpoint"},
        {'driver': 'GV3', 'value': None, 'uom': 17, 'name': "Pool Temp"},
    ]
