
import udi_interface
import sys
import time
import json
import requests
import copy
import logging

# My Template Node
from nodes import BodyNode
from nodes import CircuitNode
from nodes import TempNode

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
        self.TypedData = Custom(polyglot, 'customtypeddata')

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.LOGLEVEL, self.handleLevelChange)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)
        polyglot.subscribe(polyglot.ADDNODEDONE, self.node_queue)
        self.poly.subscribe(self.poly.POLL, self.poll)

        # Tell the interface we have subscribed to all the events we need.
        # Once we call ready(), the interface will start publishing data.
        self.poly.ready()

        # Tell the interface we exist.
        self.poly.addNode(self)

    def parameterHandler(self, params):
        self.Parameters.load(params)
        LOGGER.debug('Loading parameters now')
        self.check_params()

    def handleLevelChange(self, level):
        LOGGER.info('New log level: {}'.format(level))

    def start(self):
        self.discover()
        self.poly.updateProfile()
        LOGGER.info('Starting Pool Controller')
        # Discover pool circuit nodes
        # LOGGER.info('Found {} Circuits'.format(len(self.circuits)))

        if self.api_url:
            self.apiBaseUrl = self.api_url
            # Get all data from nodejs pool controller api
            allData = requests.get(
                url='{}/state/all'.format(self.apiBaseUrl))
            self.allDataJson = allData.json()
            LOGGER.info(self.allDataJson)

            temperatures = ['spa', 'pool']
            for temperature in temperatures:

                temperatureData = requests.get(
                    url='{}/state/temps'.format(self.apiBaseUrl))
                self.temperatureDataJson = temperatureData.json()
                LOGGER.info(self.temperatureDataJson)

                id = temperature
                LOGGER.info("temperature 1")
                LOGGER.info(temperature)

                address = ('{}_heat'.format(temperature))
                LOGGER.info("address 1")
                LOGGER.info(address)

                name = ('{} Heat'.format(temperature)).title()
                LOGGER.info("name 1")
                LOGGER.info(name)

                type = temperature
                LOGGER.info("temperature 2")
                LOGGER.info(type)

                self.poly.addNode(TempNode(
                    self, self.address, id, address, name, type, self.temperatureDataJson, self.apiBaseUrl))

                LOGGER.info('Temperature {} already configured.'.format(name))

                """if self.circuits:

                    # Get the list of circuits that are not in use
                    self.circuitsNotUsed = eval(
                        '[' + self.circuits + ']')

                    # Get circuits in use
                    allCircuits = requests.get(
                        url='{}/state/circuits'.format(self.apiBaseUrl))
                    circuitsUsed = copy.deepcopy(allCircuits)
                    LOGGER.info(allCircuits)
                    circuitsNotUsed = self.circuitsNotUsed
                    #for key in allCircuits.keys():
                    #    for circuitNotUsed in circuitsNotUsed:
                    #        if key == circuitNotUsed:
                    #            del circuitsUsed[key]

                    self.circuits = circuitsUsed

                else:
                    self.circuits = allCircuits

        #except Exception as ex:
        #    LOGGER.error(
        #        'Error reading NodeJs Pool Controller API url from Polyglot Configuration: %s', str(ex))
        #    return True
            # Add pool and spa temperature nodes
        if self.circuits:

            for circuit in sorted(self.circuits):  # key=int):
                id = circuit
                LOGGER.info(id)
                number = circuit
                address = self.circuits[circuit].get('numberStr')
                name = self.circuits[circuit].get('friendlyName').title()
                status = self.circuits[circuit].get('status')

                if address not in self.nodes:
                    self.poly.addNode(CircuitNode(
                        self, self.address, id, address, name, status, number, self.apiBaseUrl))
                    self.poly.addNode(BodyNode(
                        self, self.address, id, address, name, status, number, self.apiBaseUrl))
                else:
                    LOGGER.info('Circuit {} already configured.'.format(name))"""

    def poll(self, flag):
        if 'longPoll' in flag:
            LOGGER.debug('longPoll (controller)')
        else:
            LOGGER.debug('shortPoll (controller)')

    def query(self, command=None):
        nodes = self.poly.getNodes()
        for node in nodes:
            nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        # Discover pool circuit nodes
        LOGGER.info('Found {} Circuits'.format(len(self.circuits)))

    def update(self, report=True):

        if self.apiBaseUrl:
            # Get node js pool controller status
            controllerData = requests.get(
                url='{}/state/all'.format(self.apiBaseUrl))
            if controllerData.status_code == 200:
                self.setDriver('ST', 1, report)
            else:
                self.setDriver('ST', 0, report)

    def update(self, report=True):
        if self.apiBaseUrl:
            # Get node js pool controller status
            controllerData = requests.get(url='{}/all'.format(self.apiBaseUrl))
            if controllerData.status_code == 200:
                self.setDriver('ST', 1, report)
            else:
                self.setDriver('ST', 0, report)

    def delete(self):
        LOGGER.info('Oh No I\'m being deleted. No.')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def set_module_logs(self, level):
        logging.getLogger('urllib3').setLevel(level)

    def check_params(self):
        self.Notices.clear()
        default_api_url = "http://localhost:3000"
        default_circuits = "'0','1''"

        self.api_url = self.Parameters.api_url
        if self.api_url is None:
            self.api_url = default_api_url
            LOGGER.error(
                'check_params: user not defined in customParams, please add it.  Using {}'.format(default_api_url))
            self.api_url = default_api_url

        self.circuits = self.Parameters.circuits
        if self.circuits is None:
            self.circuits = default_circuits
            LOGGER.error('check_params: circuits not defined in customParams, please add it.  Using {}'.format(
                default_circuits))
            self.circuits = default_circuits

        # Add a notice if they need to change the user/circuits from the default.
        if self.api_url == default_api_url or self.circuits == default_circuits:
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
    ]
