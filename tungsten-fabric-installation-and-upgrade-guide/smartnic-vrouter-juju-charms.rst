Using Netronome SmartNIC vRouter with Contrail Networking and Juju Charms
=========================================================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

.. note::

   The Netronome SmartNIC vRouter technology covered in this document is
   available for evaluation purposes only. It is not intended for
   deployment in production networks.

You can deploy Contrail Networking by using Juju charms. Juju helps you
deploy, configure, and efficiently manage applications on private clouds
and public clouds. Juju accesses the cloud with the help of a Juju
controller. A charm is a module containing a collection of scripts and
metadata and is used with Juju to deploy Contrail.

Starting in Contrail Networking Release 2011, Contrail Networking
supports Netronome Agilio CX SmartNICs for Contrail Networking
deployment with Juju charms. This feature enables service providers to
improve the forwarding performance which includes packets per second
(PPS) of vRouter. This optimizes server CPU usage and you can deploy
more Virtual Network Functions (VNFs) per server.

Before you begin:

-  Equip compute nodes with Netronome Agilio CX SmartNIC. For details,
   see `Agilio CX SmartNICs
   documentation <https://www.netronome.com/products/agilio-cx/>`__.

-  Retrieve Agilio charm.

   Register on Netronome support site at https://help.netronome.com and
   provide Docker Hub credentials.

   Netronome will provide the Agilio charm for SmartNIC vRouter
   deployment on compute nodes. Add the charm version as ``charm``
   variable in the `Bundle yaml
   file <smartnic-vrouter-juju-charms.html#bundle-yaml>`__. Also,
   Netronome will authorize Docker Hub registry access.

-  Note the ``Container Tags`` for your Contrail image to customize the
   ``image-tag`` variable in the `Bundle yaml
   file <smartnic-vrouter-juju-charms.html#bundle-yaml>`__. See `README
   Access to Contrail Registry
   20XX </documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf>`__  .

-  Note the following version tags:

   agilio-image-tag: 2.48-ubuntu-queens

   maas version: 2.6.2

   Linux kernel: bionic (ga-18.04)

Contrail supports the following charms:

-  contrail-agent

-  contrail-analytics

-  contrail-analyticsdb

-  contrail-controller

-  contrail-keystone-auth

-  contrail-openstack

The following topics describe how to use Netronome SmartNIC vRouter with
Contrail Networking and Juju charms.

.. raw:: html

   </div>

.. raw:: html

   </div>

Prepare to Install Contrail Networking by Using Juju Charms
-----------------------------------------------------------

Follow these steps to prepare for deployment:

1. Install Juju.

   .. raw:: html

      <div id="jd0e107" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      sudo apt-get update
      sudo apt-get upgrade
      apt install snapd -y
      snap install juju --classic

   .. raw:: html

      </div>

   .. raw:: html

      </div>

2. Configure Juju.

   You can add a cloud to Juju, and manage clouds already added to Juju.
   Juju recognizes a wide range of cloud types for adding a cloud.

   This is an example for adding a cloud by using interactive command.

   *Example: Adding an MAAS cloud to Juju*

   .. raw:: html

      <div id="jd0e120" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e121" dir="ltr">

   ``juju add-cloud``

   .. raw:: html

      </div>

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      Cloud Types
        maas
        manual
        openstack
        oracle
        vsphere

      Select cloud type: maas

      Enter a name for your maas cloud: maas-cloud

      Enter the API endpoint url: http://<ip-address>:<node>/MAAS

      Cloud "maas-cloud" successfully added
      You may bootstrap with 'juju bootstrap maas-cloud'

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   **Note**

   Juju 2.x is compatible with MAAS series 1.x and 2.x.

3. Create a Juju controller.

   .. raw:: html

      <div id="jd0e137" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju bootstrap --bootstrap-series=xenial <cloud name> <controller name>

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   **Note**

   A Juju controller manages and keeps track of applications in the Juju
   cloud environment.

Deploy Contrail Charms in a Bundle
----------------------------------

Follow these steps to deploy Contrail charms in a bundle.

