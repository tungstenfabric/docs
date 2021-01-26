Installing Contrail with OpenStack by Using Juju Charms
=======================================================

 

You can deploy Contrail by using Juju Charms. Juju helps you deploy,
configure, and efficiently manage applications on private clouds and
public clouds. Juju accesses the cloud with the help of a Juju
controller. A Charm is a module containing a collection of scripts and
metadata and is used with Juju to deploy Contrail.

Starting in Tungsten Fabric Release 2011, Tungsten Fabric
supports OpenStack Ussuri with Ubuntu version 18.04 (Bionic Beaver) and
Ubuntu version 20.04 (Focal Fossa).

TF supports the following charms:

-  contrail-agent

-  contrail-analytics

-  contrail-analyticsdb

-  contrail-controller

-  contrail-keystone-auth

-  contrail-openstack

These topics describe how to deploy TF by using Juju Charms.

Preparing to Deploy TF by Using Juju Charms
-------------------------------------------------

Follow these steps to prepare for deployment:

1. Install Juju.

   ::

      sudo apt-get update
      sudo apt-get upgrade
      sudo apt-get install juju

2. Configure Juju.

   You can add a cloud to Juju, identify clouds supported by Juju, and
   also manage clouds already added to Juju.

   -  Adding a cloud—Juju recognizes a wide range of cloud types. You
      can use any one of the following methods to add a cloud to Juju:

      -  Adding a Cloud by Using Interactive Command

         *Example: Adding an MAAS cloud to Juju*

         ::

            juju add-cloud

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

         .. note::

            Juju 2.x is compatible with MAAS series 1.x and 2.x.

      -  Adding a Cloud Manually
         You use a YAML configuration file to add a cloud manually.
         Enter the following command:
         ::

            juju add-cloud <cloud-name>
            juju add-credential <cloud name>

         For an example, to add the cloud *junmaas*, assuming that the
         name of the configuration file in the directory is
         ``maas-clouds.yaml``, you run the following command:

         ::

            juju add-cloud junmaas maas-clouds.yaml
        
         The following is the format of the YAML configuration file:

         ::

            clouds:
              <cloud_name>:
                type: <type_of_cloud>
                auth-types: [<authenticaton_types>]
                regions:
                  <region-name>:
                    endpoint: <http://<ip-address>:<node>/MAAS>

         .. note::

            The ``auth-types`` for a MAAS cloud type is ``oauth1``.

   -  Identifying a supported cloud

      Juju recognizes the cloud types given below. You use the
      ``juju clouds`` command to list cloud types that are supported by
      Juju.

      ::

         $ juju clouds
         Cloud        Regions  Default          Type        Description
         aws               15  us-east-1        ec2         Amazon Web Services
         aws-china          1  cn-north-1       ec2         Amazon China
         aws-gov            1  us-gov-west-1    ec2         Amazon (USA Government)
         azure             26  centralus        azure       Microsoft Azure
         azure-china        2  chinaeast        azure       Microsoft Azure China
         cloudsigma         5  hnl              cloudsigma  CloudSigma Cloud
         google            13  us-east1         gce         Google Cloud Platform
         joyent             6  eu-ams-1         joyent      Joyent Cloud
         oracle             5  uscom-central-1  oracle      Oracle Cloud
         rackspace          6  dfw              rackspace   Rackspace Cloud
         localhost          1  localhost        lxd         LXD Container Hypervisor

3. Create a Juju controller.

   ::

      juju bootstrap --bootstrap-series=xenial <cloud name> <controller name>

   .. note::

      A Juju controller manages and keeps track of applications in the Juju
      cloud environment.

Deploying TF Charms
-------------------------
You can deploy TF Charms in a bundle or manually.
Deploy TF Charms in a Bundle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to deploy TF Charms in a bundle.

