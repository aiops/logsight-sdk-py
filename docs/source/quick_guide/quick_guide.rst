
Quickstart
**********

*09/06/2022, 30 minutes to complete*

Get started with the Logsight SDK for Python and client library to verify deployments.
Follow these steps to install the package and start using the algorithms provided by logsight.ai service.
The verification library enables you to evaluate the risk of a deployment of a new version of an application
by automatically using deep learning models trained on millions lines of code, regardless of the underlying IT system, failure scenario, or data volume.

Use the Logsight SDK for Python to:

+ Send data logs to your logsight.ai account
+ Verify deployments using application data logs
+ Retrieve and display the verification risk of your new deployment


Prerequisites
*************
+ logsight.ai_ subscription (create one for free)
+ You will need the `login` and `password` to paste into the code below, later

.. _logsight.ai: https://logsight.ai/



Setting up
**********

Create a directory
==================

Create a directory to store your exercise:

.. code-block:: console

    $ mkdir quick_guide
    $ cd quick_guide


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

    $ touch quick_guide.py

Alternatively, you can download the Python file directly from git:

.. code-block:: console

    $ curl https://raw.githubusercontent.com/aiops/logsight-sdk-py/main/docs/source/quick_guide/quick_guide.py --output quick_guide.py


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

Using the password from your subscription, create one environment variables for authentication:

+ LOGSIGHT_PASSWORD - Password for authenticating your requests
+ LOGSIGHT_EMAIL - Email associated with your subscription

Copy the following text to your bash file:

.. code-block:: console

    $ export LOGSIGHT_PASSWORD=<replace-with-your-password>
    $ export LOGSIGHT_EMAIL=<replace-with-your-email>

After you add the environment variables, you may want to add them to ~/.bashrc.


For the impatient
=================

.. code-block:: console

    mkdir quick_guide
    cd quick_guide
    python3 -m venv venv
    source venv/bin/activate
    curl https://raw.githubusercontent.com/aiops/logsight-sdk-py/main/docs/source/quick_guide/quick_guide.py --output quick_guide.py
    pip install logsight-sdk-py
    unset LOGSIGHT_PASSWORD LOGSIGHT_EMAIL
    export LOGSIGHT_PASSWORD=mowfU5-fyfden-fefzib
    export LOGSIGHT_EMAIL=logsight.testing.001@gmail.com
    python quick_guide.py


Code example
************

The following code snippets show what can be achieved with the Logsight SDK client library for Python:

+ Authenticate the client
+ Set tags
+ Attach the logger
+ Log logging statements
+ Verify the new deployment
+ Show the results of the verification


Load packages
=============

Load the various packages used in this guide.

.. code:: python

    import sys
    import time
    import logging

    from logsight.config import set_host
    from logsight.exceptions import InternalServerError
    from logsight.authentication import LogsightAuthentication
    from logsight.logger.logger import LogsightLogger
    from logsight.compare import LogsightCompare


Authenticate the client
=======================

To enable client authentication, set your LOGSIGHT_PASSWORD and LOGSIGHT_EMAIL.
If you use an on-prem deployment, setup the endpoint of your logsight system using function `set_host`.

.. code:: python

    EMAIL = os.getenv('LOGSIGHT_EMAIL') or 'logsight.testing.001@gmail.com'
    PASSWORD = os.getenv('LOGSIGHT_PASSWORD') or 'mowfU5-fyfden-fefzib'
    set_host("https://demo.logsight.ai/api/v1/")

    auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)



Attach the logger
=================

Add logsight.ai logging handler to your logging system:

.. code:: python

    handler = LogsightLogger(auth.token)
    handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


Set tags
========

You can set tags using a dictionary

.. code:: python

    tags = {'service': 'redis', 'version': 'v1'}

or by using environment variables. To set tags as environment variables you need to use the prefix ``LOGSIGHT_TAG``.

.. code-block:: console

    $ export LOGSIGHT_TAG_SERVICE=redis

.. code:: python

    from config import get_tags_from_env

    env_tags = get_tags_from_env()  # {"service": "redis"}
    handler.set_tags(tags=env_tags)

Execute Redis Version v1.1.1
============================

We assume you are a core developer of Redis in-memory data structure store.

+ Run v1.1.1 of your Redis application
+ Logs are tagged with: service=redis and version=v1.1.1
+ Logs generated are transparently sent to logsight.ai

.. code:: python

    print('Redis running (v1.1.1)')
    tags_1 = {'service': 'redis', 'version': 'v1.1.1'}
    handler.set_tags(tags=tags_1)
    for i in range(10):
        logger.info(f'Connecting to database (instance ID: {i % 4})')
        logger.info(f'Reading {i * 100} KBytes')
        logger.info(f'Closing connection (instance ID: {i % 4})')
    handler.flush()

Your Redis deployment runs for several months without any problems.
It is deemed reliable.


Execute Redis version v2.1.1
============================

You implement a few new features for Redis.
Your new version is v2.1.1.

+ Now, you run v2.1.1 of your Redis application in pre-production
+ Logs are tagged with: service=redis and version=v2.1.1
+ Logs generated are transparently sent to logsight.ai

.. code:: python

    print('Redis running (v2.1.1)')
    tags_2 = {'service': 'redis', 'version': 'v2.1.1'}
    handler.set_tags(tags=tags_2)
    for i in range(15):
        logger.info(f'Connecting to database (instance ID: {i % 4})')
        logger.info(f'Unable to read {i * 100} KBytes')
        logger.error(f'Underlying storage is corrupted')
        logger.info(f'Closing connection (instance ID: {i % 4})')
    handler.flush()


Verify New Release of Redis
===========================

+ You call the Compare function of Logsight to verify the new deployment

.. code:: python

    print('Calculate new deployment risk')
    comp = LogsightCompare(auth.token)
    result = {}
    retry = 5
    while retry:
        try:
            result = comp.compare(baseline_tags=tags_1, candidate_tags=tags_2)
            break
        except InternalServerError as e:
            print(f'Trying in 5s (#{retry})')
            time.sleep(5)
            retry -= 1



Show verification results
=========================

Display the deployment risk and access the webpage with the verification results

.. code:: python

    print(f'Deployment risk: {result["risk"]}')
    print(f'Report webpage: {result["link"]}')

You can copy the url to your browser to see the results of the evaluation.

Run the application
*******************

Run the Python code from your quick_guide directory.

.. code-block:: console

    $ python quick_guide.py
