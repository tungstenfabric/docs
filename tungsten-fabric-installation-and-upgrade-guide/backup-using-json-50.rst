How to Backup and Restore TF databases in JSON Format
===========================================================

 

This document shows how to backup and restore the Contrail
databases—Cassandra and Zookeeper—in JSON format.

Before You Begin
----------------

The backup and restore procedure must be completed for nodes running the
same Tungsten Fabric Networking release. The procedure is used to backup the
Tungsten Fabric Networking databases only; it does not include instructions for
backing up orchestration system databases.

.. Caution::
   Database backups must be consistent across all systems because the state
   of the TF database is associated with other system databases, such
   as OpenStack databases. Database changes associated with northbound APIs
   must be stopped on all the systems before performing any backup
   operation. For example, you might block the external VIP for northbound
   APIs at the load balancer level, such as HAproxy.

Simple Database Backup in JSON Format
-------------------------------------

This procedure provides a simple database backup in JSON format. This
procedure is performed using the ``db_json_exim.py`` script located in
the ``/usr/lib/python2.7/site-packages/cfgm_common`` on the controller
node.

To perform this database backup:

1.  Log into one of the config nodes. Create the ``/tmp/db-dump``
    directory on any of the config node hosts.

    ::

       mkdir /tmp/db-dump

2.  On the same config node, copy the ``contrail-api.conf`` file from
    the container to the host.

    *Ansible Deployer*:

    ::

       docker cp config_api_1:/etc/contrail/contrail-api.conf /tmp/db-dump/

    *Red Hat Openstack Deployer*:

    ::

       docker cp contrail_config_api:/etc/contrail/contrail-api.conf /tmp/db-dump/

    The Cassandra database instance on any configuration node includes
    the complete Cassandra database for all configuration nodes in the
    cluster. Steps 1 and 2, therefore, only need to be performed on one
    configuration node.

3.  Stop the following docker configuration services on all of the
    TF configuration nodes.

    *Ansible Deployer*:

    ::

       docker stop config_svcmonitor_1
       docker stop config_devicemgr_1
       docker stop config_schema_1
       docker stop config_api_1

    *Red Hat Openstack Deployer*:

    ::

       docker stop contrail_config_svc_monitor
       docker stop contrail_config_device_manager
       docker stop contrail_config_schema
       docker stop contrail_config_api

    This step must be performed on each individual config node in the
    cluster.

4.  Return to the config node where you performed steps 1 and 2.

    List the docker image to find the name or ID of the *config api*
    image.

    ``docker image ls | grep config-api``

    Example:

    ::

       docker image ls | grep config-api
       hub.juniper.net/contrail/contrail-controller-config-api 1909.30-ocata c9d757252a0c  4 months ago  583MB

5.  From the same config node, start the *config api* container pointing
    the ``entrypoint.sh`` script to ``/bin/bash`` and mapping
    ``/tmp/db-dump`` from the host to the ``/tmp`` directory inside the
    container. You perform this step to ensure that the API services are
    not started on the config node.

    Enter the *-v /etc/contrail/ssl:/etc/contrail/ssl:ro* command option
    when cassandra_use_ssl is used as api-server configuration parameter
    to ensure TLS certificates are mounted to the TF SSL
    directory. This mounting ensures that the backup procedure succeeds
    in environments with endpoints that require TLS authentication.

    The *registry_name* and *container_tag* variables must match step 4.

    ::

       docker run --rm -it -v /tmp/db-dump/:/tmp/ -v /etc/contrail/ssl:/etc/contrail/ssl:ro --network host --entrypoint=/bin/bash <registry_name>/contrail-controller-config_api:<container_tag>

    *Example*:

    ::

       docker run --rm -it -v /tmp/db-dump/:/tmp/ -v /etc/contrail/ssl:/etc/contrail/ssl:ro --network host --entrypoint=/bin/bash hub.juniper.net/contrail/contrail-controller-config-api:1909.30-ocata

6.  From the docker container created on the config node in Step 5,
    use the ``db_json_exim.py`` script to backup data in JSON format..
    The db dump file will be saved in the ``/tmp/db-dump/`` on this
    config node.

    ::

       cd /usr/lib/python2.7/site-packages/cfgm_common
       python db_json_exim.py --export-to /tmp/db-dump.json --api-conf /tmp/contrail-api.conf

    The Cassandra database instance on any configuration node includes
    the complete Cassandra database for all configuration nodes in the
    cluster. You, therefore, only need to perform step 4 through 6 from
    one of the configuration nodes.

7.  (Optional. Recommended) From the same config node, enter the
    ``cat /tmp/db-dump.json | python -m json.tool | less`` command to
    view a more readable version of the file transfer.

    ::

       cat /tmp/db-dump.json | python -m json.tool | less