1. Deploy TF Charms.

   To deploy TF Charms in a bundle, use the
   ``juju deploy <bundle_yaml_file>`` command.
   The following example shows you how to use ``bundle_yaml_file`` to
   deploy TF on Amazon Web Services (AWS) Cloud.
   ::

      series: bionic

      variables:
        openstack-origin:             &openstack-origin               distro
        #vhost-gateway:               &vhost-gateway                  "192.x.40.254"
        data-network:                 &data-network                   "192.x.40.0/24"
        control-network:              &control-network                "192.x.30.0/24"
        virtioforwarder-coremask:     &virtioforwarder-coremask       "1,2"
        agilio-registry:              &agilio-registry                "netronomesystems"
        agilio-image-tag:             &agilio-image-tag               "latest-ubuntu-queens"
        agilio-user:                  &agilio-user                    "<agilio-username>"
        agilio-password:              &agilio-password                "<agilio-password>"
        agilio-insecure:              &agilio-insecure                false
        agilio-phy:                   &agilio-phy                     "nfp_p0"
        docker-registry:              &docker-registry                "<registry-directory>"
        #docker-user:                 &docker-user                    "<docker_username>"
        #docker-password:             &docker-password                "<docker_password>"
        image-tag:                    &image-tag                      "2008.121"
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

   You can create or modify the TF Charm deployment bundle YAML
   file to:

   -  Point to machines or instances where the TF Charms must be
      deployed.

   -  Include the options you need.

      Each TF Charm has a specific set of options. The options you
      choose depend on the charms you select. For more information on
      the options that are available, see `Options for Juju
      Charms <deploying-contrail-using-juju-charms.html#options-for-juju-charms>`__.

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

Deploying Juju Charms with OpenStack Manually
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you begin deployment, ensure that you have:

-  Installed and configured Juju

-  Created a Juju controller

-  Ubuntu 16.04 or Ubuntu 18.04 installed

Follow these steps to deploy Juju Charms manually:

1. Create machine instances for OpenStack, compute, and Tungsten Fabric.

   ::

      juju add-machine --constraints mem=8G cores=2 root-disk=40G --series=xenial   #for openstack machine(s) 0

   ::

      juju add-machine --constraints mem=7G cores=4 root-disk=40G --series=xenial   #for compute machine(s) 1,(3)

   ::

      juju add-machine --constraints mem=15G cores=2 root-disk=300G --series=xenial #for TF machine 2

2. Deploy OpenStack services.

   You can deploy OpenStack services by using any one of the following
   methods:

   -  By specifying the OpenStack parameters in a YAML file

      The following is an example of a YAML-formatted
      (``nova-compute-config.yaml``) file.

      ::

         nova-compute:
             openstack-origin: cloud:xenial-ocata
             virt-type: qemu 
             enable-resize: True
             enable-live-migration: True
             migration-auth-type: ssh

      Use this command to deploy OpenStack services by using a
      YAML-formatted file:

      ::

         juju deploy cs:xenial/nova-compute --config ./nova-compute-config.yaml

   -  By using CLI

      To deploy OpenStack services through the CLI:

      ::

         juju deploy cs:xenial/nova-cloud-controller --config console-access-protocol=novnc --config openstack-origin=cloud:xenial-ocata

   -  By using a combination of YAML-formatted file and CLI

      To deploy OpenStack services by using a combination of
      YAML-formatted file and CLI:

      .. note::

         Use the ``--to <machine number>`` command to point to a machine or
         container where you want the application to be deployed.

      ::

         juju deploy cs:xenial/ntp
         juju deploy cs:xenial/rabbitmq-server --to lxd:0
         juju deploy cs:xenial/percona-cluster mysql --config root-password=<root-password> --config max-connections=1500 --to lxd:0
         juju deploy cs:xenial/openstack-dashboard --config openstack-origin=cloud:xenial-ocata --to lxd:0
         juju deploy cs:xenial/nova-cloud-controller --config console-access-protocol=novnc --config openstack-origin=cloud:xenial-ocata --config network-manager=Neutron --to lxd:0
         juju deploy cs:xenial/neutron-api --config manage-neutron-plugin-legacy-mode=false --config openstack-origin=cloud:xenial-ocata --config neutron-security-groups=true --to lxd:0
         juju deploy cs:xenial/glance --config openstack-origin=cloud:xenial-ocata --to lxd:0
         juju deploy cs:xenial/keystone --config admin-password=<admin-password> --config admin-role=admin --config openstack-origin=cloud:xenial-ocata --to lxd:0

      .. note::

         You set OpenStack services on different machines or on different
         containers to prevent HAProxy conflicts from applications.

3. Deploy and configure nova-compute.

   ::

      juju deploy cs:xenial/nova-compute --config ./nova-compute-config.yaml --to 1

   .. note::

      You can deploy nova-compute to more than one compute machine.

   (Optional) To add additional computes:

   ::

      juju add-unit nova-compute --to 3 # Add one more unit