1. Deploy Contrail charms.

   To deploy Contrail charms in a bundle, use the
   ``juju deploy <bundle_yaml_file>`` command.

   The following example shows you how to use ``bundle_yaml_file`` to
   deploy Contrail Networking with Netronome SmartNIC vRouter on MAAS
   based deployment.

   .. raw:: html

      <div id="bundle-yaml" class="sample" dir="ltr">

   **Bundle yaml file**

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      series: bionic
      variables:
        openstack-origin:             &openstack-origin               distro
        #vhost-gateway:               &vhost-gateway                  "192.x.40.254"
        data-network:                 &data-network                   "192.x.40.0/24"
        control-network:              &control-network                "192.x.30.0/24"
        virtioforwarder-coremask:     &virtioforwarder-coremask       "1,2"
        agilio-registry:              &agilio-registry                "netronomesystems"
        agilio-image-tag:             &agilio-image-tag               "2.48-ubuntu-queens"
        agilio-user:                  &agilio-user                    "<agilio-username>"
        agilio-password:              &agilio-password                "<agilio-password>"
        agilio-insecure:              &agilio-insecure                false
        agilio-phy:                   &agilio-phy                     "nfp_p0"
        docker-registry:              &docker-registry                "<registry-directory>"
        #docker-user:                 &docker-user                    "<docker_username>"
        #docker-password:             &docker-password                "<docker_password>"
        image-tag:                    &image-tag                      "2011.61"
        docker-registry-insecure:     &docker-registry-insecure       "true"
        dockerhub-registry:           &dockerhub-registry             "https://index.docker.io/v1/"  
      machines:
        "1":
          constraints: tags=controller
          series: bionic
        "2":
          constraints: tags=compute
          series: bionic
        "3":
          constraints: tags=neutron
          series: bionic
      services:
        ubuntu:
          charm: cs:ubuntu
          num_units: 1
          to: [ "1" ]
        ntp:
          charm: cs:ntp
          num_units: 0
          options:
                  #source: ntp.ubuntu.com
             source: 10.204.217.158
        mysql:
          charm: cs:percona-cluster
          num_units: 1
          options:
            dataset-size: 15%
            max-connections: 10000
            root-password: <password>
            sst-password: <password>
            min-cluster-size: 1
          to: [ "lxd:1" ]
        rabbitmq-server:
          charm: cs:rabbitmq-server
          num_units: 1
          options:
            min-cluster-size: 1
          to: [ "lxd:1" ]
        heat:
          charm: cs:heat
          num_units: 1
          expose: true
          options:
            debug: true
            openstack-origin: *openstack-origin
          to: [ "lxd:1" ]
        keystone:
          charm: cs:keystone
          expose: true
          num_units: 1
          options:
            admin-password: <password>
            admin-role: admin
            openstack-origin: *openstack-origin
            preferred-api-version: 3
        nova-cloud-controller:
          charm: cs:nova-cloud-controller
          num_units: 1
          expose: true
          options:
            network-manager: Neutron
            openstack-origin: *openstack-origin
          to: [ "lxd:1" ]
        neutron-api:
          charm: cs:neutron-api
          expose: true
          num_units: 1
          series: bionic
          options:
            manage-neutron-plugin-legacy-mode: false
            openstack-origin: *openstack-origin
          to: [ "3" ]
        glance:
          charm: cs:glance
          expose: true
          num_units: 1
          options:
            openstack-origin: *openstack-origin
          to: [ "lxd:1" ]
        openstack-dashboard:
          charm: cs:openstack-dashboard
          expose: true
          num_units: 1
          options:
            openstack-origin: *openstack-origin
          to: [ "lxd:1" ]
        nova-compute:
          charm: cs:nova-compute
          num_units: 0
          expose: true
          options:
            openstack-origin: *openstack-origin
        nova-compute-dpdk:
          charm: cs:nova-compute
          num_units: 0
          expose: true
          options:
            openstack-origin: *openstack-origin
        nova-compute-accel:
          charm: cs:nova-compute
          num_units: 2
          expose: true
          options:
            openstack-origin: *openstack-origin
          to: [ "2" ]
        contrail-openstack:
          charm: ./tf-charms/contrail-openstack
          series: bionic
          expose: true
          num_units: 0
          options:
            docker-registry: *docker-registry
            #docker-user: *docker-user
            #docker-password: *docker-password
            image-tag: *image-tag
            docker-registry-insecure: *docker-registry-insecure
        contrail-agent:
          charm: ./tf-charms/contrail-agent
          num_units: 0
          series: bionic
          expose: true
          options:
            log-level: "SYS_DEBUG"
            docker-registry: *docker-registry
            #docker-user: *docker-user
            #docker-password: *docker-password
            image-tag: *image-tag
            docker-registry-insecure: *docker-registry-insecure
            #vhost-gateway: *vhost-gateway
            physical-interface: *agilio-phy
        contrail-agent-dpdk:
          charm: ./tf-charms/contrail-agent
          num_units: 0
          series: bionic
          expose: true
          options:
            log-level: "SYS_DEBUG"
            docker-registry: *docker-registry
            #docker-user: *docker-user
            #docker-password: *docker-password
            image-tag: *image-tag
            docker-registry-insecure: *docker-registry-insecure
            dpdk: true
            dpdk-main-mempool-size: "65536"
            dpdk-pmd-txd-size: "2048"
            dpdk-pmd-rxd-size: "2048"
            dpdk-driver: ""
            dpdk-coremask: "1-4"
            #vhost-gateway: *vhost-gateway
            physical-interface: "nfp_p0"
        contrail-analytics:
          charm: ./tf-charms/contrail-analytics
          num_units: 1
          series: bionic
          expose: true
          options:
            log-level: "SYS_DEBUG"
            docker-registry: *docker-registry
            #docker-user: *docker-user
            #docker-password: *docker-password
            image-tag: *image-tag
            control-network: *control-network
            docker-registry-insecure: *docker-registry-insecure
          to: [ "1" ]
        contrail-analyticsdb:
          charm: ./tf-charms/contrail-analyticsdb
          num_units: 1
          series: bionic
          expose: true
          options:
            log-level: "SYS_DEBUG"
            cassandra-minimum-diskgb: "4"
            cassandra-jvm-extra-opts: "-Xms8g -Xmx8g"
            docker-registry: *docker-registry
            #docker-user: *docker-user
            #docker-password: *docker-password
            image-tag: *image-tag
            control-network: *control-network
            docker-registry-insecure: *docker-registry-insecure
          to: [ "1" ]
        contrail-controller:
          charm: ./tf-charms/contrail-controller
          series: bionic
          expose: true
          num_units: 1
          options:
            log-level: "SYS_DEBUG"
            cassandra-minimum-diskgb: "4"
            cassandra-jvm-extra-opts: "-Xms8g -Xmx8g"
            docker-registry: *docker-registry
            #docker-user: *docker-user
            #docker-password: *docker-password
            image-tag: *image-tag
            docker-registry-insecure: *docker-registry-insecure
            control-network: *control-network
            data-network: *data-network
            auth-mode: no-auth
          to: [ "1" ]
        contrail-keystone-auth:
          charm: ./tf-charms/contrail-keystone-auth
          series: bionic
          expose: true
          num_units: 1
          to: [ "lxd:1" ]
        agilio-vrouter5:
          charm: ./charm-agilio-vrt-5-37
          expose: true
          options:
            virtioforwarder-coremask: *virtioforwarder-coremask
            agilio-registry: *agilio-registry
            agilio-insecure: *agilio-insecure
            agilio-image-tag: *agilio-image-tag
            agilio-user: *agilio-user
            agilio-password: *agilio-password
      relations:
        - [ "ubuntu", "ntp" ]
        - [ "neutron-api", "ntp" ]
        - [ "keystone", "mysql" ]
        - [ "glance", "mysql" ]
        - [ "glance", "keystone" ]
        - [ "nova-cloud-controller:shared-db", "mysql:shared-db" ]
        - [ "nova-cloud-controller:amqp", "rabbitmq-server:amqp" ]
        - [ "nova-cloud-controller", "keystone" ]
        - [ "nova-cloud-controller", "glance" ]
        - [ "neutron-api", "mysql" ]
        - [ "neutron-api", "rabbitmq-server" ]
        - [ "neutron-api", "nova-cloud-controller" ]
        - [ "neutron-api", "keystone" ]
        - [ "nova-compute:amqp", "rabbitmq-server:amqp" ]
        - [ "nova-compute", "glance" ]
        - [ "nova-compute", "nova-cloud-controller" ]
        - [ "nova-compute", "ntp" ]
        - [ "openstack-dashboard:identity-service", "keystone" ]
        - [ "contrail-keystone-auth", "keystone" ]
        - [ "contrail-controller", "contrail-keystone-auth" ]
        - [ "contrail-analytics", "contrail-analyticsdb" ]
        - [ "contrail-controller", "contrail-analytics" ]
        - [ "contrail-controller", "contrail-analyticsdb" ]
        - [ "contrail-openstack", "nova-compute" ]
        - [ "contrail-openstack", "neutron-api" ]
        - [ "contrail-openstack", "contrail-controller" ]
        - [ "contrail-agent:juju-info", "nova-compute:juju-info" ]
        - [ "contrail-agent", "contrail-controller"]
        - [ "contrail-agent-dpdk:juju-info", "nova-compute-dpdk:juju-info" ]
        - [ "contrail-agent-dpdk", "contrail-controller"]
        - [ "nova-compute-dpdk:amqp", "rabbitmq-server:amqp" ]
        - [ "nova-compute-dpdk", "glance" ]
        - [ "nova-compute-dpdk", "nova-cloud-controller" ]
        - [ "nova-compute-dpdk", "ntp" ]
        - [ "contrail-openstack", "nova-compute-dpdk" ]
        - [ "contrail-agent:juju-info", "nova-compute-accel:juju-info" ]
        - [ "nova-compute-accel:amqp", "rabbitmq-server:amqp" ]
        - [ "nova-compute-accel", "glance" ]
        - [ "nova-compute-accel", "nova-cloud-controller" ]
        - [ "nova-compute-accel", "ntp" ]
        - [ "contrail-openstack", "nova-compute-accel" ]
        - [ "agilio-vrouter5:juju-info", "nova-compute-accel:juju-info"  ]
        - [ "heat:shared-db" , "mysql:shared-db" ]
        - [ "heat:amqp" , "rabbitmq-server:amqp" ]
        - [ "heat:identity-service" , "keystone:identity-service" ]
        - [ "contrail-openstack:heat-plugin" , "heat:heat-plugin-subordinate" ]

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   You can create or modify the Contrail charm deployment bundle YAML
   file to:

   -  Point to machines or instances where the Contrail charms must be
      deployed.

   -  Include the options you need.

      Each Contrail charm has a specific set of options. The options you
      choose depend on the charms you select. For more information on
      the options that are available, see `Options for Juju
      Charms <../task/configuration/juju-charms-options.html>`__.