8.  From the same config node, exit out of the *config api* container.
    This will stop the container.

    ::

       exit

9.  Start the following configuration services on all of the TF configuration nodes.

    *Ansible Deployer*:

    ::

       docker start config_api_1
       docker start config_schema_1
       docker start config_svcmonitor_1
       docker start config_devicemgr_1

    *Red Hat Openstack Deployer*:

    ::

       docker start contrail_config_api
       docker start contrail_config_schema
       docker start contrail_config_svc_monitor
       docker start contrail_config_device_manager

    This step must be performed on each individual config node.

10. On each config node, enter the contrail-status command to confirm
    that services are in the ``active`` or ``running``
    states. 
    
    .. note:: Some command output and output fields are removed for readability. Output shown is from a node hosting config and analytics services.
   
    ::

       contrail-status
       Pod             Service     Original Name                 State
       analytics       api         contrail-analytics-api        running
       analytics       collector   contrail-analytics-collector  running
       analytics       nodemgr     contrail-nodemgr              running
       analytics       provisioner contrail-provisioner          running
       analytics       redis       contrail-external-redis       running
       analytics-alarm alarm-gen   contrail-analytics-alarm-gen  running
       analytics-alarm kafka       contrail-external-kafka       running
       <some output removed for readability>

       == Contrail control ==
       control: active
       nodemgr: active
       named: active
       dns: active

       == Contrail analytics-alarm ==
       nodemgr: active
       kafka: active
       alarm-gen: active

       == Contrail database ==
       nodemgr: active
       query-engine: active
       cassandra: active

       == Contrail analytics ==
       nodemgr: active
       api: active
       collector: active

       == Contrail config-database ==
       nodemgr: active
       zookeeper: active
       rabbitmq: active
       cassandra: active

       == Contrail webui ==
       web: active
       job: active

       == Contrail analytics-snmp ==
       snmp-collector: active
       nodemgr: active
       topology: active

       == Contrail config ==
       svc-monitor: active
       nodemgr: active
       device-manager: active
       api: active
       schema: active

Examples: Simple Database Backups in JSON Format
------------------------------------------------

These examples illustrate the process for creating a simple database
backup in JSON format in both an Ansible deployer environment and a Red
Hat Openstack deployer environment.

In each example, a cluster with three config nodes—control_config1,
control_config2, and control_config3—is backed up. All tasks that need
to be performed on a single config nodes are performed on
control-config1. The tasks must be performed in the shown order.

*Ansible Deployer Environment*:

::

   ## control_config1 ##
   mkdir /tmp/db-dump
   docker cp config_api_1:/etc/contrail/contrail-api.conf /tmp/db-dump/
   docker stop config_svcmonitor_1
   docker stop config_devicemgr_1
   docker stop config_schema_1
   docker stop config_api_1

   ## control_config2 ##
   docker stop config_svcmonitor_1
   docker stop config_devicemgr_1
   docker stop config_schema_1
   docker stop config_api_1

   ## control_config3 ##
   docker stop config_svcmonitor_1
   docker stop config_devicemgr_1
   docker stop config_schema_1
   docker stop config_api_1

   ## control_config1 ##
   docker run --rm -it -v /tmp/db-dump/:/tmp/ -v /etc/contrail/ssl:/etc/contrail/ssl:ro --network host --entrypoint=/bin/bash hub.juniper.net/contrail/contrail-controller-config-api:1909.30-ocata
   cd /usr/lib/python2.7/site-packages/cfgm_common
   python db_json_exim.py --export-to /tmp/db-dump.json --api-conf /tmp/contrail-api.conf
   cat /tmp/db-dump.json | python -m json.tool | less
   exit
   docker start config_api_1
   docker start config_schema_1
   docker start config_svcmonitor_1
   docker start config_devicemgr_1
   contrail-status

   ## control_config2 ##
   docker start config_api_1
   docker start config_schema_1
   docker start config_svcmonitor_1
   docker start config_devicemgr_1
   contrail-status

   ## control_config3 ##
   docker start config_api_1
   docker start config_schema_1
   docker start config_svcmonitor_1
   docker start config_devicemgr_1
   contrail-status

*Red Hat Openstack Deployer Environment*:

