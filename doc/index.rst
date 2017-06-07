.. pyclowder2 documentation master file, created by
   sphinx-quickstart on Wed Jun  7 13:46:46 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyClowder2
======================================

If you are writing Python scripts or extractors against the Clowder API, the `pyClowder2 library <https://opensource.ncsa.illinois.edu/bitbucket/projects/CATS/repos/pyclowder2/browse>`_ provides some of the
API functionality with simplified wrapper functions. After using ``python setup.py install`` to install the library,
you can use it to get and post data to Clowder:
``
import pyclowder.files

pyclowder.files.download(None, "https://clowder.ncsa.illinois.edu/clowder", "r1ek3rs", "UUID")
``

There are several shared arguments among the majority of the pyClowder2 functions:

=============== ========================================================================================================
Argument        Description
=============== ========================================================================================================
connector       Instance of Connector class for communicating with RabbitMQ; used in extractors. If you are calling a function outside an extractor context, this should be None.
host            URL of the Clowder instance you are connecting to.
key             The secret API key of the Clowder instance you are connecting to. If you aren't sure what this is, contact an administrator.
=============== ========================================================================================================

Beyond these, more details for arguments in invidual functions can be found on the pages below.

Modules
--------

.. toctree::
      :maxdepth: 2

      modules