2. (Optional) Check the status of deployment.

   You can check the status of the deployment by using the
   ``juju status`` command.

3. Enable configuration statements.

   Based on your deployment requirements, you can enable the following
   configuration statements:

   -  ``contrail-agent``

      For more information, see
      https://jaas.ai/u/juniper-os-software/contrail-agent/.

   -  ``contrail-analytics``

      For more information, see
      https://jaas.ai/u/juniper-os-software/contrail-analytics.

   -  ``contrail-analyticsdb``

      For more information, see
      https://jaas.ai/u/juniper-os-software/contrail-analyticsdb.

   -  ``contrail-controller``

      For more information, see
      https://jaas.ai/u/juniper-os-software/contrail-controller.

   -  ``contrail-keystone-auth``

      For more information, see
      https://jaas.ai/u/juniper-os-software/contrail-keystone-auth.

   -  ``contrail-openstack``

      For more information see,
      https://jaas.ai/u/juniper-os-software/contrail-openstack.

.. raw:: html

   <div class="table">

.. raw:: html

   <div class="caption">

Release History Table

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row table-head">

.. raw:: html

   <div class="table-cell">

Release

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Description

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`2011 <#jd0e16>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Starting in Contrail Networking Release 2011, Contrail Networking
supports Netronome Agilio CX SmartNICs for Contrail Networking
deployment with Juju charms.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

 
