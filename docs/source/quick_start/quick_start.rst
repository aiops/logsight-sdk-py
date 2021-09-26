
Prerequisites
*************
+ logsight.ai_ subscription (create one for free to get your private key)
+ Once you have your subscription, create an application_ named quick_start_app in the integration tab
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

    $ mkdir quick_start
    $ cd quick_start


Prepare code file
=================

You can start with an empty Python file:

.. code-block:: console

    $ touch quick_start.py

Alternatively, you can download the Python file directly from git:

.. code-block:: console

    $ curl https://raw.githubusercontent.com/aiops/logsight-sdk-py/main/docs/source/quick_start/quick_start.py --output quick_start.py


Download a log data file
========================

As a example, we will use a sample log data file from Apache Hadoop platform:

.. code-block:: console

    $ curl https://raw.githubusercontent.com/aiops/logsight-sdk-py/main/docs/source/quick_start/Hadoop_2k.log --output Hadoop_2k.log


Install the client library
==========================

Install the Incident Detector client library for python with pip:

.. code-block:: console

    $ pip install logsight-sdk-py

or directly from the sources:

.. code-block:: console

    $ git clone https://github.com/aiops/logsight-sdk-py.git
    $ cd logsight-sdk-py
    $ python setup.py install


Code examples
*************

Code snippets show you how to do the following with the Incident Detector client library for Python:

+ Authenticate the client
+ Attach you logger
+ Send log data loaded from a file
+ Detect incident in the entire log data set
+ Show the details of the incident


Load packages
=============

Load the various packages used in this quick start guide.

.. code:: python

    import sys
    import os
    import time
    import logging

    from logsight.logger import LogsightLogger
    from logsight.result import LogsightResult
    from logsight.utils import now


Authenticate the client
=======================

To enable client authentication, access the PRIVATE_KEY environment variable (or enter the string directly as a value) and indicate your e-mail.

.. code:: python

    PRIVATE_KEY = 'xteitdidb0xd32thtt35ccruy'
    EMAIL = 'jorge.cardoso.pt@gmail.com'

Indicate the name of the application to which you will send log data.
For example, apache_server, kafka, website or backend.
This quick guide sends log data to the application quick_start_app.

.. code:: python

    APP_NAME = 'quick_start_app'


Attached the logger
===================

Adding logsight.ai logging handler in your logging system:

.. code:: python

    handler = LogsightLogger(PRIVATE_KEY, EMAIL, APP_NAME)
    handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)



Load log data from a file
=========================

+ open file with your logs (many logs are available at loghub_)
+ read all the log records from the file
+ split log messages and remove the timestamp
+ the list log_records contains tuples of the form (log level, log message)

.. _loghub: https://github.com/logpai/loghub


.. code:: python

    log_records = []
    try:
        f = open('Hadoop_2k.log', 'r')

        for i, line in enumerate(f.readlines()):
            tokens = line.split()
            level_idx, msg_idx = 2, 3
            log_records.append((tokens[level_idx], ' '.join(tokens[msg_idx:])))

    except OSError:
        sys.exit("Could not open/read file")



Send log records
================

+ store a timestamp indicating when log records started to be sent
+ iterate over the log records, extract the log level and log message
+ send the log level and message using the logger and the appropriate log function
+ once all records have been sent, flush the log handler to force buffered records to be sent
+ store a timestamp indicating when the last log records were sent

.. code:: python

    dt_start = now()
    print('Starting log records sending', dt_start)

    mapping = {'INFO': logger.info, 'WARNING': logger.warning, 'WARN': logger.warning,
               'ERROR': logger.error, 'DEBUG': logger.debug, 'CRITICAL': logger.critical,
               'FATAL': logger.critical}

    for i, m in enumerate(log_records):
        level, message = m[0].upper(), m[1]
        print(i, level, message)

        if level in mapping:
            mapping[level](message)
        else:
            sys.exit('Unknown log level. Log record number %d: %s %s' % (i, level, message))

    handler.flush()

    dt_end = now()
    print('Ended log records sending', dt_end)


Detect the anomaly status of the latest data point
==================================================

+ wait 60 seconds after sending the log records to allow logsight.ai to process the log records
+ query logsight.ai for incidents within the time window when log records were sent

.. code:: python

    sleep_time = 60
    print(f'Sleeping {sleep_time} seconds')
    time.sleep(sleep_time)

    incidents = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME)\
        .get_results(dt_start, dt_end, 'incidents')



Show incidents
==============

+ iterate over the list of incidents received and print the incidents' properties

.. code:: python

    for j, i in enumerate(incidents):
        print('Incident:', j + 1, 'Score:', i.total_score, '(', i.timestamp_start, i.timestamp_end, ')')


Run the application
*******************

Run the Python code from your quick_start directory.

.. code-block:: console

    $ python quick_start.py


Clean up resources
*******************

+ delete the application_ quick_start_app from your subscription.