4. Deploy and configure TF services.

   ::

      juju deploy --series=xenial $CHARMS_DIRECTORY/contrail-charms/contrail-keystone-auth --to 2
      juju deploy --series=xenial $CHARMS_DIRECTORY/contrail-charms/contrail-controller --config auth-mode=rbac --config cassandra-minimum-diskgb=4 --config cassandra-jvm-extra-opts="-Xms1g -Xmx2g" --to 2
      juju deploy --series=xenial $CHARMS_DIRECTORY/contrail-charms/contrail-analyticsdb cassandra-minimum-diskgb=4 --config cassandra-jvm-extra-opts="-Xms1g -Xmx2g" --to 2
      juju deploy --series=xenial $CHARMS_DIRECTORY/contrail-charms/contrail-analytics --to 2
      juju deploy --series=xenial $CHARMS_DIRECTORY/contrail-charms/contrail-openstack
      juju deploy --series=xenial $CHARMS_DIRECTORY/contrail-charms/contrail-agent

5. Enable applications to be available to external traffic:

   ::

      juju expose openstack-dashboard
      juju expose nova-cloud-controller
      juju expose neutron-api
      juju expose glance
      juju expose keystone

6. Enable contrail-controller and contrail-analytics services to be
   available to external traffic if you do not use HAProxy.

   ::

      juju expose contrail-controller
      juju expose contrail-analytics

7. Apply SSL.

   You can apply SSL if needed. To use SSL with TF services,
   deploy easy-rsa service and ``add-relation`` command to create
   relations to contrail-controller service and contrail-agent services.

   ::

      juju deploy cs:~containers/xenial/easyrsa --to 0
      juju add-relation easyrsa contrail-controller
      juju add-relation easyrsa contrail-agent

8. (Optional) HA configuration.

   If you use more than one controller, follow the HA solution given
   below:

   1. Deploy HAProxy and Keepalived services.

      HAProxy charm is deployed on machines with TF controllers.
      HAProxy charm must have ``peering_mode`` set to ``active-active``.
      If ``peering_mode`` is set to ``active-passive``, HAProxy creates
      additional listeners on the same ports as other TF services.
      This leads to port conflicts.

      Keepalived charm does not require ``to`` option.

      ::

         juju deploy cs:xenial/haproxy --to <first contrail-controller machine> --config peering_mode=active-active
         juju add-unit haproxy --to <another contrail-controller machine>
         juju deploy cs:~boucherv29/keepalived-19 --config virtual_ip=<vip>

   2. Enable HAProxy to be available to external traffic.

      ::

         juju expose haproxy

      .. note::

         If you enable HAProxy to be available to external traffic, do not
         follow step 6.

   3. Add HAProxy and Keepalived relations.

      ::

         juju add-relation haproxy:juju-info keepalived:juju-info
         juju add-relation contrail-analytics:http-services haproxy
         juju add-relation contrail-controller:http-services haproxy
         juju add-relation contrail-controller:https-services haproxy

   4. Configure contrail-controller service with VIP.

      ::

         juju set contrail-controller vip=<vip>

9. Add other necessary relations.

   ::

      juju add-relation keystone:shared-db mysql:shared-db
      juju add-relation glance:shared-db mysql:shared-db
      juju add-relation keystone:identity-service glance:identity-service
      juju add-relation nova-cloud-controller:image-service glance:image-service
      juju add-relation nova-cloud-controller:identity-service keystone:identity-service
      juju add-relation nova-cloud-controller:cloud-compute nova-compute:cloud-compute
      juju add-relation nova-compute:image-service glance:image-service
      juju add-relation nova-compute:amqp rabbitmq-server:amqp
      juju add-relation nova-cloud-controller:shared-db mysql:shared-db
      juju add-relation nova-cloud-controller:amqp rabbitmq-server:amqp
      juju add-relation openstack-dashboard:identity-service keystone

      juju add-relation neutron-api:shared-db mysql:shared-db
      juju add-relation neutron-api:neutron-api nova-cloud-controller:neutron-api
      juju add-relation neutron-api:identity-service keystone:identity-service
      juju add-relation neutron-api:amqp rabbitmq-server:amqp

      juju add-relation contrail-controller ntp
      juju add-relation nova-compute:juju info ntp:juju info

      juju add-relation contrail-controller contrail-keystone-auth
      juju add-relation contrail-keystone-auth keystone
      juju add-relation contrail-controller contrail-analytics
      juju add-relation contrail-controller contrail-analyticsdb
      juju add-relation contrail-analytics contrail-analyticsdb

      juju add-relation contrail-openstack neutron-api
      juju add-relation contrail-openstack nova-compute
      juju add-relation contrail-openstack contrail-controller

      juju add-relation contrail-agent:juju info nova-compute:juju info
      juju add-relation contrail-agent contrail-controller

