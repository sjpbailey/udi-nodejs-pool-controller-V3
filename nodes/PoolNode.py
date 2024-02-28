
import udi_interface
import sys
import time
import requests
import urllib3

LOGGER = udi_interface.LOGGER


class PoolNode(udi_interface.Node):
    """
    This is the class that all the Nodes will be represented by. You will
    add this to Polyglot/ISY with the interface.addNode method.

    Class Variables:
    self.primary: String address of the parent node.
    self.address: String address of this Node 14 character limit.
                  (ISY limitation)
    self.added: Boolean Confirmed added to ISY

    Class Methods:
    setDriver('ST', 1, report = True, force = False):
        This sets the driver 'ST' to 1. If report is False we do not report
        it to Polyglot/ISY. If force is True, we send a report even if the
        value hasn't changed.
    reportDriver(driver, force): report the driver value to Polyglot/ISY if
        it has changed.  if force is true, send regardless.
    reportDrivers(): Forces a full update of all drivers to Polyglot/ISY.
    query(): Called when ISY sends a query request to Polyglot for this
        specific node
    """

    # self, polyglot, primary, address, name, id, isOn, allDataJson):
    def __init__(self, polyglot, primary, address, name):
        """
        Optional.
        Super runs all the parent class necessities. You do NOT have
        to override the __init__ method, but if you do, you MUST call super.

        :param polyglot: Reference to the Interface class
        :param primary: Parent address
        :param address: This nodes address
        :param name: This nodes name
        """
        super(PoolNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.id = id
        self.name = name
        self.isOn = isOn
        self.allDataJson = allDataJson

    def start(self):

        LOGGER.debug('%s: get ST=%s', self.lpfx, self.getDriver('ST'))
        self.setDriver('ST', 1)
        LOGGER.debug('%s: get ST=%s', self.lpfx, self.getDriver('ST'))
        self.setDriver('ST', 0)
        LOGGER.debug('%s: get ST=%s', self.lpfx, self.getDriver('ST'))
        self.setDriver('ST', 1)
        LOGGER.debug('%s: get ST=%s', self.lpfx, self.getDriver('ST'))
        self.setDriver('ST', 0)
        LOGGER.debug('%s: get ST=%s', self.lpfx, self.getDriver('ST'))
        self.http = urllib3.PoolManager()

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

        self.setDriver('ST', 1)

    def cmd_off(self, command):

        self.setDriver('ST', 0)

    def cmd_ping(self, command):

        LOGGER.debug("cmd_ping:")
        r = self.http.request('GET', "google.com")
        LOGGER.debug("cmd_ping: r={}".format(r))

    def query(self, command=None):

        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2, 'name': "Online"},
        {'driver': 'GV1', 'value': 0, 'uom': 2, 'name': "OnOff"}
    ]

    id = 'poolnode'

    commands = {
        'DON': cmd_on,
        'DOF': cmd_off,
        'QUERY': query
    }
