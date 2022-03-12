
How To Make Quality Gates in CI/CD with GitHub
    + https://cerberus-testing.medium.com/how-to-make-quality-gates-in-ci-cd-with-github-a373d8a443b8


Rancher Command Line Interface
------------------------------

The Rancher Command Line Interface (CLI) is a unified tool to manage your Rancher server.
With this tool, you can control your environments, hosts, stacks, services and containers.

These mattermost commands include:

General administration

+ Create teams
+ Create users
+ Assign roles to users
+ Reset user passwords
+ Invite users to teams

Advanced administration

+ Permanently delete users (use cautiously - database backup recommended before use)
+ Permanently delete teams (use cautiously - database backup recommended before use)

Advanced automation

+ Create channels
+ Invite users to channels
+ Remove users from channels
+ List all channels for a team
+ Restore previously deleted channels
+ Modify a channel’s public/private type
+ Migrate sign-in options
+ Reset multi-factor authentication for a user
+ Create sample data


INSTALLATION
============
The binary can be downloaded directly from the UI.
The link can be found in the right hand side of the footer in the UI.
We have binaries for Windows, Mac, and Linux.
You can also check the releases page for our CLI for direct downloads of the binary.

CONFIGURING THE RANCHER COMMAND LINE INTERFACE
================================================
There are several methods you can configure the settings that the Rancher CLI uses when interacting with Rancher,
i.e. Rancher URL and account API keys. Account API keys can be created in API.

There is a specific load order for what will be used.

USING RANCHER CONFIG
********************
You can run rancher config to set up your configuration with Rancher server.

.. code-block:: console

    $ rancher config
    URL []: http://<server_ip>:8080
    Access Key []: <accessKey_of_account_api_key>
    Secret Key []:  <secretKey_of_account_api_key>
    # If there are more than one environment,
    # you will be asked to select which environment to work with
    Environments:
    [1] Default(1a5)
    [2] k8s(1a10)
    Select: 1
    INFO[0017] Saving config to /Users/<username>/.rancher/cli.json



USING ENVIRONMENT VARIABLES
********************
You can set the following environment variables, `RANCHER_URL`, `RANCHER_ACCESS_KEY` and `RANCHER_SECRET_KEY`.

.. code-block:: console

    # Set the url that Rancher is on
    $ export RANCHER_URL=http://<server_ip>:8080
    # Set the access key, i.e. username
    $ export RANCHER_ACCESS_KEY=<accessKey_of_account_api_key>
    # Set the secret key, i.e. password
    $ export RANCHER_SECRET_KEY=<secretKey_of_account_api_key>


PASSING OPTIONS
********************
If you choose not to run rancher config or set environment variables,
you can pass the same values as options as part of any rancher command.

.. code-block:: console

    rancher --url http://server_ip:8080 --access-key <accessKey_of_account_api_key> --secret-key <secretKey_of_account_api_key> --env <environment_id> ps


WORKING WITH ENVIRONMENTS
********************

.. code-block:: console

    If you use an account API key, you will be able to create and update environments.
    If you use an environment API key, you will not be able to create or update other environments and you will only be able to see your existing environment.

    $ rancher env ls
    ID        NAME        STATE     CATALOG                           SYSTEM    DETAIL
    1e1       zookeeper   healthy   catalog://community:zookeeper:1   false
    1e2       Default     healthy                                     false
    1e3       App1        healthy                                     false



LISTING ALL SERVICES
********************
In your selected environment, you can view all the services running in an environment.

.. code-block:: console

    $ rancher ps
    ID   TYPE                 NAME                IMAGE                       STATE     SCALE   ENDPOINTS            DETAIL
    1s1  service              zookeeper/zk        rawmind/alpine-zk:3.4.8-4   healthy   3
    1s2  service              Default/nginxApp    nginx                       healthy   1
    1s4  service              App1/db1            mysql                       healthy   1
    1s5  service              App1/wordpress      wordpress                   healthy   4
    1s6  loadBalancerService  App1/wordpress-lb                               healthy   1       111.222.333.444:80


COMMAND REFERENCE
********************

To read more about all the supported commands, please read our rancher command documentation.