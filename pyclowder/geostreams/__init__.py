# -*- coding: utf-8 -*-

"""Client library to interact with Geostreaming API in Clowder.

 This module provides methods to simplify writing client code
 against the Geostreaming Clowder API.

"""

# Set default logging handler to avoid "No handler found" warnings.
# See http://docs.python-guide.org/en/latest/writing/logging/
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