Options for Juju Charms
-----------------------

Each TF Charm has a specific set of options. The options you
choose depend on the charms you select. The following tables list the
various options you can choose:

-  Options for contrail-agent Charms.

   Table 1: Options for contrail-agent

.. list-table:: 
   :header-rows: 1

   * - Option
     - Default option
     - Description
   * - physical-interface
     - 
     - Specify the interface where you want to install vhost0 on. 
       If you do not specify an interface, vhost0 is installed on the default gateway interface.
   * - vhost-gateway
     - auto
     - Specify the gateway for vhost0. You can enter either an IP address or the keyword 
       (<span class="cli" data-v-pre="">auto</span>) to automatically set a gateway based on 
       the existing vhost routes.
   * - remove-juju-bridge
     - true
     - To install vhost0 directly on the interface, enable this option to remove any bridge created to deploy LXD/LXC and KVM workloads.
   * - dpdk
     - false
     - Specify DPDK vRouter
   * - dpdk-driver
     - uio_pci_generic
     - Specify DPDK driver for the physical interface
   * - dpdk-hugepages
     - 70%
     - Specify the percentage of huge pages reserved for DPDK vRouter and OpenStack instances
   * - dpdk-coremask
     - 1
     - Specify the vRouter CPU affinity mask to determine on which CPU the DPDK vRouter will run
   * - dpdk-main-mempool-size
     - 
     - Specify the main packet pool size
   * - dpdk-pmd-txd-size
     - 
     - Specify the DPDK PMD Tx Descriptor size
   * - dpdk-pmd-rxd-size
     - 
     - Specify the DPDK PMD Rx Descriptor size
   * - docker-registry
     - opencontrailnightly
     - Specify the URL of the docker-registry
   * - docker-registry-insecure
     - false
     - Specify if the docker-registry should be configured
   * - docker-user
     - 
     - Log in to the docker registry
   * - docker-password
     - 
     - Specify the docker-registry password
   * - image-tag
     - latest
     - Specify the docker image tag
   * - log-level
     - SYS_NOTICE
     - Specify the log level for TF services.
       Options:`SYS_EMERG`, `SYS_ALERT`, `SYS_CRIT`, `SYS_ERR`, `SYS_WARN`, `SYS_NOTICE`, `SYS_INFO`, `SYS_DEBUG`
   * - http_proxy
     - 
     - Specify URL
   * - kernel-hugepages-1g
     - Parameter not enabled by default
       **Note:** 2MB huge pages for kernel-mode vRouters are enabled by default
     - Specify the number of 1G huge pages for use with vRouters in kernel mode.
       You can enable huge pages to avoid compute node reboots during software upgrades.
       This parameter must be specified at initial deployment. It cannot be modified in an active deployment. 
       If you need to migrate to huge page usage in an active deployment, use 2MB huge pages if suitable for your environment.
       We recommend allotting 2GB of memory—either using the default 1024x2MB huge page size
       setting or the 2x1GB size setting—for huge pages. Other huge page size settings should only be set by expert users in specialized circumstances.
       1GB and 2MB huge pages cannot be enabled simultaneously in environments using Juju. 
       If you are using this command parameter to enable 1GB huge pages, you must also disable 2MB huge pages. 
       2MB huge pages can be disabled by entering the ``juju config contrail-agent kernel-hugepages-2m=““`` command with an empty value.
       A compute node reboot is required to enable a huge page setting configuration change. After this initial reboot,
       compute nodes can complete software upgrades without a reboot. Huge pages are disabled for kernel-mode vRouters if the
       ``kernel-hugepages-1g`` and the ``kernel-hugepages-2m`` options are not set.
   * - kernel-hugepages-2m
     - 1024
     - Specify the number of 2MB huge pages for use with vRouters in kernel mode. Huge pages in Tungsten Fabric
       are used primarily to allocate flow and bridge table memory within the vRouter. Huge pages for kernel-mode vRouters
       provide enough flow and bridge table memory to avoid compute node reboots to complete future Tungsten Fabric software upgrades.
       1024x2MB huge pages are configured by default starting in Tungsten Fabric Release 2005. A compute node reboot is
       required to enable a kernel-mode vRouter huge page setting configuration change, however, so this huge page setting is
       not enabled on a compute node until the compute node is rebooted. After a compute node is rebooted to enable a vRouter
       huge page setting, compute nodes can complete software upgrades without a reboot. We recommend allotting 2GB of memory—either
       using the default 1024x2MB huge page size setting or the 2x1GB size setting—for kernel-mode vRouter huge pages.
       Other huge page size settings should only be set by expert users in specialized circumstances. 1GB and 2MB huge pages cannot
       be enabled simultaneously in environments using Juju. If you are using this command parameter to enable 2MB huge pages,
       you must also disable 1GB huge pages. 1GB huge pages are disabled by default and can also be disabled by entering the
       ``juju config contrail-agent kernel-hugepages-1g=““`` command with an empty value. 1GB huge pages can only be enabled at
       initial deployment; you cannot initially enable 1GB huge pages in an active deployment.
       Huge pages are disabled for kernel-mode vRouters if the ``kernel-hugepages-1g`` and the ``kernel-hugepages-2m`` options are not set.
   * - no_proxy
     - 
     - Specify the list of destinations that must be directly accessed      

