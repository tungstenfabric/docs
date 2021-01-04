Setting Up the Overcloud
========================

 

Configuring the Overcloud
-------------------------

Use this example procedure on the undercloud to set up the configuration
for the overcloud.

1. Specify the name server to be used:

   .. raw:: html

      <div id="jd0e23" class="example" dir="ltr">

   ::

      undercloud_nameserver=8.8.8.8 
      openstack subnet set `openstack subnet show ctlplane-subnet -c id -f value` --dns-nameserver ${undercloud_nameserver}

   .. raw:: html

      </div>

2. Retrieve and upload the overcloud images.

   1. Create the image directory:

      .. raw:: html

         <div id="jd0e35" class="example" dir="ltr">

      ::

         mkdir images 
         cd images

      .. raw:: html

         </div>

   2. Retrieve the overcloud images from either the RDO project or from
      Red Hat.

      -  TripleO

         .. raw:: html

            <div id="jd0e47" class="example" dir="ltr">

         ::

            curl -O https://images.rdoproject.org/queens/rdo_trunk/current-tripleo-rdo/ironic-python-agent.tar 
            curl -O https://images.rdoproject.org/queens/rdo_trunk/current-tripleo-rdo/overcloud-full.tar 
            tar xvf ironic-python-agent.tar 
            tar xvf overcloud-full.tar

         .. raw:: html

            </div>

      -  OSP13

         .. raw:: html

            <div id="jd0e59" class="example" dir="ltr">

         ::

            sudo yum install -y rhosp-director-images rhosp-director-images-ipa 
            for i in /usr/share/rhosp-director-images/overcloud-full-latest-13.0.tar /usr/share/rhosp-director-images/ironic-python-agent-latest-13.0.tar ; do tar -xvf $i; done

         .. raw:: html

            </div>

   3. Upload the overcloud images:

      .. raw:: html

         <div id="jd0e65" class="example" dir="ltr">

      ::

         cd 
         openstack overcloud image upload --image-path /home/stack/images/

      .. raw:: html

         </div>

3. Prepare OpenStack’s bare metal provisioning (Ironic).

   Ironic is an integrated OpenStack program that provisions bare metal
   machines instead of virtual machines. It is best thought of as a bare
   metal hypervisor API and a set of plugins that interact with the bare
   metal hypervisors.

   **Note**

   Make sure to combine the ``ironic_list`` files from the three
   overcloud KVM hosts.

   1. Add the overcloud VMs to Ironic:

      .. raw:: html

         <div id="jd0e85" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         ipmi_password=<password>
         ipmi_user=<user>
         while IFS= read -r line; do
           mac=`echo $line|awk '{print $1}'`
           name=`echo $line|awk '{print $2}'`
           kvm_ip=`echo $line|awk '{print $3}'`
           profile=`echo $line|awk '{print $4}'`
           ipmi_port=`echo $line|awk '{print $5}'`
           uuid=`openstack baremetal node create --driver ipmi \
                                                 --property cpus=4 \
                                                 --property memory_mb=16348 \
                                                 --property local_gb=100 \
                                                 --property cpu_arch=x86_64 \
                                                 --driver-info ipmi_username=${ipmi_user}  \
                                                 --driver-info ipmi_address=${kvm_ip} \
                                                 --driver-info ipmi_password=${ipmi_password} \
                                                 --driver-info ipmi_port=${ipmi_port} \
                                                 --name=${name} \
                                                 --property capabilities=profile:${profile},boot_option:local \
                                                 -c uuid -f value`
           openstack baremetal port create --node ${uuid} ${mac}
         done < <(cat ironic_list)

         DEPLOY_KERNEL=$(openstack image show bm-deploy-kernel -f value -c id)
         DEPLOY_RAMDISK=$(openstack image show bm-deploy-ramdisk -f value -c id)

         for i in `openstack baremetal node list -c UUID -f value`; do
           openstack baremetal node set $i --driver-info deploy_kernel=$DEPLOY_KERNEL --driver-info deploy_ramdisk=$DEPLOY_RAMDISK
         done

         for i in `openstack baremetal node list -c UUID -f value`; do
           openstack baremetal node show $i -c properties -f value
         done

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   2. Introspect the overcloud node:

      .. raw:: html

         <div id="jd0e91" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         for node in $(openstack baremetal node list -c UUID -f value) ; do
           openstack baremetal node manage $node
         done
         openstack overcloud node introspect --all-manageable --provide

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   3. Add Baremetal Server (BMS) to Ironic.

      -  Create rules for automated profiling.

         Evaluate the attributes of the physical server. The server will
         automatically be profiled based on the rules.

         The following example shows how to create a rule for system
         manufacturer as “Supermicro” and memory greater or equal to 128
         GB.

         .. raw:: html

            <div id="jd0e105" class="sample" dir="ltr">

         .. raw:: html

            <div class="output" dir="ltr">

         ::

            cat << EOF > ~/rule_compute.json
            [
             {
                 "description": "set physical compute",
                 "conditions": [
                     {"op": "eq", "field": "data://auto_discovered", "value": true},
                     {"op": "eq", "field": "data://inventory.system_vendor.manufacturer",
                      "value": "Supermicro"},
                     {"op": "ge", "field": "memory_mb", "value": 128000}
                 ],
                 "actions": [
                     {"action": "set-attribute", "path": "driver_info/ipmi_username",
                      "value": "<user>"},
                     {"action": "set-attribute", "path": "driver_info/ipmi_password",
                      "value": "<password>"},
                     {"action": "set-capability", "name": "profile", "value": "compute"},
                     {"action": "set-attribute", "path": "driver_info/ipmi_address","value": "{data[inventory][bmc_address]}"}
                 ]
             }
            ]
            EOF

         .. raw:: html

            </div>

         .. raw:: html

            </div>

         You can import the rule by:

         .. raw:: html

            <div id="jd0e110" class="sample" dir="ltr">

         .. raw:: html

            <div class="output" dir="ltr">

         ::

            openstack baremetal introspection rule import ~/rule_compute.json

         .. raw:: html

            </div>

         .. raw:: html

            </div>

      -  Scan the BMC IP range and automatically add new servers
         matching the above rule by:

         .. raw:: html

            <div id="jd0e116" class="sample" dir="ltr">

         .. raw:: html

            <div class="output" dir="ltr">

         ::

            ipmi_range=10.87.122.25/32
            ipmi_password=<password>
            ipmi_user=<user>
            openstack overcloud node discover --range ${ipmi_range} \
              --credentials ${ipmi_user}:${ipmi_password} \
              --introspect --provide

         .. raw:: html

            </div>

         .. raw:: html

            </div>

4. Create Flavor:

   .. raw:: html

      <div id="jd0e122" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      for i in compute-dpdk \
      compute-sriov \
      contrail-controller \
      contrail-analytics \
      contrail-database \
      contrail-analytics-database; do
        openstack flavor create $i --ram 4096 --vcpus 1 --disk 40
        openstack flavor set --property "capabilities:boot_option"="local" \
                             --property "capabilities:profile"="${i}" ${i}
      done

   .. raw:: html

      </div>

   .. raw:: html

      </div>

5. Copy the TripleO heat templates.

   .. raw:: html

      <div id="jd0e128" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      cp -r /usr/share/openstack-tripleo-heat-templates/ tripleo-heat-templates

   .. raw:: html

      </div>

   .. raw:: html

      </div>

