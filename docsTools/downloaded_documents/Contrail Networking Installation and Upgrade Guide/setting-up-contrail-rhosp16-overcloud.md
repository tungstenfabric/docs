# Setting Up the Overcloud

 

<div class="section tp-summary">

##### Summary

Follow this topic to setting up the overcloud for Contrail Networking
deployment with RHOSP 16.1.

</div>

## Configuring the Overcloud

Use this example procedure on the undercloud to set up the configuration
for the overcloud.

1.  <span id="jd0e23">Specify the name server to be used:</span>
    <div id="jd0e26" class="example" dir="ltr">

        undercloud_nameserver=8.8.8.8 
        openstack subnet set `openstack subnet show ctlplane-subnet -c id -f value` --dns-nameserver ${undercloud_nameserver}

    </div>

2.  <span id="jd0e31">Retrieve and upload the overcloud images.</span>
    1.  Create the image directory:

        <div id="jd0e38" class="example" dir="ltr">

            mkdir images 
            cd images

        </div>

    2.  Retrieve the overcloud images from either the RDO project or
        from Red Hat.

        OSP16

        <div id="jd0e48" class="example" dir="ltr">

            sudo yum install -y rhosp-director-images rhosp-director-images-ipa 
            for i in /usr/share/rhosp-director-images/overcloud-full-latest-16.0.tar /usr/share/rhosp-director-images/ironic-python-agent-latest-16.0.tar ; do tar -xvf $i; done

        </div>

    3.  Upload the overcloud images:

        <div id="jd0e54" class="example" dir="ltr">

            cd 
            openstack overcloud image upload --image-path /home/stack/images/

        </div>

3.  <span id="jd0e59">Prepare OpenStack’s bare metal provisioning
    (Ironic).</span>

    Ironic is an integrated OpenStack program that provisions bare metal
    machines instead of virtual machines. It is best thought of as a
    bare metal hypervisor API and a set of plugins that interact with
    the bare metal hypervisors.

    **Note**

    Make sure to combine the `ironic_list` files from the three
    overcloud KVM hosts.

    1.  Add the overcloud VMs to Ironic:

        <div id="jd0e74" class="sample" dir="ltr">

        <div class="output" dir="ltr">

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

        </div>

        </div>

    2.  Introspect the overcloud node:

        <div id="jd0e80" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            for node in $(openstack baremetal node list -c UUID -f value) ; do
              openstack baremetal node manage $node
            done
            openstack overcloud node introspect --all-manageable --provide

        </div>

        </div>

4.  <span id="jd0e83">Create Flavor:</span>
    <div id="jd0e86" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        for i in compute-dpdk \
        compute-sriov \
        contrail-controller \
        contrail-analytics \
        contrail-database \
        contrail-analytics-database; do
          openstack flavor create $i --ram 4096 --vcpus 1 --disk 40
          openstack flavor set --property "capabilities:boot_option"="local" \
                               --property "capabilities:profile"="${i}" ${i}
          openstack flavor set --property resources:CUSTOM_BAREMETAL=1 --property resources:DISK_GB='0'
                               --property resources:MEMORY_MB='0'
                               --property resources:VCPU='0' ${i}
        done

    </div>

    </div>

5.  <span id="jd0e89">Copy the TripleO heat templates.</span>
    <div id="jd0e92" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        cp -r /usr/share/openstack-tripleo-heat-templates/ tripleo-heat-templates

    </div>

    </div>