|

-  Options for contrail-analytics Charms.

   Table 2: Options for contrail-analytics

.. list-table:: 
   :header-rows: 1

   * - Option
     - Default option
     - Description
   * - control-network
     - 
     - Specify the IP address and network mask of the control network
   * - docker-registry
     - 
     - Specify the URL of the docker-registry
   * - docker-registry-insecure
     - false
     - Specify if the docker-registry should be configured
   * - docker-user
     - 
     - Log in to the docker registry
   * - docker-password
     - 
     - Specify the docker-registry password
   * - image-tag
     - 
     - Specify the docker image tag.
   * - log-level
     - SYS_NOTICE
     - Specify the log level for TF services.
       Options: ``SYS_EMERG``, ``SYS_ALERT``, ``SYS_CRIT``, ``SYS_ERR``, ``SYS_WARN``, ``SYS_NOTICE``, ``SYS_INFO``, ``SYS_DEBUG``
   * - http_proxy
     - 
     - Specify URL.
   * - https_proxy
     - 
     - Specify URL.
   * - no_proxy
     - 
     - Specify the list of destinations that must be directly accessed.

|

-  Options for contrail-analyticsdb Charms.

   Table 3: Options for contrail-analyticsdb

.. list-table:: 
   :header-rows: 1

   * - Option
     - Default option
     - Description
   * - control-network
     - 
     - Specify the IP address and network mask of the control network
   * - cassandra-minimum-diskgb
     - 256
     - Specify the minimum disk requirement
   * - cassandra-jvm-extra-opts
     -    
     - Specify the memory limit
   * - docker-registry
     -  	
     - Specify the URL of the docker-registry
   * - docker-registry-insecure
     - false
     - Specify if the docker-registry should be configured
   * - docker-user
     -
     - Log in to the docker registry
   * - docker-password
     - 
     - Specify the docker-registry password
   * - image-tag
     -
     - Specify the docker image tag.
   * - log-level
     - SYS_NOTICE
     - Specify the log level for TF services.
       Options: ``SYS_EMERG``, ``SYS_ALERT``, ``SYS_CRIT``, ``SYS_ERR``, ``SYS_WARN``, ``SYS_NOTICE``, ``SYS_INFO``, ``SYS_DEBUG``
   * - http_proxy
     -
     - Specify URL.
   * - https_proxy
     -
     - Specify URL.
   * - no_proxy
     -
     - Specify the list of destinations that must be directly accessed.

|

-  Options for contrail-controller Charms.

   Table 4: Options for contrail-controller