::

   ## control_config1 ##
   mkdir /tmp/db-dump
   docker cp contrail_config_api:/etc/contrail/contrail-api.conf /tmp/db-dump/
   docker stop contrail_config_svc_monitor
   docker stop contrail_config_device_manager
   docker stop contrail_config_schema
   docker stop contrail_config_api

   ## control_config2 ##
   docker stop contrail_config_svc_monitor
   docker stop contrail_config_device_manager
   docker stop contrail_config_schema
   docker stop contrail_config_api

   ## control_config3 ##
   docker stop contrail_config_svc_monitor
   docker stop contrail_config_device_manager
   docker stop contrail_config_schema
   docker stop contrail_config_api

   ## control_config1 ##
   docker run --rm -it -v /tmp/db-dump/:/tmp/ -v /etc/contrail/ssl:/etc/contrail/ssl:ro --network host --entrypoint=/bin/bash hub.juniper.net/contrail/contrail-controller-config-api:1909.30-ocata
   cd /usr/lib/python2.7/site-packages/cfgm_common 
   python db_json_exim.py --export-to /tmp/db-dump.json --api-conf /tmp/contrail-api.conf
   cat /tmp/db-dump.json | python -m json.tool | less
   exit
   docker start contrail_config_api
   docker start contrail_config_schema
   docker start contrail_config_svc_monitor
   docker start contrail_config_device_manager
   contrail-status

   ## control_config2 ##
   docker start contrail_config_api
   docker start contrail_config_schema
   docker start contrail_config_svc_monitor
   docker start contrail_config_device_manager
   contrail-status

   ## control_config3 ##
   docker start contrail_config_api
   docker start contrail_config_schema
   docker start contrail_config_svc_monitor
   docker start contrail_config_device_manager
   contrail-status

Restore Database from the Backup in JSON Format
-----------------------------------------------

This procedure provides the steps to restore a system using the simple
database backup JSON file that was created in `Simple Database Backup in JSON Format`_.

To restore a system from a backup JSON file:

1.  Copy the ``contrail-api.conf`` file from the container to the host
    on any one of the config nodes.

    *Ansible Deployer*:

    ::

       docker cp config_api_1:/etc/contrail/contrail-api.conf /tmp/db-dump/

    *Red Hat Openstack Deployer*:

    ::

       docker cp contrail_config_api:/etc/contrail/contrail-api.conf /tmp/db-dump/

2.  Stop the configuration services on all of the controllers.

    *Ansible Deployer*:

    ::

       docker stop config_svcmonitor_1
       docker stop config_devicemgr_1
       docker stop config_schema_1
       docker stop config_api_1
       docker stop config_nodemgr_1
       docker stop config_database_nodemgr_1
       docker stop analytics_snmp_snmp-collector_1
       docker stop analytics_snmp_topology_1
       docker stop analytics_alarm_alarm-gen_1
       docker stop analytics_api_1
       docker stop analytics_collector_1
       docker stop analytics_alarm_kafka_1

    *Red Hat Openstack Deployer—Node hosting Tungsten Fabric Config
    containers*:

    ::

       docker stop contrail_config_svc_monitor
       docker stop contrail_config_device_manager
       docker stop contrail_config_schema
       docker stop contrail_config_api
       docker stop contrail_config_nodemgr
       docker stop contrail_config_database_nodemgr

    *Red Hat Openstack Deployer—Node hosting Tungsten Fabric Analytics
    containers*:

    ::

       docker stop contrail_analytics_snmp_collector
       docker stop contrail_analytics_topology
       docker stop contrail_analytics_alarmgen
       docker stop contrail_analytics_api
       docker stop contrail_analytics_collector
       docker stop contrail_analytics_kafka

3.  Stop the Cassandra service on all the ``config-db`` controllers.

    *Ansible Deployer*:

    ::

       docker stop config_database_cassandra_1

    *Red Hat Openstack Deployer*:

    ::

       docker stop contrail_config_database

4.  Stop the Zookeeper service on all controllers.

    *Ansible Deployer*:

    ::

       docker stop config_database_zookeeper_1

    *Red Hat Openstack Deployer*:

    ::

       docker stop contrail_config_zookeeper

5.  Backup the Zookeeper data directory on all the controllers.

    *Ansible Deployer*:

    ::

       cd /var/lib/docker/volumes/config_database_config_zookeeper/
       cp -R _data/version-2/ version-2-save

    *Red Hat Openstack Deployer*:

    ::

       cd /var/lib/docker/volumes/config_zookeeper/
       cp -R _data/version-2/ version-2-save

