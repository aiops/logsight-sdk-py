
How To Make Quality Gates in CI/CD with GitHub
    + https://cerberus-testing.medium.com/how-to-make-quality-gates-in-ci-cd-with-github-a373d8a443b8


Logsight Command Line Interface
-------------------------------

The Logsight Command Line Interface (CLI) is a unified tool to manage your logs.
With this tool, you can manage your logs, applications, tags and execute operations such as log verification.

Commands available include:

+ Applications
    + Create and delete applications
+ Users
    + Register, activate and delete users (not yet available)
    + Change and reset password (not yet available)
+ Analytics
    + Compare logs
    + Detect incidents in logs


INSTALLATION
============
The CLI can can installed using pip from PyPI.
It has been tested with Mac and Linux operating systems.

PREREQUISITE
============
You have a Logsight account with `EMAIL` and `PASSWORD`.


CONFIGURING THE LOGSIGHT COMMAND LINE INTERFACE
================================================
There are several methods you can use to configure the settings that the Logsight CLI uses when interacting with Logsight.ai service,
i.e. Logsight URL and account API keys. Account API keys can be created in API.

There is a specific load order for what will be used.

USING LOGSIGHT CONFIG
*********************
You can create a `.logsight` config file to set up your configuration with Logsight server.
The file should be placed in your home directory.

.. code-block:: console

    $ cat ~/.logsight
    [DEFAULT]
    EMAIL = john.miller@zmail.com
    PASSWORD = sawhUz-hanpe4-zaqtyr
    APP_ID = 07402355-e74e-4115-b21d-4cbf453490d1

Setting the variable APP_ID is optional.
It can be set if you frequently use the same application and want to avoid passing the Id as a parameter for each command invoked.


USING ENVIRONMENT VARIABLES
***************************
You can also set the variables using your environment, `LOGSIGHT_EMAIL`, `LOGSIGHT_PASSWORD` and `LOGSIGHT_APP_ID`.
Environment variables take precedence over config variables.

.. code-block:: console

    $ export LOGSIGHT_EMAIL=john.miller@zmail.com
    $ export LOGSIGHT_PASSWORD=sawhUz-hanpe4-zaqtyr
    $ export LOGSIGHT_APP_ID=07402355-e74e-4115-b21d-4cbf453490d1


PASSING OPTIONS
********************
If you choose not to use the logsight config file or set environment variables,
you can pass the same values as options as part of any logsight command.

.. code-block:: console

    $ python -m cli.ls-cli --email john.miller@zmail.com --password sawhUz-hanpe4-zaqtyr applications ls
    +--------------------------------------+------------------+
    |            APPLICATION Id            |       NAME       |
    +--------------------------------------+------------------+
    | 84c2ca94-e39c-498f-ad0d-0263434c71ac |    hdfs_node     |
    | 8b6cd73b-299b-4f2b-8334-3b820434a23a |   node_manager   |
    | 208d3b6d-15b7-402d-b53a-4c32c2eff623 | resource_manager |
    | 7a858f4f-33f7-4bba-ac5e-bd5fec0bd9a2 |    name_node     |
    +--------------------------------------+------------------+


EXAMPLES OF COMMAND
********************
The following list provides examples of useful commands:

.. code-block:: console

    $ python -m cli.ls-cli application ls
    $ python -m cli.ls-cli application create --name apache_srv
    $ python -m cli.ls-cli application delete --app_id <applicationId>

    $ python -m cli.ls-cli log upload <file> --tag v1 --app_id <applicationId>
    $ python -m cli.ls-cli log tag ls --app_id <applicationId>
       $ python -m cli.ls-cli log status --flush_id --app_id <applicationId>

    $ python -m cli.ls-cli compare log --app_id <applicationId> --tags <tag_v1> <tag_v2> --flush_id <flushId>
    $ python -m cli.ls-cli incident log --app_id <applicationId> --tags <tag_v1>
       $ python -m cli.ls-cli quality log --app_id <applicationId> --tags <tag_v1>


EXAMPLES OF SCENARIO
********************

    $ python -m cli.ls-cli application create --name apache_srv2
    $ # copy the <app_id> returned to next command
    $ export LOGSIGHT_APP_ID=<app_id>
    $ python -m cli.ls-cli log upload hadoop_name_node_v1 --tag v1
    $ python -m cli.ls-cli log upload hadoop_name_node_v1 --tag v2
    $ # copy <flush_id> returned to next command
    $ python -m cli.ls-cli compare log --tags v1 v2 --flush_id <flush_id>



COMMAND REFERENCE
********************

To read more about all the supported commands, please read our Logsight command documentation.