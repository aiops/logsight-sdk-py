
Quickstart
**********

*27/09/2021, 30 minutes to complete*

Get started with the Logsight SDK for Python and client library to detect incidents.
Follow these steps to install the package and start using the algorithms provided by logsight.ai service.
The incident detector client library enables you to find incidents in your logs
by automatically using deep learning models trained on millions lines of code, regardless of the underlying IT system, failure scenario, or data volume.

Use the Logsight SDK for Python to:

+ Send data logs to your logsight.ai account
+ Detect incidents in your data logs
+ Retrieve and display the log records associated with an incident


Prerequisites
*************
+ logsight.ai_ subscription (create one for free to get your private key)
+ Once you have your subscription, create an application_ named detecting_incidents_app in the integration tab
+ You will need the `private key`_ to connect your application to the Incident Detector API
+ You'll paste your private key into the code below later

.. _logsight.ai: https://logsight.ai/
.. _application: https://demo.logsight.ai/pages/integration
.. _private key: https://demo.logsight.ai/pages/integration


Setting up
**********

Create a directory
==================

Create a directory to store your exercise:

.. code-block:: console

    $ mkdir detecting_incidents
    $ cd detecting_incidents


Create a virtual env
====================

Create a Python virtual environment to decouple and isolate the packages we will install from you environment.

.. code-block:: console

    $ python3 -m venv venv
    $ source venv/bin/activate


Prepare code file
=================

You can start with an empty Python file:

.. code-block:: console

    $ touch detecting_incidents.py

Alternatively, you can download the Python file directly from git:

.. code-block:: console

    $ curl https://raw.githubusercontent.com/aiops/logsight-sdk-py/main/docs/source/detecting_incidents_app/detecting_incidents_app.py --output detecting_incidents.py


Download a log data file
========================

As a example, we will use a sample log data file from Apache Hadoop platform:

.. code-block:: console

    $ curl https://raw.githubusercontent.com/aiops/logsight-sdk-py/main/docs/source/detecting_incidents_app/Hadoop_2k.log --output Hadoop_2k.log


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


Create environment variables
=============================

Using the private key from your subscription, create one environment variables for authentication:

+ LOGSIGHT_PRIVATE_KEY - The private key for authenticating your requests
+ LOGSIGHT_EMAIL - The email associated with your subscription

Copy the following text to your bash file:

.. code-block:: console

    $ export LOGSIGHT_PRIVATE_KEY=<replace-with-your-anomaly-detector-key>
    $ export LOGSIGHT_EMAIL=<replace-with-your-email>

After you add the environment variable, run source ~/.bashrc from your console window to make the changes effective.


For the impatient
=================

.. code-block:: console

    mkdir detecting_incidents
    cd detecting_incidents
    python3 -m venv venv
    source venv/bin/activate
    curl https://raw.githubusercontent.com/aiops/logsight-sdk-py/main/docs/source/detecting_incidents/detecting_incidents.py --output detecting_incidents_app.py
    curl https://raw.githubusercontent.com/aiops/logsight-sdk-py/main/docs/source/detecting_incidents/Hadoop_2k.log --output Hadoop_2k.log
    pip install logsight-sdk-py
    unset LOGSIGHT_PRIVATE_KEY LOGSIGHT_EMAIL
    export LOGSIGHT_PRIVATE_KEY='mgewxky59zm1euavowtjon9igc'
    export LOGSIGHT_EMAIL='jorge.cardoso.pt@gmail.com'
    python detecting_incidents.py


Code example
************

The following code snippets show what can be achieved with the Logsight SDK client library for Python:

+ Authenticate the client
+ Attach the logger
+ Send log data loaded from a file
+ Detect incident in the entire log data set
+ Show the details of the incident


Load packages
=============

Load the various packages used in this detecting incidents guide.

.. code:: python

    import sys
    import time
    import logging

    from logsight.logger.logger import LogsightLogger
    from logsight.result.result import LogsightResult
    from logsight.utils import now


Authenticate the client
=======================

To enable client authentication, set your PRIVATE_KEY and e-mail.

.. code:: python

    PRIVATE_KEY = os.getenv('LOGSIGHT_PRIVATE_KEY') or 'mgewxky59zm1euavowtjon9igc'
    EMAIL = os.getenv('LOGSIGHT_EMAIL') or 'jorge.cardoso.pt@gmail.com'

Indicate the name of the application to which you will send log data.
For example, apache_server, kafka, website or backend.
This guide sends log data to the application detecting_incidents_app.

.. code:: python

    APP_NAME = 'detecting_incidents_app'


Attach the logger
=================

Add logsight.ai logging handler to your logging system:

.. code:: python

    handler = LogsightLogger(PRIVATE_KEY, EMAIL, APP_NAME)
    handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


Load log data from a file
=========================

+ Open a file with your log data (logs file samples from several systems are available at loghub_)
+ Read all the log records from the file
+ Split log messages and remove the timestamp
+ Store log_records with tuples of the form: (log level, log message)

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
        sys.exit('Could not open/read file')



Send log records
================

+ Store a timestamp indicating when log records started to be sent
+ Iterate over the log records, extract the log level and log message
+ Send the log level and message using the logger and the appropriate log function
+ Once all records have been sent, flush the log handler to force buffered records to be sent
+ Store a timestamp indicating when the last log record was sent

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

+ Wait 60 seconds after sending the last log record to allow logsight.ai AI-driven processing to finish
+ Query logsight.ai for possible incidents

.. code:: python

    sleep_time = 60
    print(f'Sleeping {sleep_time} seconds')
    time.sleep(sleep_time)

    incidents = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME)\
        .get_results(dt_start, dt_end, 'incidents')


Show incidents
==============

Iterate over the list of incidents received and print the incidents' properties

.. code:: python

    for j, i in enumerate(incidents):
        print('Incident:', j + 1, 'Score:', i.total_score, '(', i.timestamp_start, i.timestamp_end, ')')


Run the application
*******************

Run the Python code from your detecting_incidents_app directory.

.. code-block:: console

    $ python detecting_incidents_app.py


Clean up resources
*******************

Delete the application_ `detecting_incidents_app` from your subscription.