.. list-table:: 
   :header-rows: 1

   * - Option
     - Default option
     - Description
   * - control-network
     - 
     - Specify the IP address and network mask of the control network
   * - auth-mode
     - rbac
     - Specify the authentication mode.
       Options: ``rbsc``, ``cloud-admin``, ``no-auth``.
       For more information, see `https://github.com/tungstenfabric/docs/blob/master/wiki/tf-controller/RBAC.md <https://github.com/tungstenfabric/docs/blob/master/wiki/tf-controller/RBAC.md>`_
   * - cassandra-minimum-diskgb
     - 20
     - Specify the minimum disk requirement
   * - cassandra-jvm-extra-opts
     - 
     - Specify the memory limit
   * - cloud-admin-role
     - admin
     - Specify the role name in keystone for users who have admin-level access
   * - global-read-only-role
     - 
     - Specify the role name in keystone for users who have read-only access
   * - vip
     - 
     - Specify if the Tungsten Fabric API VIP is used for configuring client-side software. If not specified, private IP of the first Tungsten Fabric API VIP unit will be used
   * - use-external-rabbitmq
     - false
     - To enable the Charm to use the internal RabbitMQ server, set ``use-external-rabbitmq`` to ``false.
       To use an external AMQP server, set ``use-external-rabbitmq`` to ``true``.
       **Note:** Do not change the flag after deployment.
   * - flow-export-rate
     - 0
     - Specify how many flow records are exported by vRouter agent to the Tungsten Fabric Collector when a flow is created or deleted
   * - docker-registry
     - 
     - Specify the URL of the docker-registry.
   * - docker-registry-insecure
     - false
     - Specify if the docker-registry should be configured.
   * - docker-user
     - 
     - Log in to the docker registry.
   * - docker-password
     - 
     - Specify the docker-registry password.
   * - image-tag
     - 
     - Specify the docker image tag.
   * - log-level
     - SYS_NOTICE
     - Specify the log level for TF services.
       Options: ``SYS_EMERG``, ``SYS_ALERT``, ``SYS_CRIT``, ``SYS_ERR``, ``SYS_WARN``, ``SYS_NOTICE``, ``SYS_INFO``, ``SYS_DEBUG``
   * - http_proxy
     - 
     - Specify URL.
   * - no_proxy
     - 
     - Specify the list of destinations that must be directly accessed.

|

-  Options for contrail-keystone-auth Charms.

   Table 5: Options for contrail-keystone-auth

.. list-table:: 
   :header-rows: 1

   * - Option
     - Default option
     - Description
   * - ssl_ca
     - 
     - Specify if the base64-encoded SSL CA certificate is provided to TF keystone clients.
       **Note:** This certificate is required if you use a privately signed ssl_cert and ssl_key.

|

-  Options for contrail-openstack Charms.

   Table 6: Options for contrail-controller

.. list-table:: 
   :header-rows: 1

   * - Option
     - Default option
     - Description
   * - enable-metadata-server
     - true
     - Set enable-metadata-server to true to configure metadata and enable nova to run a local instance of nova-api-metadata for virtual machines
   * - use-internal-endpoints
     - false
     - Set use-internal-endpoints to true for OpenStack to configure services to use internal endpoints.
   * - heat-plugin-dirs
     - /usr/lib64/heat,/usr
       /lib/heat/usr/lib/
       python2.7/dist-packages/
       vnc_api/gen/heat/
       resources
     - Specify the heat plugin directories.
   * - docker-registry
     - 
     - Specify the URL of the docker-registry.
   * - docker-registry-insecure
     - false
     - Specify if the docker-registry should be configured.
   * - docker-user
     - 
     - Log in to the docker registry.
   * - docker-password
     - 
     - Specify the docker-registry password.
   * - image-tag
     - 
     - Specify the docker image tag.
   * - log-level
     - SYS_NOTICE
     - Specify the log level for TF services.
       Options: ``SYS_EMERG``, ``SYS_ALERT``, ``SYS_CRIT``, ``SYS_ERR``, ``SYS_WARN``, ``SYS_NOTICE``, ``SYS_INFO``, ``SYS_DEBUG``
   * - http_proxy
     - 
     - Specify URL.
   * - https_proxy
     - 
     - Specify URL.
   * - no_proxy
     - 
     - Specify the list of destinations that must be directly accessed.

.. list-table:: **Release History Table**
   :header-rows: 1

   * - Release
     - Description
   * - 2011
     - Starting in Tungsten Fabric Release 2011, Tungsten Fabric
       supports OpenStack Ussuri with Ubuntu version 18.04 (Bionic Beaver) and
       Ubuntu version 20.04 (Focal Fossa).