6. Download and copy the Contrail heat templates from
   https://support.juniper.net/support/downloads.

   .. raw:: html

      <div id="jd0e137" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      tar -xzvf contrail-tripleo-heat-templates-<version>.tgz
      cp -r contrail-tripleo-heat-templates/* tripleo-heat-templates/

   .. raw:: html

      </div>

   .. raw:: html

      </div>

7. Create and upload the OpenStack containers.

   1. Create the OpenStack container file.

      **Note**

      The container must be created based on the OpenStack program.

      -  TripleO

         .. raw:: html

            <div id="jd0e154" class="sample" dir="ltr">

         .. raw:: html

            <div class="output" dir="ltr">

         ::

            openstack overcloud container image prepare \
              --namespace docker.io/tripleoqueens \
              --tag current-tripleo \
              --tag-from-label rdo_version \
              --output-env-file=~/overcloud_images.yaml

            tag=`grep "docker.io/tripleoqueens" docker_registry.yaml |tail -1 |awk -F":" '{print $3}'`

            openstack overcloud container image prepare \
              --namespace docker.io/tripleoqueens \
              --tag ${tag} \
              --push-destination 192.168.24.1:8787 \
              --output-env-file=~/overcloud_images.yaml \
              --output-images-file=~/local_registry_images.yaml

         .. raw:: html

            </div>

         .. raw:: html

            </div>

      -  OSP13

         .. raw:: html

            <div id="jd0e160" class="sample" dir="ltr">

         .. raw:: html

            <div class="output" dir="ltr">

         ::

            openstack overcloud container image prepare \
             --push-destination=192.168.24.1:8787  \
             --tag-from-label {version}-{release} \
             --output-images-file ~/local_registry_images.yaml  \
             --namespace=registry.access.Red Hat.com/rhosp13  \
             --prefix=openstack-  \
             --tag-from-label {version}-{release}  \
             --output-env-file ~/overcloud_images.yaml

         .. raw:: html

            </div>

         .. raw:: html

            </div>

   2. Upload the OpenStack containers:

      .. raw:: html

         <div id="jd0e166" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         openstack overcloud container image upload --config-file ~/local_registry_images.yaml

      .. raw:: html

         </div>

      .. raw:: html

         </div>

8. Create and upload the Contrail containers.

   1. Create the Contrail container file.

      **Note**

      This step is optional. The Contrail containers can be downloaded
      from external registries later.

      .. raw:: html

         <div id="jd0e179" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         cd ~/tripleo-heat-templates/tools/contrail
         ./import_contrail_container.sh -f container_outputfile -r registry -t tag [-i insecure] [-u username] [-p password] [-c certificate pat

      .. raw:: html

         </div>

      .. raw:: html

         </div>

      Here are few examples of importing Contrail containers from
      different sources:

      -  Import from password protected public registry:

         .. raw:: html

            <div id="jd0e188" class="sample" dir="ltr">

         .. raw:: html

            <div class="output" dir="ltr">

         ::

            ./import_contrail_container.sh -f /tmp/contrail_container -r hub.juniper.net/contrail -u USERNAME -p PASSWORD -t 1234

         .. raw:: html

            </div>

         .. raw:: html

            </div>

      -  Import from Dockerhub:

         .. raw:: html

            <div id="jd0e194" class="sample" dir="ltr">

         .. raw:: html

            <div class="output" dir="ltr">

         ::

            ./import_contrail_container.sh -f /tmp/contrail_container -r docker.io/opencontrailnightly -t 1234

         .. raw:: html

            </div>

         .. raw:: html

            </div>

      -  Import from private secure registry:

         .. raw:: html

            <div id="jd0e200" class="sample" dir="ltr">

         .. raw:: html

            <div class="output" dir="ltr">

         ::

            ./import_contrail_container.sh -f /tmp/contrail_container -r device.example.net:5443 -c http://device.example.net/pub/device.example.net.crt -t 1234

         .. raw:: html

            </div>

         .. raw:: html

            </div>

      -  Import from private insecure registry:

         .. raw:: html

            <div id="jd0e206" class="sample" dir="ltr">

         .. raw:: html

            <div class="output" dir="ltr">

         ::

            ./import_contrail_container.sh -f /tmp/contrail_container -r 10.0.0.1:5443 -i 1 -t 1234

         .. raw:: html

            </div>

         .. raw:: html

            </div>

   2. Upload Contrail containers to the undercloud registry:

      .. raw:: html

         <div id="jd0e212" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         openstack overcloud container image upload --config-file /tmp/contrail_container

      .. raw:: html

         </div>

      .. raw:: html

         </div>

.. _customizing-the-contrail-service-with-templates-contrail-servicesyaml:

Customizing the Contrail Service with Templates (contrail-services.yaml)
------------------------------------------------------------------------

This section contains information to customize Contrail services for
your network by modifying the ``contrail-services.yaml`` file.

-  Contrail Services customization

   .. raw:: html

      <div id="jd0e229" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      vi ~/tripleo-heat-templates/environments/contrail-services.yaml

   .. raw:: html

      </div>

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      parameter_defaults:
        ContrailSettings:
          VROUTER_GATEWAY: 10.0.0.1
          # KEY1: value1
          # KEY2: value2

          VXLAN_VN_ID_MODE: "configured"
          ENCAP_PRIORITY: "VXLAN,MPLSoUDP,MPLSoGRE"
          
        ContrailControllerParameters:
          AAAMode: rbac

   .. raw:: html

      </div>

   .. raw:: html

      </div>

-  Contrail registry settings

   .. raw:: html

      <div id="jd0e237" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      vi ~/tripleo-heat-templates/environments/contrail-services.yaml

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   Here are few examples of default values for various registries:

   -  Public Juniper registry

      .. raw:: html

         <div id="jd0e246" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         parameter_defaults:
           ContrailRegistry: hub.juniper.net/contrail
           ContrailRegistryUser: <USER>
           ContrailRegistryPassword: <PASSWORD>

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   -  Insecure registry

      .. raw:: html

         <div id="jd0e252" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         parameter_defaults:
           ContrailRegistryInsecure: true
           DockerInsecureRegistryAddress: 10.87.64.32:5000,192.168.24.1:8787
           ContrailRegistry: 10.87.64.32:5000

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   -  Private secure registry

      .. raw:: html

         <div id="jd0e258" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         parameter_defaults:
           ContrailRegistryCertUrl: http://device.example.net/pub/device.example.net.crt
           ContrailRegistry: device.example.net:5443

      .. raw:: html

         </div>

      .. raw:: html

         </div>

-  Contrail Container image settings

   .. raw:: html

      <div id="jd0e264" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      parameter_defaults:
        ContrailImageTag: queens-5.0-104-rhel-queens

   .. raw:: html

      </div>

   .. raw:: html

      </div>

.. raw:: html

   <div id="id-customizing-the-contrail-network-with-templates">

Customizing the Contrail Network with Templates
-----------------------------------------------

-  `Overview <setting-up-contrail-rhosp-overcloud.html#id-overview>`__

-  `Roles Configuration
   (roles_data_contrail_aio.yaml) <setting-up-contrail-rhosp-overcloud.html#id-roles-configuration-rolesdatacontrailaioyaml>`__

-  `Network Parameter Configuration
   (contrail-net.yaml) <setting-up-contrail-rhosp-overcloud.html#id-network-parameter-configuration-contrailnetyaml>`__

-  `Network Interface Configuration
   (*-NIC-*.yaml) <setting-up-contrail-rhosp-overcloud.html#id-network-interface-configuration-nicyaml>`__

-  `Advanced vRouter Kernel Mode
   Configuration <setting-up-contrail-rhosp-overcloud.html#id-advanced-vrouter-kernel-mode-configuration>`__

-  `Advanced vRouter DPDK Mode
   Configuration <setting-up-contrail-rhosp-overcloud.html#id-advanced-vrouter-dpdk-mode-configuration>`__

-  `Advanced vRouter SRIOV + Kernel Mode
   Configuration <setting-up-contrail-rhosp-overcloud.html#id-advanced-vrouter-sriov-kernel-mode-configuration>`__

-  `Advanced vRouter SRIOV + DPDK Mode
   Configuration <setting-up-contrail-rhosp-overcloud.html#id-advanced-vrouter-sriov-dpdk-mode-configuration>`__

-  `Advanced
   Scenarios <setting-up-contrail-rhosp-overcloud.html#id-advanced-scenarios>`__

Overview
~~~~~~~~

In order to customize the network, define different networks and
configure the overcloud nodes NIC layout. TripleO supports a flexible
way of customizing the network.

The following networking customization example uses network as:

Table 1: Network Customization

============ ==== ========================
Network      VLAN overcloud Nodes
============ ==== ========================
provisioning -    All
internal_api 710  All
external_api 720  OpenStack CTRL
storage      740  OpenStack CTRL, Computes
storage_mgmt 750  OpenStack CTRL
tenant       -    Contrail CTRL, Computes
============ ==== ========================

.. _roles-configuration-roles_data_contrail_aioyaml:

Roles Configuration (roles_data_contrail_aio.yaml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The networks must be activated per role in the roles_data file:

.. raw:: html

   <div id="jd0e367" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   vi ~/tripleo-heat-templates/roles_data_contrail_aio.yaml

.. raw:: html

   </div>

.. raw:: html

   </div>

-  `OpenStack
   Controller <setting-up-contrail-rhosp-overcloud.html#jd0e372>`__

-  `Compute Node <setting-up-contrail-rhosp-overcloud.html#jd0e378>`__

-  `Contrail
   Controller <setting-up-contrail-rhosp-overcloud.html#jd0e384>`__

-  `Compute DPDK <setting-up-contrail-rhosp-overcloud.html#jd0e390>`__

-  `Compute SRIOV <setting-up-contrail-rhosp-overcloud.html#jd0e396>`__

-  `Compute CSN <setting-up-contrail-rhosp-overcloud.html#jd0e402>`__

OpenStack Controller
^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e375" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   ###############################################################################
   # Role: Controller                                                            #
   ###############################################################################
   - name: Controller
     description: |
       Controller role that has all the controler services loaded and handles
       Database, Messaging and Network functions.
     CountDefault: 1
     tags:
       - primary
       - controller
     networks:
       - External
       - InternalApi
       - Storage
       - StorageMgmt

.. raw:: html

   </div>

.. raw:: html

   </div>

Compute Node
^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e381" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   ###############################################################################
   # Role: Compute                                                               #
   ###############################################################################
   - name: Compute
     description: |
       Basic Compute Node role
     CountDefault: 1
     networks:
       - InternalApi
       - Tenant
       - Storage

.. raw:: html

   </div>

.. raw:: html

   </div>

Contrail Controller
^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e387" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   ###############################################################################
   # Role: ContrailController                                                    #
   ###############################################################################
   - name: ContrailController
     description: |
       ContrailController role that has all the Contrail controler services loaded
       and handles config, control and webui functions
     CountDefault: 1
     tags:
       - primary
       - contrailcontroller
     networks:
       - InternalApi
       - Tenant

.. raw:: html

   </div>

.. raw:: html

   </div>

Compute DPDK
^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e393" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   ###############################################################################
   # Role: ContrailDpdk                                                          #
   ###############################################################################
   - name: ContrailDpdk
     description: |
       Contrail Dpdk Node role
     CountDefault: 0
     tags:
       - contraildpdk
     networks:
       - InternalApi
       - Tenant
       - Storage

.. raw:: html

   </div>

.. raw:: html

   </div>

Compute SRIOV
^^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e399" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   ###############################################################################
   # Role: ContrailSriov
   ###############################################################################
   - name: ContrailSriov
     description: |
       Contrail Sriov Node role
     CountDefault: 0
     tags:
       - contrailsriov
     networks:
       - InternalApi
       - Tenant
       - Storage

.. raw:: html

   </div>

.. raw:: html

   </div>

Compute CSN
^^^^^^^^^^^

.. raw:: html

   <div id="jd0e405" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   ###############################################################################
   # Role: ContrailTsn
   ###############################################################################
   - name: ContrailTsn
     description: |
       Contrail Tsn Node role
     CountDefault: 0
     tags:
       - contrailtsn
     networks:
       - InternalApi
       - Tenant
       - Storage

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _network-parameter-configuration-contrail-netyaml:

Network Parameter Configuration (contrail-net.yaml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <div id="jd0e413" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   cat ~/tripleo-heat-templates/environments/contrail/contrail-net.yaml

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   resource_registry:
     OS::TripleO::Controller::Net::SoftwareConfig: ../../network/config/contrail/controller-nic-config.yaml
     OS::TripleO::ContrailController::Net::SoftwareConfig: ../../network/config/contrail/contrail-controller-nic-config.yaml
     OS::TripleO::ContrailControlOnly::Net::SoftwareConfig: ../../network/config/contrail/contrail-controller-nic-config.yaml
     OS::TripleO::Compute::Net::SoftwareConfig: ../../network/config/contrail/compute-nic-config.yaml
     OS::TripleO::ContrailDpdk::Net::SoftwareConfig: ../../network/config/contrail/contrail-dpdk-nic-config.yaml
     OS::TripleO::ContrailSriov::Net::SoftwareConfig: ../../network/config/contrail/contrail-sriov-nic-config.yaml
     OS::TripleO::ContrailTsn::Net::SoftwareConfig: ../../network/config/contrail/contrail-tsn-nic-config.yaml

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   parameter_defaults:
     # Customize all these values to match the local environment
     TenantNetCidr: 10.0.0.0/24
     InternalApiNetCidr: 10.1.0.0/24
     ExternalNetCidr: 10.2.0.0/24
     StorageNetCidr: 10.3.0.0/24
     StorageMgmtNetCidr: 10.4.0.0/24
     # CIDR subnet mask length for provisioning network
     ControlPlaneSubnetCidr: '24'
     # Allocation pools
     TenantAllocationPools: [{'start': '10.0.0.10', 'end': '10.0.0.200'}]
     InternalApiAllocationPools: [{'start': '10.1.0.10', 'end': '10.1.0.200'}]
     ExternalAllocationPools: [{'start': '10.2.0.10', 'end': '10.2.0.200'}]
     StorageAllocationPools: [{'start': '10.3.0.10', 'end': '10.3.0.200'}]
     StorageMgmtAllocationPools: [{'start': '10.4.0.10', 'end': '10.4.0.200'}]
     # Routes
     ControlPlaneDefaultRoute: 192.168.24.1
     InternalApiDefaultRoute: 10.1.0.1
     ExternalInterfaceDefaultRoute: 10.2.0.1
     # Vlans
     InternalApiNetworkVlanID: 710
     ExternalNetworkVlanID: 720
     StorageNetworkVlanID: 730
     StorageMgmtNetworkVlanID: 740
     TenantNetworkVlanID: 3211
     # Services
     EC2MetadataIp: 192.168.24.1  # Generally the IP of the undercloud
     DnsServers: ["172.x.x.x"]
     NtpServer: 10.0.0.1

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _network-interface-configuration--nic-yaml:

Network Interface Configuration (*-NIC-*.yaml)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NIC configuration files exist per role in the following directory:

.. raw:: html

   <div id="jd0e429" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   cd ~/tripleo-heat-templates/network/config/contrail

.. raw:: html

   </div>

.. raw:: html

   </div>

-  `OpenStack
   Controller <setting-up-contrail-rhosp-overcloud.html#jd0e434>`__

-  `Contrail
   Controller <setting-up-contrail-rhosp-overcloud.html#jd0e449>`__

-  `Compute Node <setting-up-contrail-rhosp-overcloud.html#jd0e467>`__

.. _openstack-controller-1:

OpenStack Controller
^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e437" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   heat_template_version: queens

   description: >
     Software Config to drive os-net-config to configure multiple interfaces
     for the compute role. This is an example for a Nova compute node using
     Contrail vrouter and the vhost0 interface.

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   parameters:
     ControlPlaneIp:
       default: ''
       description: IP address/subnet on the ctlplane network
       type: string
     ExternalIpSubnet:
       default: ''
       description: IP address/subnet on the external network
       type: string
     InternalApiIpSubnet:
       default: ''
       description: IP address/subnet on the internal_api network
       type: string
     InternalApiDefaultRoute: # Not used by default in this template
       default: '10.0.0.1'
       description: The default route of the internal api network.
       type: string
     StorageIpSubnet:
       default: ''
       description: IP address/subnet on the storage network
       type: string
     StorageMgmtIpSubnet:
       default: ''
       description: IP address/subnet on the storage_mgmt network
       type: string
     TenantIpSubnet:
       default: ''
       description: IP address/subnet on the tenant network
       type: string
     ManagementIpSubnet: # Only populated when including environments/network-management.yaml
       default: ''
       description: IP address/subnet on the management network
       type: string
     ExternalNetworkVlanID:
       default: 10
       description: Vlan ID for the external network traffic.
       type: number
     InternalApiNetworkVlanID:
       default: 20
       description: Vlan ID for the internal_api network traffic.
       type: number
     StorageNetworkVlanID:
       default: 30
       description: Vlan ID for the storage network traffic.
       type: number
     StorageMgmtNetworkVlanID:
       default: 40
       description: Vlan ID for the storage mgmt network traffic.
       type: number
     TenantNetworkVlanID:
       default: 50
       description: Vlan ID for the tenant network traffic.
       type: number
     ManagementNetworkVlanID:
       default: 60
       description: Vlan ID for the management network traffic.
       type: number
     ControlPlaneSubnetCidr: # Override this via parameter_defaults
       default: '24'
       description: The subnet CIDR of the control plane network.
       type: string
     ControlPlaneDefaultRoute: # Override this via parameter_defaults
       description: The default route of the control plane network.
       type: string
     ExternalInterfaceDefaultRoute: # Not used by default in this template
       default: '10.0.0.1'
       description: The default route of the external network.
       type: string
     ManagementInterfaceDefaultRoute: # Commented out by default in this template
       default: unset
       description: The default route of the management network.
       type: string
     DnsServers: # Override this via parameter_defaults
       default: []
       description: A list of DNS servers (2 max for some implementations) that will be added to resolv.conf.
       type: comma_delimited_list
     EC2MetadataIp: # Override this via parameter_defaults
       description: The IP address of the EC2 metadata server.
       type: string

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   resources:
     OsNetConfigImpl:
       type: OS::Heat::SoftwareConfig
       properties:
         group: script
         config:
           str_replace:
             template:
               get_file: ../../scripts/run-os-net-config.sh
             params:
               $network_config:
                 network_config:
                 - type: interface
                   name: nic1
                   use_dhcp: false
                   dns_servers:
                     get_param: DnsServers
                   addresses:
                   - ip_netmask:
                       list_join:
                         - '/'
                         - - get_param: ControlPlaneIp
                           - get_param: ControlPlaneSubnetCidr
                   routes:
                   - ip_netmask: 169.x.x.x/32
                     next_hop:
                       get_param: EC2MetadataIp
                   - default: true
                     next_hop:
                       get_param: ControlPlaneDefaultRoute
                 - type: vlan
                   vlan_id:
                     get_param: InternalApiNetworkVlanID
                   device: nic1
                   addresses:
                   - ip_netmask:
                       get_param: InternalApiIpSubnet
                 - type: vlan
                   vlan_id:
                     get_param: ExternalNetworkVlanID
                   device: nic1
                   addresses:
                   - ip_netmask:
                       get_param: ExternalIpSubnet
                 - type: vlan
                   vlan_id:
                     get_param: StorageNetworkVlanID
                   device: nic1
                   addresses:
                   - ip_netmask:
                       get_param: StorageIpSubnet
                 - type: vlan
                   vlan_id:
                     get_param: StorageMgmtNetworkVlanID
                   device: nic1
                   addresses:
                   - ip_netmask:
                       get_param: StorageMgmtIpSubnet

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   outputs:
     OS::stack_id:
       description: The OsNetConfigImpl resource.
       value:
         get_resource: OsNetConfigImpl

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _contrail-controller-1:

Contrail Controller
^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e452" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   heat_template_version: queens

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   description: >
     Software Config to drive os-net-config to configure multiple interfaces
     for the compute role. This is an example for a Nova compute node using
     Contrail vrouter and the vhost0 interface.

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   parameters:
     ControlPlaneIp:
       default: ''
       description: IP address/subnet on the ctlplane network
       type: string
     ExternalIpSubnet:
       default: ''
       description: IP address/subnet on the external network
       type: string
     InternalApiIpSubnet:
       default: ''
       description: IP address/subnet on the internal_api network
       type: string
     InternalApiDefaultRoute: # Not used by default in this template
       default: '10.0.0.1'
       description: The default route of the internal api network.
       type: string
     StorageIpSubnet:
       default: ''
       description: IP address/subnet on the storage network
       type: string
     StorageMgmtIpSubnet:
       default: ''
       description: IP address/subnet on the storage_mgmt network
       type: string
     TenantIpSubnet:
       default: ''
       description: IP address/subnet on the tenant network
       type: string
     ManagementIpSubnet: # Only populated when including environments/network-management.yaml
       default: ''
       description: IP address/subnet on the management network
       type: string
     ExternalNetworkVlanID:
       default: 10
       description: Vlan ID for the external network traffic.
       type: number
     InternalApiNetworkVlanID:
       default: 20
       description: Vlan ID for the internal_api network traffic.
       type: number
     StorageNetworkVlanID:
       default: 30
       description: Vlan ID for the storage network traffic.
       type: number
     StorageMgmtNetworkVlanID:
       default: 40
       description: Vlan ID for the storage mgmt network traffic.
       type: number
     TenantNetworkVlanID:
       default: 50
       description: Vlan ID for the tenant network traffic.
       type: number
     ManagementNetworkVlanID:
       default: 60
       description: Vlan ID for the management network traffic.
       type: number
     ControlPlaneSubnetCidr: # Override this via parameter_defaults
       default: '24'
       description: The subnet CIDR of the control plane network.
       type: string
     ControlPlaneDefaultRoute: # Override this via parameter_defaults
       description: The default route of the control plane network.
       type: string
     ExternalInterfaceDefaultRoute: # Not used by default in this template
       default: '10.0.0.1'
       description: The default route of the external network.
       type: string
     ManagementInterfaceDefaultRoute: # Commented out by default in this template
       default: unset
       description: The default route of the management network.
       type: string
     DnsServers: # Override this via parameter_defaults
       default: []
       description: A list of DNS servers (2 max for some implementations) that will be added to resolv.conf.
       type: comma_delimited_list
     EC2MetadataIp: # Override this via parameter_defaults
       description: The IP address of the EC2 metadata server.
       type: string

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   resources:
     OsNetConfigImpl:
       type: OS::Heat::SoftwareConfig
       properties:
         group: script
         config:
           str_replace:
             template:
               get_file: ../../scripts/run-os-net-config.sh
             params:
               $network_config:
                 network_config:
                 - type: interface
                   name: nic1
                   use_dhcp: false
                   dns_servers:
                     get_param: DnsServers
                   addresses:
                   - ip_netmask:
                       list_join:
                         - '/'
                         - - get_param: ControlPlaneIp
                           - get_param: ControlPlaneSubnetCidr
                   routes:
                   - ip_netmask: 169.x.x.x/32
                     next_hop:
                       get_param: EC2MetadataIp
                   - default: true
                     next_hop:
                       get_param: ControlPlaneDefaultRoute
                 - type: vlan
                   vlan_id:
                     get_param: InternalApiNetworkVlanID
                   device: nic1
                   addresses:
                   - ip_netmask:
                       get_param: InternalApiIpSubnet
                 - type: interface
                   name: nic2
                   use_dhcp: false
                   addresses:
                   - ip_netmask:
                       get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   outputs:
     OS::stack_id:
       description: The OsNetConfigImpl resource.
       value:
         get_resource: OsNetConfigImpl

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _compute-node-1:

Compute Node
^^^^^^^^^^^^

.. raw:: html

   <div id="jd0e470" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   heat_template_version: queens

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   description: >
     Software Config to drive os-net-config to configure multiple interfaces
     for the compute role. This is an example for a Nova compute node using
     Contrail vrouter and the vhost0 interface.

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   parameters:
     ControlPlaneIp:
       default: ''
       description: IP address/subnet on the ctlplane network
       type: string
     ExternalIpSubnet:
       default: ''
       description: IP address/subnet on the external network
       type: string
     InternalApiIpSubnet:
       default: ''
       description: IP address/subnet on the internal_api network
       type: string
     InternalApiDefaultRoute: # Not used by default in this template
       default: '10.0.0.1'
       description: The default route of the internal api network.
       type: string
     StorageIpSubnet:
       default: ''
       description: IP address/subnet on the storage network
       type: string
     StorageMgmtIpSubnet:
       default: ''
       description: IP address/subnet on the storage_mgmt network
       type: string
     TenantIpSubnet:
       default: ''
       description: IP address/subnet on the tenant network
       type: string
     ManagementIpSubnet: # Only populated when including environments/network-management.yaml
       default: ''
       description: IP address/subnet on the management network
       type: string
     ExternalNetworkVlanID:
       default: 10
       description: Vlan ID for the external network traffic.
       type: number
     InternalApiNetworkVlanID:
       default: 20
       description: Vlan ID for the internal_api network traffic.
       type: number
     StorageNetworkVlanID:
       default: 30
       description: Vlan ID for the storage network traffic.
       type: number
     StorageMgmtNetworkVlanID:
       default: 40
       description: Vlan ID for the storage mgmt network traffic.
       type: number
     TenantNetworkVlanID:
       default: 50
       description: Vlan ID for the tenant network traffic.
       type: number
     ManagementNetworkVlanID:
       default: 60
       description: Vlan ID for the management network traffic.
       type: number
     ControlPlaneSubnetCidr: # Override this via parameter_defaults
       default: '24'
       description: The subnet CIDR of the control plane network.
       type: string
     ControlPlaneDefaultRoute: # Override this via parameter_defaults
       description: The default route of the control plane network.
       type: string
     ExternalInterfaceDefaultRoute: # Not used by default in this template
       default: '10.0.0.1'
       description: The default route of the external network.
       type: string
     ManagementInterfaceDefaultRoute: # Commented out by default in this template
       default: unset
       description: The default route of the management network.
       type: string
     DnsServers: # Override this via parameter_defaults
       default: []
       description: A list of DNS servers (2 max for some implementations) that will be added to resolv.conf.
       type: comma_delimited_list
     EC2MetadataIp: # Override this via parameter_defaults
       description: The IP address of the EC2 metadata server.
       type: string

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   resources:
     OsNetConfigImpl:
       type: OS::Heat::SoftwareConfig
       properties:
         group: script
         config:
           str_replace:
             template:
               get_file: ../../scripts/run-os-net-config.sh
             params:
               $network_config:
                 network_config:
                 - type: interface
                   name: nic1
                   use_dhcp: false
                   dns_servers:
                     get_param: DnsServers
                   addresses:
                   - ip_netmask:
                       list_join:
                         - '/'
                         - - get_param: ControlPlaneIp
                           - get_param: ControlPlaneSubnetCidr
                   routes:
                   - ip_netmask: 169.x.x.x/32
                     next_hop:
                       get_param: EC2MetadataIp
                   - default: true
                     next_hop:
                       get_param: ControlPlaneDefaultRoute
                 - type: vlan
                   vlan_id:
                     get_param: InternalApiNetworkVlanID
                   device: nic1
                   addresses:
                   - ip_netmask:
                       get_param: InternalApiIpSubnet
                 - type: vlan
                   vlan_id:
                     get_param: StorageNetworkVlanID
                   device: nic1
                   addresses:
                   - ip_netmask:
                       get_param: StorageIpSubnet
                 - type: contrail_vrouter
                   name: vhost0
                   use_dhcp: false
                   members:
                     -
                       type: interface
                       name: nic2
                       use_dhcp: false
                   addresses:
                   - ip_netmask:
                       get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   <div class="output" dir="ltr">

::

   outputs:
     OS::stack_id:
       description: The OsNetConfigImpl resource.
       value:
         get_resource: OsNetConfigImpl

.. raw:: html

   </div>

.. raw:: html

   </div>

Advanced vRouter Kernel Mode Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the standard NIC configuration, the vRouter kernel mode
supports VLAN, Bond, and Bond + VLAN modes. The configuration snippets
below only show the relevant section of the NIC template configuration
for each mode.

-  `VLAN <setting-up-contrail-rhosp-overcloud.html#jd0e494>`__

-  `Bond <setting-up-contrail-rhosp-overcloud.html#jd0e500>`__

-  `Bond + VLAN <setting-up-contrail-rhosp-overcloud.html#jd0e506>`__

VLAN
^^^^

.. raw:: html

   <div id="jd0e497" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: vlan
     vlan_id:
       get_param: TenantNetworkVlanID
     device: nic2
   - type: contrail_vrouter
     name: vhost0
     use_dhcp: false
     members:
       -
         type: interface
         name:
           str_replace:
             template: vlanVLANID
             params:
               VLANID: {get_param: TenantNetworkVlanID}
         use_dhcp: false
     addresses:
     - ip_netmask:
         get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

Bond
^^^^

.. raw:: html

   <div id="jd0e503" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: linux_bond
     name: bond0
     bonding_options: "mode=4 xmit_hash_policy=layer2+3"
     use_dhcp: false
     members:
      -
        type: interface
        name: nic2
      -
        type: interface
        name: nic3
   - type: contrail_vrouter
     name: vhost0
     use_dhcp: false
     members:
       -
         type: interface
         name: bond0
         use_dhcp: false
     addresses:
     - ip_netmask:
         get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _bond--vlan:

Bond + VLAN
^^^^^^^^^^^

.. raw:: html

   <div id="jd0e509" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: linux_bond
     name: bond0
     bonding_options: "mode=4 xmit_hash_policy=layer2+3"
     use_dhcp: false
     members:
      -
        type: interface
        name: nic2
      -
        type: interface
        name: nic3
   - type: vlan
     vlan_id:
       get_param: TenantNetworkVlanID
     device: bond0
   - type: contrail_vrouter
     name: vhost0
     use_dhcp: false
     members:
       -
         type: interface
         name:
           str_replace:
             template: vlanVLANID
             params:
               VLANID: {get_param: TenantNetworkVlanID}
         use_dhcp: false
     addresses:
     - ip_netmask:
         get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

Advanced vRouter DPDK Mode Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the standard NIC configuration, the vRouter DPDK mode
supports Standard, VLAN, Bond, and Bond + VLAN modes.

Network Environment Configuration:

.. raw:: html

   <div id="jd0e521" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   vi ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml

.. raw:: html

   </div>

.. raw:: html

   </div>

Enable the number of hugepages:

.. raw:: html

   <div id="jd0e526" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   parameter_defaults:
     ContrailDpdkHugepages1GB: 10

.. raw:: html

   </div>

.. raw:: html

   </div>

See the following NIC template configurations for vRouter DPDK mode. The
configuration snippets below only show the relevant section of the NIC
configuration for each mode.

-  `Standard <setting-up-contrail-rhosp-overcloud.html#jd0e533>`__

-  `VLAN <setting-up-contrail-rhosp-overcloud.html#jd0e539>`__

-  `Bond <setting-up-contrail-rhosp-overcloud.html#jd0e545>`__

-  `Bond + VLAN <setting-up-contrail-rhosp-overcloud.html#jd0e551>`__

Standard
^^^^^^^^

.. raw:: html

   <div id="jd0e536" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: contrail_vrouter_dpdk
     name: vhost0
     use_dhcp: false
     driver: uio_pci_generic
     cpu_list: 0x01
     members:
       -
         type: interface
         name: nic2
         use_dhcp: false
     addresses:
     - ip_netmask:
         get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _vlan-1:

VLAN
^^^^

.. raw:: html

   <div id="jd0e542" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

    - type: contrail_vrouter_dpdk
                name: vhost0
                use_dhcp: false
                driver: uio_pci_generic
                cpu_list: 0x01
                vlan_id:
                  get_param: TenantNetworkVlanID
                members:
                  -
                    type: interface
                    name: nic2
                    use_dhcp: false
                addresses:
                - ip_netmask:
                    get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _bond-1:

Bond
^^^^

.. raw:: html

   <div id="jd0e548" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: contrail_vrouter_dpdk
                name: vhost0
                use_dhcp: false
                driver: uio_pci_generic
                cpu_list: 0x01
                bond_mode: 4
                bond_policy: layer2+3
                members:
                  -
                    type: interface
                    name: nic2
                    use_dhcp: false
                  -
                    type: interface
                    name: nic3
                    use_dhcp: false
                addresses:
                - ip_netmask:
                    get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _bond--vlan-1:

Bond + VLAN
^^^^^^^^^^^

.. raw:: html

   <div id="jd0e554" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

    - type: contrail_vrouter_dpdk
                name: vhost0
                use_dhcp: false
                driver: uio_pci_generic
                cpu_list: 0x01
                vlan_id:
                  get_param: TenantNetworkVlanID
                bond_mode: 4
                bond_policy: layer2+3
                members:
                  -
                    type: interface
                    name: nic2
                    use_dhcp: false
                  -
                    type: interface
                    name: nic3
                    use_dhcp: false
                addresses:
                - ip_netmask:
                    get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _advanced-vrouter-sriov--kernel-mode-configuration:

Advanced vRouter SRIOV + Kernel Mode Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

vRouter SRIOV + Kernel mode can be used in the following combinations:

-  Standard

-  VLAN

-  Bond

-  Bond + VLAN

Network environment configuration:

.. raw:: html

   <div id="jd0e579" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   vi ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml

.. raw:: html

   </div>

.. raw:: html

   </div>

Enable the number of hugepages:

.. raw:: html

   <div id="jd0e584" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   parameter_defaults:
     ContrailSriovHugepages1GB: 10

.. raw:: html

   </div>

.. raw:: html

   </div>

SRIOV PF/VF settings:

.. raw:: html

   <div id="jd0e589" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   NovaPCIPassthrough:
   - devname: "ens2f1"
     physical_network: "sriov1"
   ContrailSriovNumVFs: ["ens2f1:7"]

.. raw:: html

   </div>

.. raw:: html

   </div>

The SRIOV NICs are not configured in the NIC templates. However, vRouter
NICs must still be configured. See the following NIC template
configurations for vRouter kernel mode. The configuration snippets below
only show the relevant section of the NIC configuration for each mode.

-  `VLAN <setting-up-contrail-rhosp-overcloud.html#jd0e596>`__

-  `Bond <setting-up-contrail-rhosp-overcloud.html#jd0e602>`__

-  `Bond + VLAN <setting-up-contrail-rhosp-overcloud.html#jd0e608>`__

.. _vlan-2:

VLAN
^^^^

.. raw:: html

   <div id="jd0e599" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: vlan
     vlan_id:
       get_param: TenantNetworkVlanID
     device: nic2
   - type: contrail_vrouter
     name: vhost0
     use_dhcp: false
     members:
       -
         type: interface
         name:
           str_replace:
             template: vlanVLANID
             params:
               VLANID: {get_param: TenantNetworkVlanID}
         use_dhcp: false
     addresses:
     - ip_netmask:
         get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _bond-2:

Bond
^^^^

.. raw:: html

   <div id="jd0e605" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: linux_bond
     name: bond0
     bonding_options: "mode=4 xmit_hash_policy=layer2+3"
     use_dhcp: false
     members:
      -
        type: interface
        name: nic2
      -
        type: interface
        name: nic3
   - type: contrail_vrouter
     name: vhost0
     use_dhcp: false
     members:
       -
         type: interface
         name: bond0
         use_dhcp: false
     addresses:
     - ip_netmask:
         get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _bond--vlan-2:

Bond + VLAN
^^^^^^^^^^^

.. raw:: html

   <div id="jd0e611" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: linux_bond
     name: bond0
     bonding_options: "mode=4 xmit_hash_policy=layer2+3"
     use_dhcp: false
     members:
      -
        type: interface
        name: nic2
      -
        type: interface
        name: nic3
   - type: vlan
     vlan_id:
       get_param: TenantNetworkVlanID
     device: bond0
   - type: contrail_vrouter
     name: vhost0
     use_dhcp: false
     members:
       -
         type: interface
         name:
           str_replace:
             template: vlanVLANID
             params:
               VLANID: {get_param: TenantNetworkVlanID}
         use_dhcp: false
     addresses:
     - ip_netmask:
         get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _advanced-vrouter-sriov--dpdk-mode-configuration:

Advanced vRouter SRIOV + DPDK Mode Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

vRouter SRIOV + DPDK can be used in the following combinations:

-  Standard

-  VLAN

-  Bond

-  Bond + VLAN

Network environment configuration:

.. raw:: html

   <div id="jd0e636" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   vi ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml

.. raw:: html

   </div>

.. raw:: html

   </div>

Enable the number of hugepages

.. raw:: html

   <div id="jd0e641" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   parameter_defaults:
     ContrailSriovMode: dpdk
     ContrailDpdkHugepages1GB: 10
     ContrailSriovHugepages1GB: 10

.. raw:: html

   </div>

.. raw:: html

   </div>

SRIOV PF/VF settings

.. raw:: html

   <div id="jd0e646" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   NovaPCIPassthrough:
   - devname: "ens2f1"
     physical_network: "sriov1"
   ContrailSriovNumVFs: ["ens2f1:7"]

.. raw:: html

   </div>

.. raw:: html

   </div>

The SRIOV NICs are not configured in the NIC templates. However, vRouter
NICs must still be configured. See the following NIC template
configurations for vRouter DPDK mode. The configuration snippets below
only show the relevant section of the NIC configuration for each mode.

-  `Standard <setting-up-contrail-rhosp-overcloud.html#jd0e653>`__

-  `VLAN <setting-up-contrail-rhosp-overcloud.html#jd0e659>`__

-  `Bond <setting-up-contrail-rhosp-overcloud.html#jd0e665>`__

-  `Bond + VLAN <setting-up-contrail-rhosp-overcloud.html#jd0e671>`__

.. _standard-1:

Standard
^^^^^^^^

.. raw:: html

   <div id="jd0e656" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: contrail_vrouter_dpdk
     name: vhost0
     use_dhcp: false
     driver: uio_pci_generic
     cpu_list: 0x01
     members:
       -
         type: interface
         name: nic2
         use_dhcp: false
     addresses:
     - ip_netmask:
         get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _vlan-3:

VLAN
^^^^

.. raw:: html

   <div id="jd0e662" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

    - type: contrail_vrouter_dpdk
                name: vhost0
                use_dhcp: false
                driver: uio_pci_generic
                cpu_list: 0x01
                vlan_id:
                  get_param: TenantNetworkVlanID
                members:
                  -
                    type: interface
                    name: nic2
                    use_dhcp: false
                addresses:
                - ip_netmask:
                    get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _bond-3:

Bond
^^^^

.. raw:: html

   <div id="jd0e668" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   - type: contrail_vrouter_dpdk
                name: vhost0
                use_dhcp: false
                driver: uio_pci_generic
                cpu_list: 0x01
                bond_mode: 4
                bond_policy: layer2+3
                members:
                  -
                    type: interface
                    name: nic2
                    use_dhcp: false
                  -
                    type: interface
                    name: nic3
                    use_dhcp: false
                addresses:
                - ip_netmask:
                    get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

.. _bond--vlan-3:

Bond + VLAN
^^^^^^^^^^^

.. raw:: html

   <div id="jd0e674" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

    - type: contrail_vrouter_dpdk
                name: vhost0
                use_dhcp: false
                driver: uio_pci_generic
                cpu_list: 0x01
                vlan_id:
                  get_param: TenantNetworkVlanID
                bond_mode: 4
                bond_policy: layer2+3
                members:
                  -
                    type: interface
                    name: nic2
                    use_dhcp: false
                  -
                    type: interface
                    name: nic3
                    use_dhcp: false
                addresses:
                - ip_netmask:
                    get_param: TenantIpSubnet

.. raw:: html

   </div>

.. raw:: html

   </div>

Advanced Scenarios
~~~~~~~~~~~~~~~~~~

Remote Compute

Remote Compute extends the data plane to remote locations (POP) whilest
keeping the control plane central. Each POP will have its own set of
Contrail control services, which are running in the central location.
The difficulty is to ensure that the compute nodes of a given POP
connect to the Control nodes assigned to that POC. The Control nodes
must have predictable IP addresses and the compute nodes have to know
these IP addresses. In order to achieve that the following methods are
used:

-  Custom Roles

-  Static IP assignment

-  Precise Node placement

-  Per Node hieradata

Each overcloud node has a unique DMI UUID. This UUID is known on the
undercloud node as well as on the overcloud node. Hence, this UUID can
be used for mapping node specific information. For each POP, a Control
role and a Compute role has to be created.

Overview

|image1|

Mapping Table

Table 2: Mapping Table

.. raw:: html

   <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
   <colgroup>
   <col style="width: 16%" />
   <col style="width: 16%" />
   <col style="width: 16%" />
   <col style="width: 16%" />
   <col style="width: 16%" />
   <col style="width: 16%" />
   </colgroup>
   <thead>
   <tr class="header">
   <th style="text-align: left;"><p>Nova Name</p></th>
   <th style="text-align: left;"><p>Ironic Name</p></th>
   <th style="text-align: left;"><p>UUID</p></th>
   <th style="text-align: left;"><p>KVM</p></th>
   <th style="text-align: left;"><p>IP Address</p></th>
   <th style="text-align: left;"><p>POP</p></th>
   </tr>
   </thead>
   <tbody>
   <tr class="odd">
   <td style="text-align: left;"><p>overcloud<br />
   -contrailcontrolonly<br />
   -0</p></td>
   <td style="text-align: left;"><p>control-only-1-<br />
   5b3s30</p></td>
   <td style="text-align: left;"><p>Ironic UUID: 7d758dce-2784-<br />
   45fd-be09-5a41eb53e764</p>
   <br />

.. raw:: html

   <p>DMI UUID: 73F8D030-E896-<br />
   4A95-A9F5-E1A4FEBE322D</p></td>
   <td style="text-align: left;"><p>5b3s30</p></td>
   <td style="text-align: left;"><p>10.0.0.11</p></td>
   <td style="text-align: left;"><p>POP1</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p>overcloud<br />
   -contrailcontrolonly<br />
   -1</p></td>
   <td style="text-align: left;"><p>control-only-2-<br />
   5b3s30</p></td>
   <td style="text-align: left;"><p>Ironic UUID: d26abdeb-d514-<br />
   4a37-a7fb-2cd2511c351f</p>
   <br />

.. raw:: html

   <p>DMI UUID: 14639A66-D62C-<br />
   4408-82EE-FDDC4E509687</p></td>
   <td style="text-align: left;"><p>5b3s30</p></td>
   <td style="text-align: left;"><p>10.0.0.14</p></td>
   <td style="text-align: left;"><p>POP2</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p>overcloud<br />
   -contrailcontrolonly<br />
   -2</p></td>
   <td style="text-align: left;"><p>control-only-1-<br />
   5b3s31</p></td>
   <td style="text-align: left;"><p>Ironic UUID: 91dd9fa9-e8eb-<br />
   4b51-8b5e-bbaffb6640e4</p>
   <br />

.. raw:: html

   <p>DMI UUID: 28AB0B57-D612-<br />
   431E-B177-1C578AE0FEA4</p></td>
   <td style="text-align: left;"><p>5b3s31</p></td>
   <td style="text-align: left;"><p>10.0.0.12</p></td>
   <td style="text-align: left;"><p>POP1</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p>overcloud<br />
   -contrailcontrolonly<br />
   -3</p></td>
   <td style="text-align: left;"><p>control-only-2-<br />
   5b3s31</p></td>
   <td style="text-align: left;"><p>Ironic UUID: 09fa57b8-580f-<br />
   42ec-bf10-a19573521ed4</p>
   <br />

.. raw:: html

   <p>DMI UUID: 09BEC8CB-77E9-<br />
   42A6-AFF4-6D4880FD87D0</p></td>
   <td style="text-align: left;"><p>5b3s31</p></td>
   <td style="text-align: left;"><p>10.0.0.15</p></td>
   <td style="text-align: left;"><p>POP2</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p>overcloud<br />
   -contrailcontrolonly<br />
   -4</p></td>
   <td style="text-align: left;"><p>control-only-1-<br />
   5b3s32</p></td>
   <td style="text-align: left;"><p>Ironic UUID: 4766799-24c8-<br />
   4e3b-af54-353f2b796ca4</p>
   <br />

.. raw:: html

   <p>DMI UUID: 3993957A-ECBF-<br />
   4520-9F49-0AF6EE1667A7</p></td>
   <td style="text-align: left;"><p>5b3s32</p></td>
   <td style="text-align: left;"><p>10.0.0.13</p></td>
   <td style="text-align: left;"><p>POP1</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p>overcloud<br />
   -contrailcontrolonly<br />
   -5</p></td>
   <td style="text-align: left;"><p>control-only-2-<br />
   5b3s32</p></td>
   <td style="text-align: left;"><p>Ironic UUID: 58a803ae-a785-<br />
   470e-9789-139abbfa74fb</p>
   <br />

.. raw:: html

   <p>DMI UUID: AF92F485-C30C-<br />
   4D0A-BDC4-C6AE97D06A66</p></td>
   <td style="text-align: left;"><p>5b3s32</p></td>
   <td style="text-align: left;"><p>10.0.0.16</p></td>
   <td style="text-align: left;"><p>POP2</p></td>
   </tr>
   </tbody>
   </table>

ControlOnly preparation

Add ControlOnly overcloud VMs to overcloud KVM host

**Note**

This has to be done on the overcloud KVM hosts

Two ControlOnly overcloud VM definitions will be created on each of the
overcloud KVM hosts.

.. raw:: html

   <div id="jd0e940" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   ROLES=control-only:2
   num=4
   ipmi_user=<user>
   ipmi_password=<password>
   libvirt_path=/var/lib/libvirt/images
   port_group=overcloud
   prov_switch=br0

   /bin/rm ironic_list
   IFS=',' read -ra role_list <<< "${ROLES}"
   for role in ${role_list[@]}; do
     role_name=`echo $role|cut -d ":" -f 1`
     role_count=`echo $role|cut -d ":" -f 2`
     for count in `seq 1 ${role_count}`; do
       echo $role_name $count
       qemu-img create -f qcow2 ${libvirt_path}/${role_name}_${count}.qcow2 99G
       virsh define /dev/stdin <<EOF
    $(virt-install --name ${role_name}_${count} \
   --disk ${libvirt_path}/${role_name}_${count}.qcow2 \
   --vcpus=4 \
   --ram=16348 \
   --network network=br0,model=virtio,portgroup=${port_group} \
   --network network=br1,model=virtio \
   --virt-type kvm \
   --cpu host \
   --import \
   --os-variant rhel7 \
   --serial pty \
   --console pty,target_type=virtio \
   --graphics vnc \
   --print-xml)
   EOF
       vbmc add ${role_name}_${count} --port 1623${num} --username ${ipmi_user} --password ${ipmi_password}
       vbmc start ${role_name}_${count}
       prov_mac=`virsh domiflist ${role_name}_${count}|grep ${prov_switch}|awk '{print $5}'`
       vm_name=${role_name}-${count}-`hostname -s`
       kvm_ip=`ip route get 1  |grep src |awk '{print $7}'`
       echo ${prov_mac} ${vm_name} ${kvm_ip} ${role_name} 1623${num}>> ironic_list
       num=$(expr $num + 1)
     done
   done

.. raw:: html

   </div>

.. raw:: html

   </div>

**Note**

The generated *ironic_list* will be needed on the undercloud to import
the nodes to Ironic.

Get the ironic_lists from the overcloud KVM hosts and combine them.

.. raw:: html

   <div id="jd0e955" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   cat ironic_list_control_only
   52:54:00:3a:2f:ca control-only-1-5b3s30 10.87.64.31 control-only 16234
   52:54:00:31:4f:63 control-only-2-5b3s30 10.87.64.31 control-only 16235
   52:54:00:0c:11:74 control-only-1-5b3s31 10.87.64.32 control-only 16234
   52:54:00:56:ab:55 control-only-2-5b3s31 10.87.64.32 control-only 16235
   52:54:00:c1:f0:9a control-only-1-5b3s32 10.87.64.33 control-only 16234
   52:54:00:f3:ce:13 control-only-2-5b3s32 10.87.64.33 control-only 16235

.. raw:: html

   </div>

.. raw:: html

   </div>

Import:

.. raw:: html

   <div id="jd0e960" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   ipmi_password=<password>
   ipmi_user=<user>

   DEPLOY_KERNEL=$(openstack image show bm-deploy-kernel -f value -c id)
   DEPLOY_RAMDISK=$(openstack image show bm-deploy-ramdisk -f value -c id)

   num=0
   while IFS= read -r line; do
     mac=`echo $line|awk '{print $1}'`
     name=`echo $line|awk '{print $2}'`
     kvm_ip=`echo $line|awk '{print $3}'`
     profile=`echo $line|awk '{print $4}'`
     ipmi_port=`echo $line|awk '{print $5}'`
     uuid=`openstack baremetal node create --driver ipmi \
                                           --property cpus=4 \
                                           --property memory_mb=16348 \
                                           --property local_gb=100 \
                                           --property cpu_arch=x86_64 \
                                           --driver-info ipmi_username=${ipmi_user}  \
                                           --driver-info ipmi_address=${kvm_ip} \
                                           --driver-info ipmi_password=${ipmi_password} \
                                           --driver-info ipmi_port=${ipmi_port} \
                                           --name=${name} \
                                           --property capabilities=boot_option:local \
                                           -c uuid -f value`
     openstack baremetal node set ${uuid} --driver-info deploy_kernel=$DEPLOY_KERNEL --driver-info deploy_ramdisk=$DEPLOY_RAMDISK
     openstack baremetal port create --node ${uuid} ${mac}
     openstack baremetal node manage ${uuid}
     num=$(expr $num + 1)
   done < <(cat ironic_list_control_only)

.. raw:: html

   </div>

.. raw:: html

   </div>

ControlOnly node introspection

.. raw:: html

   <div id="jd0e965" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   openstack overcloud node introspect --all-manageable --provide

.. raw:: html

   </div>

.. raw:: html

   </div>

Get the ironic UUID of the ControlOnly nodes

.. raw:: html

   <div id="jd0e970" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   openstack baremetal node list |grep control-only
   | 7d758dce-2784-45fd-be09-5a41eb53e764 | control-only-1-5b3s30  | None | power off | available | False |
   | d26abdeb-d514-4a37-a7fb-2cd2511c351f | control-only-2-5b3s30  | None | power off | available | False |
   | 91dd9fa9-e8eb-4b51-8b5e-bbaffb6640e4 | control-only-1-5b3s31  | None | power off | available | False |
   | 09fa57b8-580f-42ec-bf10-a19573521ed4 | control-only-2-5b3s31  | None | power off | available | False |
   | f4766799-24c8-4e3b-af54-353f2b796ca4 | control-only-1-5b3s32  | None | power off | available | False |
   | 58a803ae-a785-470e-9789-139abbfa74fb | control-only-2-5b3s32  | None | power off | available | False |

.. raw:: html

   </div>

.. raw:: html

   </div>

The first ControlOnly node on each of the overcloud KVM hosts will be
used for POP1, the second for POP2, and so and so forth.

Get the ironic UUID of the POP compute nodes:

.. raw:: html

   <div id="jd0e977" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   openstack baremetal node list |grep compute
   | 91d6026c-b9db-49cb-a685-99a63da5d81e | compute-3-5b3s30 | None | power off | available | False |
   | 8028eb8c-e1e6-4357-8fcf-0796778bd2f7 | compute-4-5b3s30 | None | power off | available | False |
   | b795b3b9-c4e3-4a76-90af-258d9336d9fb | compute-3-5b3s31 | None | power off | available | False |
   | 2d4be83e-6fcc-4761-86f2-c2615dd15074 | compute-4-5b3s31 | None | power off | available | False |

.. raw:: html

   </div>

The first two compute nodes belong to POP1 the second two compute nodes
belong to POP2.

.. raw:: html

   </div>

Create an input YAML using the ironic UUIDs:

.. raw:: html

   <div id="jd0e984" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

    ~/subcluster_input.yaml
   ---
   - subcluster: subcluster1
     asn: "65413"
     control_nodes:
       - uuid: 7d758dce-2784-45fd-be09-5a41eb53e764
         ipaddress: 10.0.0.11
       - uuid: 91dd9fa9-e8eb-4b51-8b5e-bbaffb6640e4
         ipaddress: 10.0.0.12
       - uuid: f4766799-24c8-4e3b-af54-353f2b796ca4
         ipaddress: 10.0.0.13
     compute_nodes:
       - uuid: 91d6026c-b9db-49cb-a685-99a63da5d81e
         vrouter_gateway: 10.0.0.1
       - uuid: 8028eb8c-e1e6-4357-8fcf-0796778bd2f7
         vrouter_gateway: 10.0.0.1
   - subcluster: subcluster2
     asn: "65414"
     control_nodes:
       - uuid: d26abdeb-d514-4a37-a7fb-2cd2511c351f
         ipaddress: 10.0.0.14
       - uuid: 09fa57b8-580f-42ec-bf10-a19573521ed4
         ipaddress: 10.0.0.15
       - uuid: 58a803ae-a785-470e-9789-139abbfa74fb
         ipaddress: 10.0.0.16
     compute_nodes:
       - uuid: b795b3b9-c4e3-4a76-90af-258d9336d9fb
         vrouter_gateway: 10.0.0.1
       - uuid: 2d4be83e-6fcc-4761-86f2-c2615dd15074
         vrouter_gateway: 10.0.0.1

.. raw:: html

   </div>

.. raw:: html

   </div>

**Note**

Only control_nodes, compute_nodes, dpdk_nodes and sriov_nodes are
supported.

Generate subcluster environment:

.. raw:: html

   <div id="jd0e992" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   ~/tripleo-heat-templates/tools/contrail/create_subcluster_environment.py -i ~/subcluster_input.yaml \
                  -o ~/tripleo-heat-templates/environments/contrail/contrail-subcluster.yaml

.. raw:: html

   </div>

.. raw:: html

   </div>

Check subcluster environment file:

.. raw:: html

   <div id="jd0e997" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   cat ~/tripleo-heat-templates/environments/contrail/contrail-subcluster.yaml
   parameter_defaults:
     NodeDataLookup:
       041D7B75-6581-41B3-886E-C06847B9C87E:
         contrail_settings:
           CONTROL_NODES: 10.0.0.14,10.0.0.15,10.0.0.16
           SUBCLUSTER: subcluster2
           VROUTER_GATEWAY: 10.0.0.1
       09BEC8CB-77E9-42A6-AFF4-6D4880FD87D0:
         contrail_settings:
           BGP_ASN: '65414'
           SUBCLUSTER: subcluster2
       14639A66-D62C-4408-82EE-FDDC4E509687:
         contrail_settings:
           BGP_ASN: '65414'
           SUBCLUSTER: subcluster2
       28AB0B57-D612-431E-B177-1C578AE0FEA4:
         contrail_settings:
           BGP_ASN: '65413'
           SUBCLUSTER: subcluster1
       3993957A-ECBF-4520-9F49-0AF6EE1667A7:
         contrail_settings:
           BGP_ASN: '65413'
           SUBCLUSTER: subcluster1
       73F8D030-E896-4A95-A9F5-E1A4FEBE322D:
         contrail_settings:
           BGP_ASN: '65413'
           SUBCLUSTER: subcluster1
       7933C2D8-E61E-4752-854E-B7B18A424971:
         contrail_settings:
           CONTROL_NODES: 10.0.0.14,10.0.0.15,10.0.0.16
           SUBCLUSTER: subcluster2
           VROUTER_GATEWAY: 10.0.0.1
       AF92F485-C30C-4D0A-BDC4-C6AE97D06A66:
         contrail_settings:
           BGP_ASN: '65414'
           SUBCLUSTER: subcluster2
       BB9E9D00-57D1-410B-8B19-17A0DA581044:
         contrail_settings:
           CONTROL_NODES: 10.0.0.11,10.0.0.12,10.0.0.13
           SUBCLUSTER: subcluster1
           VROUTER_GATEWAY: 10.0.0.1
       E1A809DE-FDB2-4EB2-A91F-1B3F75B99510:
         contrail_settings:
           CONTROL_NODES: 10.0.0.11,10.0.0.12,10.0.0.13
           SUBCLUSTER: subcluster1
           VROUTER_GATEWAY: 10.0.0.1

.. raw:: html

   </div>

.. raw:: html

   </div>

Deployment

Add contrail-subcluster.yaml, contrail-ips-from-pool-all.yaml and
contrail-scheduler-hints.yaml to the OpenStack deploy command:

.. raw:: html

   <div id="jd0e1004" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   openstack overcloud deploy --templates ~/tripleo-heat-templates \
    -e ~/overcloud_images.yaml \
    -e ~/tripleo-heat-templates/environments/network-isolation.yaml \
    -e ~/tripleo-heat-templates/environments/contrail/contrail-plugins.yaml \
    -e ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml \
    -e ~/tripleo-heat-templates/environments/contrail/contrail-net.yaml \
    -e ~/tripleo-heat-templates/environments/contrail/contrail-subcluster.yaml \
    -e ~/tripleo-heat-templates/environments/contrail/contrail-ips-from-pool-all.yaml \
    -e ~/tripleo-heat-templates/environments/contrail/contrail-scheduler-hints.yaml \
    --roles-file ~/tripleo-heat-templates/roles_data_contrail_aio.yaml

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

Installing Overcloud
--------------------

1. Deployment:

   .. raw:: html

      <div id="jd0e1018" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      openstack overcloud deploy --templates ~/tripleo-heat-templates \
      -e ~/overcloud_images.yaml \
      -e ~/tripleo-heat-templates/environments/network-isolation.yaml \
      -e ~/tripleo-heat-templates/environments/contrail/contrail-plugins.yaml \
      -e ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml \
      -e ~/tripleo-heat-templates/environments/contrail/contrail-net.yaml \
      --roles-file ~/tripleo-heat-templates/roles_data_contrail_aio.yaml

   .. raw:: html

      </div>

   .. raw:: html

      </div>

2. Validation Test:

   .. raw:: html

      <div id="jd0e1024" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      source overcloudrc
      curl -O http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img
      openstack image create --container-format bare --disk-format qcow2 --file cirros-0.3.5-x86_64-disk.img cirros
      openstack flavor create --public cirros --id auto --ram 64 --disk 0 --vcpus 1
      openstack network create net1
      openstack subnet create --subnet-range 1.0.0.0/24 --network net1 sn1
      nova boot --image cirros --flavor cirros --nic net-id=`openstack network show net1 -c id -f value` --availability-zone nova:overcloud-novacompute-0.localdomain c1
      nova list

   .. raw:: html

      </div>

   .. raw:: html

      </div>

 

.. |image1| image:: documentation/images/g200478.png