6.  <span id="jd0e95">Download and copy the Contrail heat templates from
    <https://support.juniper.net/support/downloads>.</span>
    <div id="jd0e101" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        tar -xzvf contrail-tripleo-heat-templates-<version>.tgz
        cp -r contrail-tripleo-heat-templates/* tripleo-heat-templates/

    </div>

    </div>

7.  <span id="jd0e104">Create `rhsm.yaml` file with your RedHat
    credentials</span>
    <div id="jd0e110" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        parameter_defaults:
          RhsmVars:
            rhsm_repos:
              - fast-datapath-for-rhel-8-x86_64-rpms
              - openstack-16.1-for-rhel-8-x86_64-rpms
              - satellite-tools-6.5-for-rhel-8-x86_64-rpms
              - ansible-2-for-rhel-8-x86_64-rpms
              - rhel-8-for-x86_64-highavailability-rpms
              - rhel-8-for-x86_64-appstream-rpms
              - rhel-8-for-x86_64-baseos-rpms
            rhsm_username: "YOUR_REDHAT_LOGIN"
            rhsm_password: "YOUR_REDHAT_PASSWORD"
            rhsm_org_id: "YOUR_REDHAT_ID"
            rhsm_pool_ids: "YOUR_REDHAT_POOL_ID"

    </div>

    </div>

8.  <span id="jd0e113">Create and upload the OpenStack
    containers.</span>
    1.  Create the OpenStack container file.

        **Note**

        The container must be created based on the OpenStack program.

        OSP16

        <div id="jd0e125" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            sudo openstack tripleo container image prepare \
              -e ~/containers-prepare-parameter.yaml
              -e ~/rhsm.yaml > ~/overcloud_containers.yaml

            sudo openstack overcloud container image upload --config-file ~/overcloud_containers.yaml

        </div>

        </div>

    2.  Upload the OpenStack containers:

        <div id="jd0e131" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            openstack overcloud container image upload --config-file ~/local_registry_images.yaml

        </div>

        </div>

9.  <span id="jd0e134">Create and upload the Contrail containers.</span>
    1.  Create the Contrail container file.

        **Note**

        This step is optional. The Contrail containers can be downloaded
        from external registries later.

        <div id="jd0e144" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            cd ~/tf-heat-templates/tools/contrail
            ./import_contrail_container.sh -f container_outputfile -r registry -t tag [-i insecure] [-u username] [-p password] [-c certificate path]

        </div>

        </div>

        Here are few examples of importing Contrail containers from
        different sources:

        -   Import from password protected public registry:

            <div id="jd0e153" class="sample" dir="ltr">

            <div class="output" dir="ltr">

                ./import_contrail_container.sh -f /tmp/contrail_container -r hub.juniper.net/contrail -u USERNAME -p PASSWORD -t 1234

            </div>

            </div>

        -   Import from Dockerhub:

            <div id="jd0e159" class="sample" dir="ltr">

            <div class="output" dir="ltr">

                ./import_contrail_container.sh -f /tmp/contrail_container -r docker.io/opencontrailnightly -t 1234

            </div>

            </div>

        -   Import from private secure registry:

            <div id="jd0e165" class="sample" dir="ltr">

            <div class="output" dir="ltr">

                ./import_contrail_container.sh -f /tmp/contrail_container -r device.example.net:5443 -c http://device.example.net/pub/device.example.net.crt -t 1234

            </div>

            </div>

        -   Import from private insecure registry:

            <div id="jd0e171" class="sample" dir="ltr">

            <div class="output" dir="ltr">

                ./import_contrail_container.sh -f /tmp/contrail_container -r 10.0.0.1:5443 -i 1 -t 1234

            </div>

            </div>

    2.  Upload Contrail containers to the undercloud registry:

        <div id="jd0e177" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            openstack overcloud container image upload --config-file /tmp/contrail_container

        </div>

        </div>

## Customizing the Contrail Service with Templates (contrail-services.yaml)

This section contains information to customize Contrail services for
your network by modifying the `contrail-services.yaml` file.

-   Contrail Services customization

    <div id="jd0e194" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        vi ~/tripleo-heat-templates/environments/contrail-services.yaml

    </div>

    <div class="output" dir="ltr">

        parameter_defaults:
          ContrailSettings:
            VROUTER_GATEWAY: 10.0.0.1
            # KEY1: value1
            # KEY2: value2

            VXLAN_VN_ID_MODE: "configured"
            ENCAP_PRIORITY: "VXLAN,MPLSoUDP,MPLSoGRE"
            
          ContrailControllerParameters:
            AAAMode: rbac

    </div>

    </div>

-   Contrail registry settings

    <div id="jd0e202" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        vi ~/tripleo-heat-templates/environments/contrail-services.yaml

    </div>

    </div>

    Here are few examples of default values for various registries:

    -   Public Juniper registry

        <div id="jd0e211" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            parameter_defaults:
              ContrailRegistry: hub.juniper.net/contrail
              ContrailRegistryUser: <USER>
              ContrailRegistryPassword: <PASSWORD>

        </div>

        </div>

    -   Insecure registry

        <div id="jd0e217" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            parameter_defaults:
              ContrailRegistryInsecure: true
              DockerInsecureRegistryAddress: 10.87.64.32:5000,192.168.24.1:8787
              ContrailRegistry: 10.87.64.32:5000

        </div>

        </div>

    -   Private secure registry

        <div id="jd0e223" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            parameter_defaults:
              ContrailRegistryCertUrl: http://device.example.net/pub/device.example.net.crt
              ContrailRegistry: device.example.net:5443

        </div>

        </div>

-   Contrail Container image settings

    <div id="jd0e229" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        parameter_defaults:
          ContrailImageTag: queens-5.0-104-rhel-queens

    </div>

    </div>

<div id="id-customizing-the-contrail-network-with-templates">

## Customizing the Contrail Network with Templates

-   [Overview](setting-up-contrail-rhosp16-overcloud.html#id-overview)

-   [Roles Configuration
    (roles\_data\_contrail\_aio.yaml)](setting-up-contrail-rhosp16-overcloud.html#id-roles-configuration-rolesdatacontrailaioyaml)

-   [Network Parameter Configuration
    (contrail-net.yaml)](setting-up-contrail-rhosp16-overcloud.html#id-network-parameter-configuration-contrailnetyaml)

-   [Network Interface Configuration
    (\*-NIC-\*.yaml)](setting-up-contrail-rhosp16-overcloud.html#id-network-interface-configuration-nicyaml)

-   [Advanced vRouter Kernel Mode
    Configuration](setting-up-contrail-rhosp16-overcloud.html#id-advanced-vrouter-kernel-mode-configuration)

-   [Advanced vRouter DPDK Mode
    Configuration](setting-up-contrail-rhosp16-overcloud.html#id-advanced-vrouter-dpdk-mode-configuration)

-   [Advanced vRouter SRIOV + Kernel Mode
    Configuration](setting-up-contrail-rhosp16-overcloud.html#id-advanced-vrouter-sriov-kernel-mode-configuration)

-   [Advanced vRouter SRIOV + DPDK Mode
    Configuration](setting-up-contrail-rhosp16-overcloud.html#id-advanced-vrouter-sriov-dpdk-mode-configuration)

-   [Advanced
    Scenarios](setting-up-contrail-rhosp16-overcloud.html#id-advanced-scenarios)

### Overview

In order to customize the network, define different networks and
configure the overcloud nodes NIC layout. TripleO supports a flexible
way of customizing the network.

The following networking customization example uses network as:

Table 1: Network Customization

| Network       | VLAN | overcloud Nodes          |
|:--------------|:-----|:-------------------------|
| provisioning  | \-   | All                      |
| internal\_api | 710  | All                      |
| external\_api | 720  | OpenStack CTRL           |
| storage       | 740  | OpenStack CTRL, Computes |
| storage\_mgmt | 750  | OpenStack CTRL           |
| tenant        | \-   | Contrail CTRL, Computes  |

### Roles Configuration (roles\_data\_contrail\_aio.yaml)

The networks must be activated per role in the roles\_data file:

<div id="jd0e332" class="sample" dir="ltr">

<div class="output" dir="ltr">

    vi ~/tripleo-heat-templates/roles_data_contrail_aio.yaml

</div>

</div>

-   [OpenStack
    Controller](setting-up-contrail-rhosp16-overcloud.html#jd0e337)

-   [Compute Node](setting-up-contrail-rhosp16-overcloud.html#jd0e343)

-   [Contrail
    Controller](setting-up-contrail-rhosp16-overcloud.html#jd0e349)

-   [Compute DPDK](setting-up-contrail-rhosp16-overcloud.html#jd0e355)

-   [Compute SRIOV](setting-up-contrail-rhosp16-overcloud.html#jd0e361)

-   [Compute CSN](setting-up-contrail-rhosp16-overcloud.html#jd0e367)

#### OpenStack Controller

<div id="jd0e340" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Compute Node

<div id="jd0e346" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Contrail Controller

<div id="jd0e352" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Compute DPDK

<div id="jd0e358" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Compute SRIOV

<div id="jd0e364" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Compute CSN

<div id="jd0e370" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

### Network Parameter Configuration (contrail-net.yaml)

<div id="jd0e378" class="sample" dir="ltr">

<div class="output" dir="ltr">

    cat ~/tripleo-heat-templates/environments/contrail/contrail-net.yaml

</div>

  

<div class="output" dir="ltr">

    resource_registry:
      OS::TripleO::Controller::Net::SoftwareConfig: ../../network/config/contrail/controller-nic-config.yaml
      OS::TripleO::ContrailController::Net::SoftwareConfig: ../../network/config/contrail/contrail-controller-nic-config.yaml
      OS::TripleO::ContrailControlOnly::Net::SoftwareConfig: ../../network/config/contrail/contrail-controller-nic-config.yaml
      OS::TripleO::Compute::Net::SoftwareConfig: ../../network/config/contrail/compute-nic-config.yaml
      OS::TripleO::ContrailDpdk::Net::SoftwareConfig: ../../network/config/contrail/contrail-dpdk-nic-config.yaml
      OS::TripleO::ContrailSriov::Net::SoftwareConfig: ../../network/config/contrail/contrail-sriov-nic-config.yaml
      OS::TripleO::ContrailTsn::Net::SoftwareConfig: ../../network/config/contrail/contrail-tsn-nic-config.yaml

</div>

  

<div class="output" dir="ltr">

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

</div>

</div>

### Network Interface Configuration (\*-NIC-\*.yaml)

NIC configuration files exist per role in the following directory:

<div id="jd0e394" class="sample" dir="ltr">

<div class="output" dir="ltr">

    cd ~/tripleo-heat-templates/network/config/contrail

</div>

</div>

-   [OpenStack
    Controller](setting-up-contrail-rhosp16-overcloud.html#jd0e399)

-   [Contrail
    Controller](setting-up-contrail-rhosp16-overcloud.html#jd0e414)

-   [Compute Node](setting-up-contrail-rhosp16-overcloud.html#jd0e432)

#### OpenStack Controller

<div id="jd0e402" class="sample" dir="ltr">

<div class="output" dir="ltr">

    heat_template_version: rocky

    description: >
      Software Config to drive os-net-config to configure multiple interfaces
      for the compute role. This is an example for a Nova compute node using
      Contrail vrouter and the vhost0 interface.

</div>

  

<div class="output" dir="ltr">

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

</div>

  

<div class="output" dir="ltr">

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

</div>

  

<div class="output" dir="ltr">

    outputs:
      OS::stack_id:
        description: The OsNetConfigImpl resource.
        value:
          get_resource: OsNetConfigImpl

</div>

</div>

#### Contrail Controller

<div id="jd0e417" class="sample" dir="ltr">

<div class="output" dir="ltr">

    heat_template_version: rocky

</div>

  

<div class="output" dir="ltr">

    description: >
      Software Config to drive os-net-config to configure multiple interfaces
      for the compute role. This is an example for a Nova compute node using
      Contrail vrouter and the vhost0 interface.

</div>

  

<div class="output" dir="ltr">

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

</div>

  

<div class="output" dir="ltr">

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

</div>

  

<div class="output" dir="ltr">

    outputs:
      OS::stack_id:
        description: The OsNetConfigImpl resource.
        value:
          get_resource: OsNetConfigImpl

</div>

</div>

#### Compute Node

<div id="jd0e435" class="sample" dir="ltr">

<div class="output" dir="ltr">

    heat_template_version: rocky

</div>

  

<div class="output" dir="ltr">

    description: >
      Software Config to drive os-net-config to configure multiple interfaces
      for the compute role. This is an example for a Nova compute node using
      Contrail vrouter and the vhost0 interface.

</div>

  

<div class="output" dir="ltr">

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

</div>

  

<div class="output" dir="ltr">

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

</div>

  

<div class="output" dir="ltr">

    outputs:
      OS::stack_id:
        description: The OsNetConfigImpl resource.
        value:
          get_resource: OsNetConfigImpl

</div>

</div>

### Advanced vRouter Kernel Mode Configuration

In addition to the standard NIC configuration, the vRouter kernel mode
supports VLAN, Bond, and Bond + VLAN modes. The configuration snippets
below only show the relevant section of the NIC template configuration
for each mode.

-   [VLAN](setting-up-contrail-rhosp16-overcloud.html#jd0e459)

-   [Bond](setting-up-contrail-rhosp16-overcloud.html#jd0e465)

-   [Bond + VLAN](setting-up-contrail-rhosp16-overcloud.html#jd0e471)

#### VLAN

<div id="jd0e462" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Bond

<div id="jd0e468" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Bond + VLAN

<div id="jd0e474" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

### Advanced vRouter DPDK Mode Configuration

In addition to the standard NIC configuration, the vRouter DPDK mode
supports Standard, VLAN, Bond, and Bond + VLAN modes.

Network Environment Configuration:

<div id="jd0e486" class="sample" dir="ltr">

<div class="output" dir="ltr">

    vi ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml

</div>

</div>

Enable the number of hugepages:

<div id="jd0e491" class="sample" dir="ltr">

<div class="output" dir="ltr">

     # For Intel CPU
      ContrailDpdkParameters:
        KernelArgs: "intel_iommu=on iommu=pt default_hugepagesz=1GB hugepagesz=1G hugepages=4 hugepagesz=2M hugepages=1024"
        ExtraSysctlSettings:
          # must be equal to value from kernel args: hugepages=4
          vm.nr_hugepages:
            value: 4
          vm.max_map_count:
            value: 128960

</div>

</div>

See the following NIC template configurations for vRouter DPDK mode. The
configuration snippets below only show the relevant section of the NIC
configuration for each mode.

-   [Standard](setting-up-contrail-rhosp16-overcloud.html#jd0e498)

-   [VLAN](setting-up-contrail-rhosp16-overcloud.html#jd0e504)

-   [Bond](setting-up-contrail-rhosp16-overcloud.html#jd0e510)

-   [Bond + VLAN](setting-up-contrail-rhosp16-overcloud.html#jd0e516)

#### Standard

<div id="jd0e501" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### VLAN

<div id="jd0e507" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Bond

<div id="jd0e513" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Bond + VLAN

<div id="jd0e519" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

### Advanced vRouter SRIOV + Kernel Mode Configuration

vRouter SRIOV + Kernel mode can be used in the following combinations:

-   Standard

-   VLAN

-   Bond

-   Bond + VLAN

Network environment configuration:

<div id="jd0e544" class="sample" dir="ltr">

<div class="output" dir="ltr">

    vi ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml

</div>

</div>

Enable the number of hugepages:

<div id="jd0e549" class="sample" dir="ltr">

<div class="output" dir="ltr">

    ContrailSriovParameters:
        KernelArgs: "intel_iommu=on iommu=pt default_hugepagesz=1GB hugepagesz=1G hugepages=4 hugepagesz=2M hugepages=1024"
        ExtraSysctlSettings:
          # must be equal to value from 1G kernel args: hugepages=4
          vm.nr_hugepages:
            value: 4

</div>

</div>

SRIOV PF/VF settings:

<div id="jd0e554" class="sample" dir="ltr">

<div class="output" dir="ltr">

    NovaPCIPassthrough:
    - devname: "ens2f1"
      physical_network: "sriov1"
    ContrailSriovNumVFs: ["ens2f1:7"]

</div>

</div>

The SRIOV NICs are not configured in the NIC templates. However, vRouter
NICs must still be configured. See the following NIC template
configurations for vRouter kernel mode. The configuration snippets below
only show the relevant section of the NIC configuration for each mode.

-   [VLAN](setting-up-contrail-rhosp16-overcloud.html#jd0e561)

-   [Bond](setting-up-contrail-rhosp16-overcloud.html#jd0e567)

-   [Bond + VLAN](setting-up-contrail-rhosp16-overcloud.html#jd0e573)

#### VLAN

<div id="jd0e564" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Bond

<div id="jd0e570" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Bond + VLAN

<div id="jd0e576" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

### Advanced vRouter SRIOV + DPDK Mode Configuration

vRouter SRIOV + DPDK can be used in the following combinations:

-   Standard

-   VLAN

-   Bond

-   Bond + VLAN

Network environment configuration:

<div id="jd0e601" class="sample" dir="ltr">

<div class="output" dir="ltr">

    vi ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml

</div>

</div>

Enable the number of hugepages

<div id="jd0e606" class="sample" dir="ltr">

<div class="output" dir="ltr">

    ContrailSriovParameters:
        KernelArgs: "intel_iommu=on iommu=pt default_hugepagesz=1GB hugepagesz=1G hugepages=4 hugepagesz=2M hugepages=1024"
        ExtraSysctlSettings:
          # must be equal to value from 1G kernel args: hugepages=4
          vm.nr_hugepages:
            value: 4

</div>

</div>

SRIOV PF/VF settings

<div id="jd0e611" class="sample" dir="ltr">

<div class="output" dir="ltr">

    NovaPCIPassthrough:
    - devname: "ens2f1"
      physical_network: "sriov1"
    ContrailSriovNumVFs: ["ens2f1:7"]

</div>

</div>

The SRIOV NICs are not configured in the NIC templates. However, vRouter
NICs must still be configured. See the following NIC template
configurations for vRouter DPDK mode. The configuration snippets below
only show the relevant section of the NIC configuration for each mode.

-   [Standard](setting-up-contrail-rhosp16-overcloud.html#jd0e618)

-   [VLAN](setting-up-contrail-rhosp16-overcloud.html#jd0e624)

-   [Bond](setting-up-contrail-rhosp16-overcloud.html#jd0e630)

-   [Bond + VLAN](setting-up-contrail-rhosp16-overcloud.html#jd0e636)

#### Standard

<div id="jd0e621" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### VLAN

<div id="jd0e627" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Bond

<div id="jd0e633" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

#### Bond + VLAN

<div id="jd0e639" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

### Advanced Scenarios

Remote Compute

Remote Compute extends the data plane to remote locations (POP) whilest
keeping the control plane central. Each POP will have its own set of
Contrail control services, which are running in the central location.
The difficulty is to ensure that the compute nodes of a given POP
connect to the Control nodes assigned to that POC. The Control nodes
must have predictable IP addresses and the compute nodes have to know
these IP addresses. In order to achieve that the following methods are
used:

-   Custom Roles

-   Static IP assignment

-   Precise Node placement

-   Per Node hieradata

Each overcloud node has a unique DMI UUID. This UUID is known on the
undercloud node as well as on the overcloud node. Hence, this UUID can
be used for mapping node specific information. For each POP, a Control
role and a Compute role has to be created.

Overview

![](documentation/images/g200478.png)

Mapping Table

Table 2: Mapping Table

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

<div id="jd0e905" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

**Note**

The generated *ironic\_list* will be needed on the undercloud to import
the nodes to Ironic.

Get the ironic\_lists from the overcloud KVM hosts and combine them.

<div id="jd0e920" class="sample" dir="ltr">

<div class="output" dir="ltr">

    cat ironic_list_control_only
    52:54:00:3a:2f:ca control-only-1-5b3s30 10.87.64.31 control-only 16234
    52:54:00:31:4f:63 control-only-2-5b3s30 10.87.64.31 control-only 16235
    52:54:00:0c:11:74 control-only-1-5b3s31 10.87.64.32 control-only 16234
    52:54:00:56:ab:55 control-only-2-5b3s31 10.87.64.32 control-only 16235
    52:54:00:c1:f0:9a control-only-1-5b3s32 10.87.64.33 control-only 16234
    52:54:00:f3:ce:13 control-only-2-5b3s32 10.87.64.33 control-only 16235

</div>

</div>

Import:

<div id="jd0e925" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

ControlOnly node introspection

<div id="jd0e930" class="sample" dir="ltr">

<div class="output" dir="ltr">

    openstack overcloud node introspect --all-manageable --provide

</div>

</div>

Get the ironic UUID of the ControlOnly nodes

<div id="jd0e935" class="sample" dir="ltr">

<div class="output" dir="ltr">

    openstack baremetal node list |grep control-only
    | 7d758dce-2784-45fd-be09-5a41eb53e764 | control-only-1-5b3s30  | None | power off | available | False |
    | d26abdeb-d514-4a37-a7fb-2cd2511c351f | control-only-2-5b3s30  | None | power off | available | False |
    | 91dd9fa9-e8eb-4b51-8b5e-bbaffb6640e4 | control-only-1-5b3s31  | None | power off | available | False |
    | 09fa57b8-580f-42ec-bf10-a19573521ed4 | control-only-2-5b3s31  | None | power off | available | False |
    | f4766799-24c8-4e3b-af54-353f2b796ca4 | control-only-1-5b3s32  | None | power off | available | False |
    | 58a803ae-a785-470e-9789-139abbfa74fb | control-only-2-5b3s32  | None | power off | available | False |

</div>

</div>

The first ControlOnly node on each of the overcloud KVM hosts will be
used for POP1, the second for POP2, and so and so forth.

Get the ironic UUID of the POP compute nodes:

<div id="jd0e942" class="sample" dir="ltr">

<div class="output" dir="ltr">

    openstack baremetal node list |grep compute
    | 91d6026c-b9db-49cb-a685-99a63da5d81e | compute-3-5b3s30 | None | power off | available | False |
    | 8028eb8c-e1e6-4357-8fcf-0796778bd2f7 | compute-4-5b3s30 | None | power off | available | False |
    | b795b3b9-c4e3-4a76-90af-258d9336d9fb | compute-3-5b3s31 | None | power off | available | False |
    | 2d4be83e-6fcc-4761-86f2-c2615dd15074 | compute-4-5b3s31 | None | power off | available | False |

</div>

The first two compute nodes belong to POP1 the second two compute nodes
belong to POP2.

</div>

Create an input YAML using the ironic UUIDs:

<div id="jd0e949" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

**Note**

Only control\_nodes, compute\_nodes, dpdk\_nodes and sriov\_nodes are
supported.

Generate subcluster environment:

<div id="jd0e957" class="sample" dir="ltr">

<div class="output" dir="ltr">

    ~/tripleo-heat-templates/tools/contrail/create_subcluster_environment.py -i ~/subcluster_input.yaml \
                   -o ~/tripleo-heat-templates/environments/contrail/contrail-subcluster.yaml

</div>

</div>

Check subcluster environment file:

<div id="jd0e962" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

Deployment

Add contrail-subcluster.yaml, contrail-ips-from-pool-all.yaml and
contrail-scheduler-hints.yaml to the OpenStack deploy command:

<div id="jd0e969" class="sample" dir="ltr">

<div class="output" dir="ltr">

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

</div>

</div>

</div>

## Installing Overcloud

1.  <span id="overcloud-deployment">Deployment:</span>
    <div id="jd0e983" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        openstack overcloud deploy --templates tripleo-heat-templates/ \
          --stack overcloud --libvirt-type kvm \
          --roles-file $role_file \
          -e tripleo-heat-templates/environments/rhsm.yaml \
          -e tripleo-heat-templates/environments/network-isolation.yaml \
          -e tripleo-heat-templates/environments/contrail/contrail-services.yaml \
          -e tripleo-heat-templates/environments/contrail/contrail-net.yaml \
          -e tripleo-heat-templates/environments/contrail/contrail-plugins.yaml \
          -e containers-prepare-parameter.yaml \
          -e rhsm.yaml

    </div>

    </div>
2.  <span id="jd0e986">Validation Test:</span>
    <div id="jd0e989" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        source overcloudrc
        curl -O http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img
        openstack image create --container-format bare --disk-format qcow2 --file cirros-0.3.5-x86_64-disk.img cirros
        openstack flavor create --public cirros --id auto --ram 64 --disk 0 --vcpus 1
        openstack network create net1
        openstack subnet create --subnet-range 1.0.0.0/24 --network net1 sn1
        nova boot --image cirros --flavor cirros --nic net-id=`openstack network show net1 -c id -f value` --availability-zone nova:overcloud-novacompute-0.localdomain c1
        nova list

    </div>

    </div>

 