6.  Delete the Zookeeper data directory contents on all the controllers.

    ::

       rm -rf _data/version-2/*

7.  Backup the Cassandra data directory on all the controllers.

    *Ansible Deployer*:

    ::

       cd /var/lib/docker/volumes/config_database_config_cassandra/
       cp -R _data/ Cassandra_data-save

    *Red Hat Openstack Deployer*:

    ::

       cd /var/lib/docker/volumes/config_cassandra/
       cp -R _data/ Cassandra_data-save

8.  Delete the Cassandra data directory contents on all controllers.

    ::

       rm -rf _data/*

9.  Start the Zookeeper service on all the controllers.

    *Ansible Deployer*:

    ::

       docker start config_database_zookeeper_1

    *Red Hat Openstack Deployer*:

    ::

       docker start contrail_config_zookeeper

10. Start the Cassandra service on all the controllers.

    *Ansible Deployer*:

    ::

       docker start config_database_cassandra_1

    *Red Hat Openstack Deployer*:

    ::

       docker start contrail_config_database

11. List docker image to find the name or ID of the ``config-api`` image
    on the config node.

    ::

       docker image ls | grep config-api

    Example:

    ::

       docker image ls | grep config-api
       hub.juniper.net/contrail/contrail-controller-config-api 1909.30-ocata c9d757252a0c  4 months ago  583MB

12. Run a new docker container using the name or ID of the
    ``config_api`` image on the same config node.

    Enter the *-v /etc/contrail/ssl:/etc/contrail/ssl:ro* command option
    when cassandra_use_ssl is used as api-server configuration parameter
    to ensure TLS certificates are mounted to the TF SSL
    directory. This mounting ensures that this backup procedure succeeds
    in environments with endpoints that require TLS authentication.

    Use the *registry_name* and *container_tag* from the output of the
    step 11.

    ::

       docker run --rm -it -v /tmp/db-dump/:/tmp/ -v /etc/contrail/ssl:/etc/contrail/ssl:ro --network host --entrypoint=/bin/bash <registry_name>/contrail-controller-config_api:<container tag>

    Example

    ::

       docker run --rm -it -v /tmp/db-dump/:/tmp/ -v /etc/contrail/ssl:/etc/contrail/ssl:ro --network host --entrypoint=/bin/bash hub.juniper.net/contrail/contrail-controller-config-api:1909.30-ocata

13. Restore the data in new running docker on the same config node.

    ::

       cd /usr/lib/python2.7/site-packages/cfgm_common
       python db_json_exim.py --import-from /tmp/db-dump.json --api-conf /tmp/contrail-api.conf


14. Exit out of the *config api* container. This will stop the
    container.


    ::

       exit

15. Start config services on all the controllers.

    *Ansible Deployer*:

    ::

       docker start config_svcmonitor_1
       docker start config_devicemgr_1
       docker start config_schema_1
       docker start config_api_1
       docker start config_nodemgr_1
       docker start config_database_nodemgr_1
       docker start analytics_snmp_snmp-collector_1
       docker start analytics_snmp_topology_1
       docker start analytics_alarm_alarm-gen_1
       docker start analytics_api_1
       docker start analytics_collector_1
       docker start analytics_alarm_kafka_1

    *Red Hat Openstack Deployer—Node hosting Tungsten Fabric Config
    containers*:

    ::

       docker start contrail_config_svc_monitor
       docker start contrail_config_device_manager
       docker start contrail_config_schema
       docker start contrail_config_api
       docker start contrail_config_nodemgr
       docker start contrail_config_database_nodemgr

    *Red Hat Openstack Deployer—Node hosting Tungsten Fabric Analytics
    containers*:

    ::

       docker start contrail_analytics_snmp_collector
       docker start contrail_analytics_topology
       docker start contrail_analytics_alarmgen
       docker start contrail_analytics_api
       docker start contrail_analytics_collector
       docker start contrail_analytics_kafka

16. Enter the contrail-status command on each configuration node and,
    when applicable, on each analytics node to confirm that services are
    in the ``active`` or ``running`` states.
    
    .. note:: Output shown for a config node. Some command output and output fields are removed for readability.

    ::

       contrail-status
       Pod     Service         Original Name                         State
       config  api             contrail-controller-config-api        running
       config  device-manager  contrail-controller-config-devicemgr  running
       config  dnsmasq         contrail-controller-config-dnsmasq    running
       config  nodemgr         contrail-nodemgr                      running
       config  provisioner     contrail-provisioner                  running
       config  schema          contrail-controller-config-schema     running
       config  stats           contrail-controller-config-stats      running
       <some output removed for readability>

       == Contrail control ==
       control: active
       nodemgr: active
       named: active
       dns: active


       == Contrail database ==
       nodemgr: active
       query-engine: active
       cassandra: active

       == Contrail config-database ==
       nodemgr: active
       zookeeper: active
       rabbitmq: active
       cassandra: active

       == Contrail webui ==
       web: active
       job: active

       == Contrail config ==
       svc-monitor: active
       nodemgr: active
       device-manager: active
       api: active
       schema: active

Example: How to Restore a Database Using the JSON Backup (Ansible Deployer Environment)
---------------------------------------------------------------------------------------

This example shows how to restore the databases for three controllers
connected to the Tungsten Fabric Configuration database (config-db). This
example assumes a JSON backup file of the databases was previously
created using the instructions provided in `Simple Database Backup in
JSON Format`_. The
network was deployed using Ansible and the three controllers—nodec53,
nodec54, and nodec55—have separate IP addresses.

::

   ## Make db-dump directory. Copy contrail-api.conf to db-dump directory. ##
   root@nodec54 ~]# mkdir /tmp/db-dump
   root@nodec54 ~]# docker cp config_api_1:/etc/contrail/contrail-api.conf /tmp/db-dump/

   ## Stop Configuration Services on All Controllers ##
   [root@nodec53 ~]# docker stop config_schema_1
   [root@nodec53 ~]# docker stop config_api_1
   [root@nodec53 ~]# docker stop config_svcmonitor_1 
   [root@nodec53 ~]# docker stop config_devicemgr_1
   [root@nodec53 ~]# docker stop config_nodemgr_1
   [root@nodec53 ~]# docker stop config_database_nodemgr_1
   [root@nodec53 ~]# docker stop analytics_snmp_snmp-collector_1
   [root@nodec53 ~]# docker stop analytics_snmp_topology_1
   [root@nodec53 ~]# docker stop analytics_alarm_alarm-gen_1
   [root@nodec53 ~]# docker stop analytics_api_1
   [root@nodec53 ~]# docker stop analytics_collector_1
   [root@nodec53 ~]# docker stop analytics_alarm_kafka_1

   [root@nodec54 ~]# # docker stop config_schema_1
   [root@nodec54 ~]# docker stop config_api_1
   [root@nodec54 ~]# docker stop config_svcmonitor_1 
   [root@nodec54 ~]# docker stop config_devicemgr_1
   [root@nodec54 ~]# docker stop config_nodemgr_1
   [root@nodec54 ~]# docker stop config_database_nodemgr_1
   [root@nodec54 ~]# docker stop analytics_snmp_snmp-collector_1
   [root@nodec54 ~]# docker stop analytics_snmp_topology_1
   [root@nodec54 ~]# docker stop analytics_alarm_alarm-gen_1
   [root@nodec54 ~]# docker stop analytics_api_1
   [root@nodec54 ~]# docker stop analytics_collector_1
   [root@nodec54 ~]# docker stop analytics_alarm_kafka_1

   [root@nodec55 ~]# docker stop config_schema_1
   [root@nodec55 ~]# docker stop config_api_1
   [root@nodec55 ~]# docker stop config_svcmonitor_1 
   [root@nodec55 ~]# docker stop config_devicemgr_1
   [root@nodec55 ~]# docker stop config_nodemgr_1 
   [root@nodec55 ~]# docker stop config_database_nodemgr_1
   [root@nodec55 ~]# docker stop analytics_snmp_snmp-collector_1
   [root@nodec55 ~]# docker stop analytics_snmp_topology_1
   [root@nodec55 ~]# docker stop analytics_alarm_alarm-gen_1
   [root@nodec55 ~]# docker stop analytics_api_1
   [root@nodec55 ~]# docker stop analytics_collector_1
   [root@nodec55 ~]# docker stop analytics_alarm_kafka_1

   ## Stop Cassandra ##
   [root@nodec53 ~]# docker stop config_database_cassandra_1
   [root@nodec54 ~]# docker stop config_database_cassandra_1
   [root@nodec55 ~]# docker stop config_database_cassandra_1

   ## Stop Zookeeper ##
   [root@nodec53 ~]# docker stop config_database_zookeeper_1
   [root@nodec54 ~]# docker stop config_database_zookeeper_1
   [root@nodec55 ~]# docker stop config_database_zookeeper_1

   ## Backup Zookeeper Directories Before Deleting Zookeeper Data Directory Contents ##
   [root@nodec53 _data]# cd /var/lib/docker/volumes/config_database_config_zookeeper/
   [root@nodec53 config_database_config_zookeeper]# cp -R _data/version-2/ version-2-save
   [root@nodec53 config_database_config_zookeeper]# rm -rf _data/version-2/*

   [root@nodec54 _data]# cd /var/lib/docker/volumes/config_database_config_zookeeper/
   [root@nodec54 config_database_config_zookeeper]# cp -R _data/version-2/ version-2-save
   [root@nodec54 config_database_config_zookeeper]# rm -rf _data/version-2/*

   [root@nodec55 _data]# cd /var/lib/docker/volumes/config_database_config_zookeeper/
   [root@nodec55 config_database_config_zookeeper]# cp -R _data/version-2/ version-2-save
   [root@nodec55 config_database_config_zookeeper]# rm -rf _data/version-2/*

   ## Backup Cassandra Directory Before Deleting Cassandra Data Directory Contents ##
   [root@nodec53 ~]# cd /var/lib/docker/volumes/config_database_config_cassandra/
   [root@nodec53 config_database_config_cassandra]# cp -R _data/ Cassandra_data-save
   [root@nodec53 config_database_config_cassandra]# rm -rf _data/*

   [root@nodec54 ~]# cd /var/lib/docker/volumes/config_database_config_cassandra/
   [root@nodec54 config_database_config_cassandra]# cp -R _data/ Cassandra_data-save
   [root@nodec54 config_database_config_cassandra]# rm -rf _data/*

   [root@nodec55 ~]# cd /var/lib/docker/volumes/config_database_config_cassandra/
   [root@nodec55 config_database_config_cassandra]# cp -R _data/ Cassandra_data-save
   [root@nodec55 config_database_config_cassandra]# rm -rf _data/*

   ## Start Zookeeper ##
   [root@nodec53 ~]# docker start config_database_zookeeper_1
   [root@nodec54 ~]# docker start config_database_zookeeper_1
   [root@nodec55 ~]# docker start config_database_zookeeper_1

   ## Start Cassandra ##
   [root@nodec53 ~]# docker start config_database_cassandra_1
   [root@nodec54 ~]# docker start config_database_cassandra_1
   [root@nodec55 ~]# docker start config_database_cassandra_1

   ## Run Docker Image & Mount TF TLS Certificates to TF SSL Directory ##
   [root@nodec54 ~]# docker image ls | grep config-api
   hub.juniper.net/contrail/contrail-controller-config-api  1909.30-ocata c9d757252a0c  4 months ago  583MB
   [root@nodec54 ~]# docker run --rm -it -v /tmp/db-dump/:/tmp/ -v /etc/contrail/ssl:/etc/contrail/ssl:ro --network host --entrypoint=/bin/bash hub.juniper.net/contrail/contrail-controller-config-api:1909.30-ocata

   ## Restore Data in New Docker Containers ##
   (config_api_1)[root@nodec54 /root]$ cd /usr/lib/python2.7/site-packages/cfgm_common/
   (config_api_1)[root@nodec54 /usr/lib/python2.7/site-packages/cfgm_common]$ python db_json_exim.py --import-from /tmp/db-dump.json --api-conf /tmp/contrail-api.conf

   ## Start Configuration Services ##
   [root@nodec53 ~]# docker start config_schema_1
   [root@nodec53 ~]# docker start config_svcmonitor_1 
   [root@nodec53 ~]# docker start config_devicemgr_1
   [root@nodec53 ~]# docker start config_nodemgr_1
   [root@nodec53 ~]# docker start config_database_nodemgr_1
   [root@nodec53 ~]# docker start config_api_1
   [root@nodec53 ~]# docker start analytics_snmp_snmp-collector_1
   [root@nodec53 ~]# docker start analytics_snmp_topology_1
   [root@nodec53 ~]# docker start analytics_alarm_alarm-gen_1
   [root@nodec53 ~]# docker start analytics_api_1
   [root@nodec53 ~]# docker start analytics_collector_1
   [root@nodec53 ~]# docker start analytics_alarm_kafka_1

   [root@nodec54 ~]# docker start config_schema_1
   [root@nodec54 ~]# docker start config_svcmonitor_1 
   [root@nodec54 ~]# docker start config_devicemgr_1
   [root@nodec54 ~]# docker start config_nodemgr_1
   [root@nodec54 ~]# docker start config_database_nodemgr_1
   [root@nodec54 ~]# docker start config_api_1
   [root@nodec54 ~]# docker start analytics_snmp_snmp-collector_1
   [root@nodec54 ~]# docker start analytics_snmp_topology_1
   [root@nodec54 ~]# docker start analytics_alarm_alarm-gen_1
   [root@nodec54 ~]# docker start analytics_api_1
   [root@nodec54 ~]# docker start analytics_collector_1
   [root@nodec54 ~]# docker start analytics_alarm_kafka_1

   [root@nodec55 ~]# docker start config_schema_1
   [root@nodec55 ~]# docker start config_svcmonitor_1 
   [root@nodec55 ~]# docker start config_devicemgr_1
   [root@nodec55 ~]# docker start config_nodemgr_1
   [root@nodec55 ~]# docker start config_database_nodemgr_1
   [root@nodec55 ~]# docker start config_api_1
   [root@nodec55 ~]# docker start analytics_snmp_snmp-collector_1
   [root@nodec55 ~]# docker start analytics_snmp_topology_1
   [root@nodec55 ~]# docker start analytics_alarm_alarm-gen_1
   [root@nodec55 ~]# docker start analytics_api_1
   [root@nodec55 ~]# docker start analytics_collector_1
   [root@nodec55 ~]# docker start analytics_alarm_kafka_1

   ## Confirm Services are Active ##
   [root@nodec53 ~]# contrail-status
   [root@nodec54 ~]# contrail-status
   [root@nodec55 ~]# contrail-status

Example: How to Restore a Database Using the JSON Backup (Red Hat Openstack Deployer Environment)
-------------------------------------------------------------------------------------------------

This example shows how to restore the databases from an environment that
was deployed using Red Hat Openstack and includes three config
nodes—``config1``, ``config2``, and ``config3``—connected to the
Tungsten Fabric Configuration database (config-db). All steps that need to be
done from a single config node are performed from ``config1``.

The environment also contains three analytics nodes—``analytics1``,
``analytics2``, and ``analytics3``—to provide analytics services.

This example assumes a JSON backup file of the databases was previously
created using the instructions provided in `Simple Database Backup in
JSON Format`_.

::

   ## Make db-dump directory. Copy contrail-api.conf to db-dump directory. ##
   [root@config1 ~]# mkdir /tmp/db-dump
   [root@config1 ~]# docker cp config_api_1:/etc/contrail/contrail-api.conf /tmp/db-dump/

   ## Stop Configuration Services on All Config Nodes ##
   [root@config1 ~]# docker stop contrail_config_svc_monitor
   [root@config1 ~]# docker stop contrail_config_device_manager
   [root@config1 ~]# docker stop contrail_config_schema
   [root@config1 ~]# docker stop contrail_config_api
   [root@config1 ~]# docker stop contrail_config_nodemgr
   [root@config1 ~]# docker stop contrail_config_database_nodemgr

   [root@config2 ~]# docker stop contrail_config_svc_monitor
   [root@config2 ~]# docker stop contrail_config_device_manager
   [root@config2 ~]# docker stop contrail_config_schema
   [root@config2 ~]# docker stop contrail_config_api
   [root@config2 ~]# docker stop contrail_config_nodemgr
   [root@config2 ~]# docker stop contrail_config_database_nodemgr

   [root@config3 ~]# docker stop contrail_config_svc_monitor
   [root@config3 ~]# docker stop contrail_config_device_manager
   [root@config3 ~]# docker stop contrail_config_schema
   [root@config3 ~]# docker stop contrail_config_api
   [root@config3 ~]# docker stop contrail_config_nodemgr
   [root@config3 ~]# docker stop contrail_config_database_nodemgr

   ## Stop Analytics Services on All Analytics Nodes ##
   [root@analytics1 ~]# docker stop contrail_analytics_snmp_collector
   [root@analytics1 ~]# docker stop contrail_analytics_topology
   [root@analytics1 ~]# docker stop contrail_analytics_alarmgen
   [root@analytics1 ~]# docker stop contrail_analytics_api
   [root@analytics1 ~]# docker stop contrail_analytics_collector
   [root@analytics1 ~]# docker stop contrail_analytics_kafka

   [root@analytics2 ~]# docker stop contrail_analytics_snmp_collector
   [root@analytics2 ~]# docker stop contrail_analytics_topology
   [root@analytics2 ~]# docker stop contrail_analytics_alarmgen
   [root@analytics2 ~]# docker stop contrail_analytics_api
   [root@analytics2 ~]# docker stop contrail_analytics_collector
   [root@analytics2 ~]# docker stop contrail_analytics_kafka

   [root@analytics3 ~]# docker stop contrail_analytics_snmp_collector
   [root@analytics3 ~]# docker stop contrail_analytics_topology
   [root@analytics3 ~]# docker stop contrail_analytics_alarmgen
   [root@analytics3 ~]# docker stop contrail_analytics_api
   [root@analytics3 ~]# docker stop contrail_analytics_collector
   [root@analytics3 ~]# docker stop contrail_analytics_kafka

   ## Stop Cassandra ##
   [root@config1 ~]# docker stop contrail_config_database
   [root@config2 ~]# docker stop contrail_config_database
   [root@config3 ~]# docker stop contrail_config_database

   ## Stop Zookeeper ##
   [root@config1 ~]# docker stop contrail_config_zookeeper
   [root@config2 ~]# docker stop contrail_config_zookeeper
   [root@config3 ~]# docker stop contrail_config_zookeeper

   ## Backup Zookeeper Directories Before Deleting Zookeeper Data Directory Contents ##
   [root@config1 _data]# cd /var/lib/docker/volumes/config_zookeeper/
   [root@config1 config_zookeeper]# cp -R _data/version-2/ version-2-save
   [root@config1 config_zookeeper]# rm -rf _data/version-2/*
   [root@config2 _data]# cd /var/lib/docker/volumes/config_zookeeper/
   [root@config2 config_zookeeper]# cp -R _data/version-2/ version-2-save
   [root@config2 config_zookeeper]# rm -rf _data/version-2/*
   [root@config3 _data]# cd /var/lib/docker/volumes/config_zookeeper/
   [root@config3 config_zookeeper]# cp -R _data/version-2/ version-2-save
   [root@config3 config_zookeeper]# rm -rf _data/version-2/*

   ## Backup Cassandra Directory Before Deleting Cassandra Data Directory Contents ##
   [root@config1 ~]# cd /var/lib/docker/volumes/config_cassandra/
   [root@config1 config_cassandra]# cp -R _data/ Cassandra_data-save
   [root@config1 config_cassandra]# rm -rf _data/*

   [root@config2 ~]# cd /var/lib/docker/volumes/config_cassandra/
   [root@config2 config_cassandra]# cp -R _data/ Cassandra_data-save
   [root@config2 config_cassandra]# rm -rf _data/*

   [root@config3 ~]# cd /var/lib/docker/volumes/config_cassandra/
   [root@config3 config_cassandra]# cp -R _data/ Cassandra_data-save
   [root@config3 config_cassandra]# rm -rf _data/*

   ## Start Zookeeper ##
   [root@config1 ~]# docker start contrail_config_zookeeper
   [root@config2 ~]# docker start contrail_config_zookeeper
   [root@config3 ~]# docker start contrail_config_zookeeper

   ## Start Cassandra ##
   [root@config1 ~]# docker start contrail_config_database
   [root@config2 ~]# docker start contrail_config_database
   [root@config3 ~]# docker start contrail_config_database

   ## Run Docker Image & Mount TF TLS Certificates to TF SSL Directory ##
   [root@config1 ~]# docker image ls | grep config-api
   hub.juniper.net/contrail/contrail-controller-config-api  1909.30-ocata c9d757252a0c  4 months ago  583MB
   [root@config1 ~]# docker run --rm -it -v /tmp/db-dump/:/tmp/ -v /etc/contrail/ssl:/etc/contrail/ssl:ro --network host --entrypoint=/bin/bash hub.juniper.net/contrail/contrail-controller-config-api:1909.30-ocata

   ## Restore Data in New Docker Containers ##
   (config_api_1)[root@config1 /root]$ cd /usr/lib/python2.7/site-packages/cfgm_common/
   (config_api_1)[root@config1 /usr/lib/python2.7/site-packages/cfgm_common]$ python db_json_exim.py --import-from /tmp/db-dump.json --api-conf /tmp/contrail-api.conf

   ## Start Configuration Services on All Config Nodes ##
   [root@config1 ~]# docker start contrail_config_svc_monitor
   [root@config1 ~]# docker start contrail_config_device_manager
   [root@config1 ~]# docker start contrail_config_schema
   [root@config1 ~]# docker start contrail_config_api
   [root@config1 ~]# docker start contrail_config_nodemgr
   [root@config1 ~]# docker start contrail_config_database_nodemgr

   [root@config2 ~]# docker start contrail_config_svc_monitor
   [root@config2 ~]# docker start contrail_config_device_manager
   [root@config2 ~]# docker start contrail_config_schema
   [root@config2 ~]# docker start contrail_config_api
   [root@config2 ~]# docker start contrail_config_nodemgr
   [root@config2 ~]# docker start contrail_config_database_nodemgr

   [root@config3 ~]# docker start contrail_config_svc_monitor
   [root@config3 ~]# docker start contrail_config_device_manager
   [root@config3 ~]# docker start contrail_config_schema
   [root@config3 ~]# docker start contrail_config_api
   [root@config3 ~]# docker start contrail_config_nodemgr
   [root@config3 ~]# docker start contrail_config_database_nodemgr

   ## Start Configuration Services on All Analytics Nodes ##
   [root@analytics1 ~]# docker start contrail_analytics_snmp_collector
   [root@analytics1 ~]# docker start contrail_analytics_topology
   [root@analytics1 ~]# docker start contrail_analytics_alarmgen
   [root@analytics1 ~]# docker start contrail_analytics_api
   [root@analytics1 ~]# docker start contrail_analytics_collector
   [root@analytics1 ~]# docker start contrail_analytics_kafka

   [root@analytics2 ~]# docker start contrail_analytics_snmp_collector
   [root@analytics2 ~]# docker start contrail_analytics_topology
   [root@analytics2 ~]# docker start contrail_analytics_alarmgen
   [root@analytics2 ~]# docker start contrail_analytics_api
   [root@analytics2 ~]# docker start contrail_analytics_collector
   [root@analytics2 ~]# docker start contrail_analytics_kafka

   [root@analytics3 ~]# docker start contrail_analytics_snmp_collector
   [root@analytics3 ~]# docker start contrail_analytics_topology
   [root@analytics3 ~]# docker start contrail_analytics_alarmgen
   [root@analytics3 ~]# docker start contrail_analytics_api
   [root@analytics3 ~]# docker start contrail_analytics_collector
   [root@analytics3 ~]# docker start contrail_analytics_kafka


   ## Confirm Services are Active ##
   [root@config1 ~]# contrail-status
   [root@config2 ~]# contrail-status
   [root@config3 ~]# contrail-status

   [root@analytics1 ~]# contrail-status
   [root@analytics2 ~]# contrail-status
   [root@analytics3 ~]# contrail-status
