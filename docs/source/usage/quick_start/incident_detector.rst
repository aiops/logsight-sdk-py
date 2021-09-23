
Prerequisites
*************
+ logsight.ai_ subscription (create one for free to get your private key)
+ Once you have your subscription, create an application_ resource in the portal
+ You will need the `private key`_ to connect your application to the Incident Detector API
+ You'll paste your private key into the code below later

.. _logsight.ai: https://logsight.ai/
.. _application: https://demo.logsight.ai/pages/integration
.. _private key: https://demo.logsight.ai/pages/integration


Setting up
**********

Create a directory
==================

Create a directory to store your quick guide exercise:

.. code-block:: console

    $ mkdir quick_guide
    $ cd quick_guide

You can start with an empty Python file:

.. code-block:: console

    $ touch quick_guide.py

Alternatively, you can download the Python file directly from git:

.. code-block:: console

    $ wget full_url_to_raw_file_on_github


Create an environment variable
==============================

Using the private key from your subscription, create one environment variables for authentication:

+ PRIVATE_KEY - The private key for authenticating your requests.

Copy the following text to your bash file:

.. code-block:: console

    $ export PRIVATE_KEY=<replace-with-your-anomaly-detector-key>


After you add the environment variable, run source ~/.bashrc from your console window to make the changes effective.


Install the client library
==========================

Install the Incident Detector client library for python with pip:

.. code-block:: console

    $ pip install logsight_sdk

or directly from the sources:

.. code-block:: console

    $ git clone https://github.com/logsight/python-logsight-sdk.git
    $ cd sdk-python
    $ python setup.py install


Code examples
*************

Code snippets show you how to do the following with the Incident Detector client library for Python:

+ Authenticate the client
+ Load log data from a file
+ Detect incident in the entire data set
+ Detect the anomaly status of the latest data point (???)
+ Detect the change points in the data set (???)


Load packages
=============

Load the various packages used in this quick guide.

.. code:: python

    import sys
    import os
    import time
    import logging

    from logsight.exceptions import LogsightException
    from logsight.applications import LogsightApplication
    from logsight.logger import LogsightLogger
    from logsight.result import LogsightResult
    from logsight.utils import now, create_apps, delete_apps


Authenticate the client
=======================

To enable client authentication, access the PRIVATE_KEY environment variable (or enter the string directly as a value) and indicate your e-mail.

.. code:: python

    PRIVATE_KEY = os.getenv('PRIVATE_KEY') or 'xteitdidb0xd32thtt35ccruy'
    EMAIL = 'jorge.cardoso.pt@gmail.com'


Create application
==================

Indicate the name of the application to which you will send log data.
For example, apache_server, kafka, website or backend.
Create your new application in your subscription (an exception is raised in case it already exists)

.. code:: python

    APP_NAME = 'quick_start_app'

    app_mng = LogsightApplication(PRIVATE_KEY, EMAIL)
    try:
        app_mng.create(APP_NAME)
    except LogsightException as e:
        print(e)


Attached your logger
====================

Adding logsight.ai logging handler in your logging system:

.. code:: python

    handler = LogsightLogger(PRIVATE_KEY, EMAIL, APP_NAME)
    handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)



Load log data from a file
=========================

.. code:: python

    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), './OpenStack_2k.log')
    log_records = []
    try:
        f = open(filename, 'r')

        level_idx, msg_idx = 4, 5
        for i, line in enumerate(f.readlines()):
            tokens = line.split()
            log_records.append((tokens[level_idx], ' '.join(tokens[msg_idx:])))

    except OSError:
        sys.exit("Could not open/read file: %s" % filename)



Send log records
================

.. code:: python

    dt_start = now()
    print('Starting message sending', dt_start)

    for i, m in enumerate(log_records):
        level, message = m[0].upper(), m[1]
        print(i, level, message)

        mapping = {'INFO': logger.info, 'WARNING': logger.warning, 'ERROR': logger.error, 'DEBUG': logger.debug, 'CRITICAL': logger.critical}

        if level in mapping:
            mapping[level](message)
        else:
            sys.exit('Error parsing level for log message number %d: %s %s' % (i, level, message))

    dt_end = now()
    print('Ended message sending', dt_end)


Detect the anomaly status of the latest data point
==================================================

.. code:: python

    time.sleep(60)
    delete_apps(PRIVATE_KEY, EMAIL, [APP_NAME])

    incidents = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME)\
        .get_results(dt_start, dt_end, 'incidents')
    real_incidents = sum([1 if i.total_score > 0 else 0 for i in incidents])


Show incident
=============

.. code:: python

    for i in incidents:
        print('Incident', i)


Run the application
*******************

Run the application with python run command from your quickguide directory.

.. code-block:: console

    $ python quick_guide.py


Clean up resources
*******************

Deleting the resource group also deletes any other resources associated with the resource group.

Remove handler
==============

If need to remove the handler to force any log record in the buffer to be flushed to logsight.ai.

.. code:: python

    handler.close()
    logger.removeHandler(handler)


If you want to clean up, you can remove the application from your subscription.

Delete your application
=======================

.. code:: python

    time.sleep(60)
    delete_apps(PRIVATE_KEY, EMAIL, [APP_NAME])
