
import udi_interface
import sys
import time
import json
import requests
import copy

# My Template Node
from nodes import BodyNode

"""
Some shortcuts for udi interface components

- LOGGER: to create log entries
- Custom: to access the custom data class
- ISY:    to communicate directly with the ISY (not commonly used)
"""
LOGGER = udi_interface.LOGGER
LOG_HANDLER = udi_interface.LOG_HANDLER
Custom = udi_interface.Custom
ISY = udi_interface.ISY

# IF you want a different log format than the current default
LOG_HANDLER.set_log_format(
    '%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')


class PoolController(udi_interface.Node):

    def __init__(self, polyglot, primary, address, name):
        """
        Optional.
        Super runs all the parent class necessities. You do NOT have
        to override the __init__ method, but if you do, you MUST call super.

        In most cases, you will want to do this for the controller node.
        """
        super(PoolController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = 'Template Controller'  # override what was passed in
        self.hb = 0

        # Create data storage classes to hold specific data that we need
        # to interact with.
        self.Parameters = Custom(polyglot, 'customparams')
        self.Notices = Custom(polyglot, 'notices')
        self.TypedData = Custom(polyglot, 'customtypeddata')

        # Subscribe to various events from the Interface class.  This is
        # how you will get information from Polyglog.  See the API
        # documentation for the full list of events you can subscribe to.
        #
        # The START event is unique in that you can subscribe to
        # the start event for each node you define.

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.LOGLEVEL, self.handleLevelChange)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)
        self.poly.subscribe(self.poly.CUSTOMTYPEDPARAMS,
                            self.typedParameterHandler)
        self.poly.subscribe(self.poly.CUSTOMTYPEDDATA, self.typedDataHandler)
        self.poly.subscribe(self.poly.POLL, self.poll)

        # Tell the interface we have subscribed to all the events we need.
        # Once we call ready(), the interface will start publishing data.
        self.poly.ready()

        # Tell the interface we exist.
        self.poly.addNode(self)

    def start(self):
        """
        The Polyglot v3 Interface will publish an event to let you know you
        can start your integration. (see the START event subscribed to above)

        This is where you do your initialization / device setup.
        Polyglot v3 Interface startup done.

        Here is where you start your integration. I.E. if you need to 
        initiate communication with a device, do so here.
        """

        # Send the profile files to the ISY if neccessary. The profile version
        # number will be checked and compared. If it has changed since the last
        # start, the new files will be sent.
        self.poly.updateProfile()

        # Send the default custom parameters documentation file to Polyglot
        # for display in the dashboard.
        self.poly.setCustomParamsDoc()

        # Initializing a heartbeat is an example of something you'd want
        # to do during start.  Note that it is not required to have a
        # heartbeat in your node server
        self.heartbeat(0)

        # Device discovery. Here you may query for your device(s) and
        # their capabilities.  Also where you can create nodes that
        # represent the found device(s)
        self.discover()

        # Here you may want to send updated values to the ISY rather
        # than wait for a poll interval.  The user will get more
        # immediate feedback that the node server is running

    """
    Called via the CUSTOMPARAMS event. When the user enters or
    updates Custom Parameters via the dashboard. The full list of
    parameters will be sent to your node server via this event.

    Here we're loading them into our local storage so that we may
    use them as needed.

    New or changed parameters are marked so that you may trigger
    other actions when the user changes or adds a parameter.

    NOTE: Be careful to not change parameters here. Changing
    parameters will result in a new event, causing an infinite loop.
    """

    def parameterHandler(self, params):
        self.Parameters.load(params)
        LOGGER.debug('Loading parameters now')
        self.check_params()

    """
    Called via the CUSTOMTYPEDPARAMS event. This event is sent When
    the Custom Typed Parameters are created.  See the check_params()
    below.  Generally, this event can be ignored.

    Here we're re-load the parameters into our local storage.
    The local storage should be considered read-only while processing
    them here as changing them will cause the event to be sent again,
    creating an infinite loop.
    """

    def typedDataHandler(self, params):
        self.TypedData.load(params)
        LOGGER.debug('Loading typed data now')
        LOGGER.debug(params)

    """
    Called via the LOGLEVEL event.
    """

    def handleLevelChange(self, level):
        LOGGER.info('New log level: {}'.format(level))

    """
    Called via the POLL event.  The POLL event is triggerd at
    the intervals specified in the node server configuration. There
    are two separate poll events, a long poll and a short poll. Which
    one is indicated by the flag.  flag will hold the poll type either
    'longPoll' or 'shortPoll'.

    Use this if you want your node server to do something at fixed
    intervals.
    """

    def poll(self, flag):
        if 'longPoll' in flag:
            LOGGER.debug('longPoll (controller)')
            self.heartbeat()
        else:
            LOGGER.debug('shortPoll (controller)')

    def query(self, command=None):
        """
        Optional.

        The query method will be called when the ISY attempts to query the
        status of the node directly.  You can do one of two things here.
        You can send the values currently held by Polyglot back to the
        ISY by calling reportDriver() or you can actually query the 
        device represented by the node and report back the current 
        status.
        """
        nodes = self.poly.getNodes()
        for node in nodes:
            nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        """
        Example
        Do discovery here. Does not have to be called discovery. Called from
        example controller start method and from DISCOVER command recieved
        from ISY as an exmaple.
        """
        self.poly.addNode(BodyNode(self.poly, self.address,
                          'templateaddr', 'Template Node Name'))

    def delete(self):
        """
        Example
        This is call3ed by Polyglot upon deletion of the NodeServer. If the
        process is co-resident and controlled by Polyglot, it will be
        terminiated within 5 seconds of receiving this message.
        """
        LOGGER.info(
            'Oh God I\'m being deleted. Nooooooooooooooooooooooooooooooooooooooooo.')

    def stop(self):
        """
        This is called by Polyglot when the node server is stopped.  You have
        the opportunity here to cleanly disconnect from your device or do
        other shutdown type tasks.
        """
        LOGGER.debug('NodeServer stopped.')

    """
    This is an example of implementing a heartbeat function.  It uses the
    long poll intervale to alternately send a ON and OFF command back to
    the ISY.  Programs on the ISY can then monitor this and take action
    when the heartbeat fails to update.
    """

    def heartbeat(self, init=False):
        LOGGER.debug('heartbeat: init={}'.format(init))
        if init is not False:
            self.hb = init
        LOGGER.debug('heartbeat: hb={}'.format(self.hb))
        if self.hb == 0:
            self.reportCmd("DON", 2)
            self.hb = 1
        else:
            self.reportCmd("DOF", 2)
            self.hb = 0

    def set_module_logs(self, level):
        logging.getLogger('urllib3').setLevel(level)

    def check_params(self):
        """
        This is an example if using custom Params for user and password and an example with a Dictionary
        """
        self.Notices.clear()
        self.Notices['hello'] = 'Hey there, my IP is {}'.format(
            self.poly.network_interface['addr'])
        self.Notices['hello2'] = 'Hello Friends!'
        default_user = "YourUserName"
        default_password = "YourPassword"

        self.user = self.Parameters.user
        if self.user is None:
            self.user = default_user
            LOGGER.error(
                'check_params: user not defined in customParams, please add it.  Using {}'.format(default_user))
            self.user = default_user

        self.password = self.Parameters.password
        if self.password is None:
            self.password = default_password
            LOGGER.error('check_params: password not defined in customParams, please add it.  Using {}'.format(
                default_password))
            self.password = default_password

        # Add a notice if they need to change the user/password from the default.
        if self.user == default_user or self.password == default_password:
            self.Notices['auth'] = 'Please set proper user and password in configuration page'
            self.Notices['test'] = 'This is only a test'

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
        {'driver': 'ST', 'value': 1, 'uom': 2},
    ]
