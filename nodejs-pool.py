#!/usr/bin/env python

from nodes import PoolController

import udi_interface
import sys

LOGGER = udi_interface.LOGGER

if __name__ == "__main__":
    try:

        polyglot = udi_interface.Interface([PoolController])
        polyglot.start()
        control = PoolController(
            polyglot, 'controller', 'controller', 'PoolController')
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        LOGGER.warning("Received interrupt or exit...")

        polyglot.stop()
    except Exception as err:
        LOGGER.error('Exception: {0}'.format(err), exc_info=True)
    sys.exit(0)
