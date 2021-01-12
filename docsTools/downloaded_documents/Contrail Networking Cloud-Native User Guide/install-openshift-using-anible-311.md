# Installing a Standalone Red Hat OpenShift Container Platform 3.11 Cluster with Contrail Using Contrail OpenShift Deployer

 

You can install Contrail Networking together with a standalone Red Hat
OpenShift Container Platform 3.11 cluster using Contrail OpenShift
deployer. Consider the topology illustrated here.

![Figure 1: Sample installation topology](images/g300780.png)

<span class="kbd user-typing" v-pre="">Prerequisites</span>

The recommended system requirements are:

System Requirements

Primary Node

Infrastructure Node

Compute Node

CPU/RAM

8 vCPU, 16 GB RAM

16 vCPU, 64 GB RAM

As per
[OpenShift](https://docs.openshift.com/container-platform/3.11/install/prerequisites.html)
recommendations.

Disk

100 GB

250 GB

**Note**

If you use NFS mount volumes, check disk capacity and mounts. Also,
openshift-logging with NFS is not recommended.

Perform the following steps to install a standalone OpenShift 3.11
cluster along with Contrail Networking using
contrail-openshift-deployer.

1.  <div id="jd0e78">

    Set up environment nodes for RHEL OpenShift enterprise
    installations:

    1.  <span id="jd0e83">Subscribe to RHEL.</span>

        `(all-nodes)# subscription-manager register --username <> --password <> --force`

    2.  <span id="jd0e89">From the list of available subscriptions, find
        and attach the pool ID for the OpenShift Container Platform
        subscription.</span>

        ` (all-nodes)# subscription-manager attach --pool=pool-ID `

    3.  <span id="jd0e98">Disable all yum repositories.</span>

        `(all-nodes)# subscription-manager repos --disable="*"`

    4.  <span id="jd0e104">Enable only the required repositories.</span>
        <div id="jd0e107" class="sample" dir="ltr">

        <div class="output" dir="ltr">

             (all-nodes)# subscription-manager repos \
                --enable="rhel-7-server-rpms" \
                --enable="rhel-7-server-extras-rpms" \
                --enable="rhel-7-server-ose-3.11-rpms" \
                --enable=rhel-7-fast-datapath-rpms \
                --enable="rhel-7-server-ansible-2.6-rpms"

        </div>

        </div>

    5.  <span id="jd0e110">Install required packages, such as
        python-netaddr, iptables-services, and so on.</span>

        `(all-nodes)# yum install -y tcpdump wget git net-tools bind-utils yum-utils iptables-services bridge-utils bash-completion kexec-tools sos psacct python-netaddr openshift-ansible`

    **Note**
    CentOS OpenShift Origin installations are not supported.

    </div>

2.  <span id="jd0e119">Get the files from the latest tar ball. Download
    the OpenShift Container Platform install package from Juniper
    software download site and modify the contents of the
    `openshift-ansible` inventory file.</span>

    1.  <span id="jd0e126">Download the Openshift Deployer
        (`contrail-openshift-deployer-release-tag.tgz`) installer from
        the Juniper software download site,
        <https://www.juniper.net/support/downloads/?p=contrail#sw>. See
        [README Access for Contrail Networking Registry
        19xx](https://www.juniper.net/documentation/en_US/contrail19/information-products/topic-collections/release-notes/readme-contrail-19.pdf)  
        for appropriate release tags.</span>

    2.  <span id="jd0e141">Copy the install package to the node from
        where Ansible is deployed. Ensure that the node has
        password-free access to the OpenShift primary and slave
        nodes.</span>

        `scp contrail-openshift-deployer-release-tag.tgz openshift-ansible-node:/root/`

    3.  <span id="jd0e153">Log in to the Ansible node and untar the
        <span class="cli"
        v-pre="">contrail-openshift-deployer-`release-tag`.tgz</span>
        package.</span>

        `tar -xzvf  contrail-openshift-deployer-release-tag.tgz -C /root/`

    4.  <span id="jd0e168">Verify the contents of the
        `openshift-ansible` directory.</span>

        `cd /root/openshift-ansible/`

    5.  <span id="jd0e177">Modify the `inventory/ose-install` file to
        match your OpenShift environment.</span>

        Populate the `inventory/ose-install` file with Contrail
        configuration parameters specific to your system. The following
        mandatory parameters must be set. For example:

        <div id="jd0e188" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            contrail_version=5.1
            contrail_container_tag=<>
            contrail_registry="hub.juniper.net/contrail-nightly"
            contrail_registry_username=<>
            contrail_registry_password=<>
            openshift_use_openshift_sdn=false
            os_sdn_network_plugin_name='cni'
            openshift_use_contrail=true

        </div>

        </div>

        **Note**

        The `contrail_container_tag` value for this release can be found
        in the [README Access to Contrail Registry
        19XX](/documentation/en_US/contrail19/information-products/topic-collections/release-notes/readme-contrail-19.pdf)  
        file.

        Juniper Networks recommends that you obtain the Ansible source
        files from the latest release.

    This procedure assumes that there is one primary node, one
    infrastructure node, and one compute node.

    <div id="jd0e207" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        master : server1 (1x.xx.xx.11)
        infrastructure : server2 (1x.xx.xx.22)
        compute : server3 (1x.xx.xx.33)

    </div>

    </div>

3.  <span id="jd0e210">Edit `/etc/hosts` to include all the nodes
    information.</span>
    <div id="jd0e216" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        [root@server1]# cat /etc/hosts
        127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
        ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
        1x.xx.xx.100 puppet
        1x.xx.xx.11 server1.contrail.juniper.net server1
        1x.xx.xx.22 server2.contrail.juniper.net server2
        1x.xx.xx.33 server3.contrail.juniper.net server3

    </div>

    </div>

4.  <span id="jd0e219">Set up password-free SSH access to the Ansible
    node and all the nodes.</span>
    <div id="jd0e222" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        ssh-keygen -t rsa
        ssh-copy-id root@1x.xx.xx.11
        ssh-copy-id root@1x.xx.xx.22
        ssh-copy-id root@1x.xx.xx.33

    </div>

    </div>

5.  <span id="jd0e225">Run Ansible playbook to install OpenShift
    Container Platform with Contrail. Before you run Ansible playbook,
    ensure that you have edited `inventory/ose-install` file.</span>

    <div id="jd0e231" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        (ansible-node)# cd /root/openshift-ansible
        (ansible-node)# ansible-playbook -i inventory/ose-install playbooks/prerequisites.yml
        (ansible-node)# ansible-playbook -i inventory/ose-install playbooks/deploy_cluster.yml

    </div>

    </div>

    For a sample `inventory/ose-install` file, see [Sample
    inventory/ose-install
    File](install-openshift-using-anible-311.html#sample_ose_install).

6.  <span id="loginpass">Create a password for the admin user to log in
    to the UI from the primary node.</span>

    <div id="jd0e244" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        (master-node)# htpasswd /etc/origin/master/htpasswd admin

    </div>

    </div>

    **Note**

    If you are using a load balancer, you must manually copy the
    htpasswd file into all your primary nodes.

7.  <span id="jd0e250">Assign cluster-admin role to admin user.</span>
    <div id="jd0e253" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        (master-node)# oc adm policy add-cluster-role-to-user cluster-admin admin
        (master-node)# oc login -u admin

    </div>

    </div>

8.  <span id="jd0e256">Open a Web browser and type the entire fqdn name
    of your primary node or load balancer node, followed by <span
    class="cli" v-pre="">:8443/console</span>.</span>

    <div id="jd0e262" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        https://<your host name from your ose-install inventory>:8443/console

    </div>

    </div>

    Use the user name and password created in step
    [6](install-openshift-using-anible-311.html#loginpass) to log in to
    the Web console.

    Your DNS should resolve the host name for access. If the host name
    is not resolved, modify the /etc/hosts file to route to the above
    host.

**Note**

OpenShift 3.11 cluster upgrades are not supported.

<div id="sample_ose_install" class="sample" dir="ltr">

**Sample inventory/ose-install File**

<div class="output" dir="ltr">

    [OSEv3:vars]

    ###########################################################################
    ### OpenShift Basic Vars
    ###########################################################################
    openshift_deployment_type=openshift-enterprise
    deployment_type=openshift-enterprise
    containerized=false
    openshift_disable_check=docker_image_availability,memory_availability,package_availability,disk_availability,package_version,docker_storage

    # Default node selectors
    openshift_hosted_infra_selector="node-role.kubernetes.io/infra=true"

    oreg_auth_user=<>
    oreg_auth_password=<>

    ###########################################################################
    ### OpenShift Master Vars
    ###########################################################################

    openshift_master_api_port=8443
    openshift_master_console_port=8443
    openshift_master_cluster_method=native

    # Set this line to enable NFS
    openshift_enable_unsupported_configurations=True


    ###########################################################################
    ### OpenShift Network Vars
    ###########################################################################

    openshift_use_openshift_sdn=false
    os_sdn_network_plugin_name='cni'
    openshift_use_contrail=true

    ###########################################################################
    ### OpenShift Authentication Vars
    ###########################################################################

    # htpasswd Authentication
    openshift_master_identity_providers=[{'name': 'htpasswd_auth', 'login': 'true', 'challenge': 'true', 'kind': 'HTPasswdPasswordIdentityProvider'}]

    ###########################################################################
    ### OpenShift Router and Registry Vars
    ###########################################################################

    openshift_hosted_router_replicas=1
    openshift_hosted_registry_replicas=1

    openshift_hosted_registry_storage_kind=nfs
    openshift_hosted_registry_storage_access_modes=['ReadWriteMany']
    openshift_hosted_registry_storage_nfs_directory=/export
    openshift_hosted_registry_storage_nfs_options='*(rw,root_squash)'
    openshift_hosted_registry_storage_volume_name=registry
    openshift_hosted_registry_storage_volume_size=10Gi
    openshift_hosted_registry_pullthrough=true
    openshift_hosted_registry_acceptschema2=true
    openshift_hosted_registry_enforcequota=true
    openshift_hosted_router_selector="node-role.kubernetes.io/infra=true"
    openshift_hosted_registry_selector="node-role.kubernetes.io/infra=true"

    ###########################################################################
    ### OpenShift Service Catalog Vars
    ###########################################################################

    openshift_enable_service_catalog=True

    template_service_broker_install=True
    openshift_template_service_broker_namespaces=['openshift']

    ansible_service_broker_install=True

    openshift_hosted_etcd_storage_kind=nfs
    openshift_hosted_etcd_storage_nfs_options="*(rw,root_squash,sync,no_wdelay)"
    openshift_hosted_etcd_storage_nfs_directory=/export
    openshift_hosted_etcd_storage_labels={'storage': 'etcd-asb'}
    openshift_hosted_etcd_storage_volume_name=etcd-asb
    openshift_hosted_etcd_storage_access_modes=['ReadWriteOnce']
    openshift_hosted_etcd_storage_volume_size=2G





    ###########################################################################
    ### OpenShift Metrics and Logging Vars
    ###########################################################################
    # Enable cluster metrics
    openshift_metrics_install_metrics=True

    openshift_metrics_storage_kind=nfs
    openshift_metrics_storage_access_modes=['ReadWriteOnce']
    openshift_metrics_storage_nfs_directory=/export
    openshift_metrics_storage_nfs_options='*(rw,root_squash)'
    openshift_metrics_storage_volume_name=metrics
    openshift_metrics_storage_volume_size=2Gi
    openshift_metrics_storage_labels={'storage': 'metrics'}

    openshift_metrics_cassandra_nodeselector={"node-role.kubernetes.io/infra":"true"}
    openshift_metrics_hawkular_nodeselector={"node-role.kubernetes.io/infra":"true"}
    openshift_metrics_heapster_nodeselector={"node-role.kubernetes.io/infra":"true"}

    # Enable cluster logging. (( 
    ####openshift_logging_install_logging=True
    openshift_logging_install_logging=False
    #openshift_logging_storage_kind=nfs
    #openshift_logging_storage_access_modes=['ReadWriteOnce']
    #openshift_logging_storage_nfs_directory=/export
    #openshift_logging_storage_nfs_options='*(rw,root_squash)'
    #openshift_logging_storage_volume_name=logging
    #openshift_logging_storage_volume_size=5Gi
    #openshift_logging_storage_labels={'storage': 'logging'}
    #openshift_logging_es_cluster_size=1
    #openshift_logging_es_nodeselector={"node-role.kubernetes.io/infra":"true"}
    #openshift_logging_kibana_nodeselector={"node-role.kubernetes.io/infra":"true"}
    #openshift_logging_curator_nodeselector={"node-role.kubernetes.io/infra":"true"}

    ###########################################################################
    ### OpenShift Prometheus Vars
    ###########################################################################

    ## Add Prometheus Metrics:
    openshift_hosted_prometheus_deploy=True
    openshift_prometheus_node_selector={"node-role.kubernetes.io/infra":"true"}
    openshift_prometheus_namespace=openshift-metrics

    # Prometheus
    openshift_prometheus_storage_kind=nfs
    openshift_prometheus_storage_access_modes=['ReadWriteOnce']
    openshift_prometheus_storage_nfs_directory=/export
    openshift_prometheus_storage_nfs_options='*(rw,root_squash)'
    openshift_prometheus_storage_volume_name=prometheus
    openshift_prometheus_storage_volume_size=1Gi
    openshift_prometheus_storage_labels={'storage': 'prometheus'}
    openshift_prometheus_storage_type='pvc'

    # For prometheus-alertmanager
    openshift_prometheus_alertmanager_storage_kind=nfs
    openshift_prometheus_alertmanager_storage_access_modes=['ReadWriteOnce']
    openshift_prometheus_alertmanager_storage_nfs_directory=/export
    openshift_prometheus_alertmanager_storage_nfs_options='*(rw,root_squash)'
    openshift_prometheus_alertmanager_storage_volume_name=prometheus-alertmanager
    openshift_prometheus_alertmanager_storage_volume_size=1Gi
    openshift_prometheus_alertmanager_storage_labels={'storage': 'prometheus-alertmanager'}
    openshift_prometheus_alertmanager_storage_type='pvc'

    # For prometheus-alertbuffer
    openshift_prometheus_alertbuffer_storage_kind=nfs
    openshift_prometheus_alertbuffer_storage_access_modes=['ReadWriteOnce']
    openshift_prometheus_alertbuffer_storage_nfs_directory=/export
    openshift_prometheus_alertbuffer_storage_nfs_options='*(rw,root_squash)'
    openshift_prometheus_alertbuffer_storage_volume_name=prometheus-alertbuffer
    openshift_prometheus_alertbuffer_storage_volume_size=1Gi
    openshift_prometheus_alertbuffer_storage_labels={'storage': 'prometheus-alertbuffer'}
    openshift_prometheus_alertbuffer_storage_type='pvc'


    #########################################################################
    ### Openshift HA
    #########################################################################

    # Openshift HA
    openshift_master_cluster_hostname=load-balancer-0-3eba0c20dc494dfc93d5d50d06bbde89
    openshift_master_cluster_public_hostname=load-balancer-0-3eba0c20dc494dfc93d5d50d06bbde89


    #########################################################################
    ### Contrail Variables
    ########################################################################

    service_subnets="172.30.0.0/16"
    pod_subnets="10.128.0.0/14"

    # Below are Contrail variables. Comment them out if you don't want to install Contrail through ansible-playbook
    contrail_version=5.1
    contrail_container_tag=<>
    contrail_registry=hub.juniper.net/contrail
    contrail_registry_username=<>
    contrail_registry_password=<>
    openshift_docker_insecure_registries=hub.juniper.net/contrail
    contrail_nodes=[10.0.0.5,10.0.0.3,10.0.0.4]
    vrouter_physical_interface=eth0


    ###########################################################################
    ### OpenShift Hosts
    ###########################################################################
    [OSEv3:children]
    masters
    etcd
    nodes
    lb
    nfs
    openshift_ca

    [masters]
    kube-master-2-3eba0c20dc494dfc93d5d50d06bbde89
    kube-master-1-3eba0c20dc494dfc93d5d50d06bbde89
    kube-master-0-3eba0c20dc494dfc93d5d50d06bbde89

    [etcd]
    kube-master-2-3eba0c20dc494dfc93d5d50d06bbde89
    kube-master-1-3eba0c20dc494dfc93d5d50d06bbde89
    kube-master-0-3eba0c20dc494dfc93d5d50d06bbde89

    [lb]
    load-balancer-0-3eba0c20dc494dfc93d5d50d06bbde89

    [nodes]
    kube-master-2-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-master'
    controller-0-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-infra'
    compute-1-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-compute'
    controller-2-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-infra'
    kube-master-1-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-master'
    kube-master-0-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-master'
    compute-0-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-compute'
    controller-1-3eba0c20dc494dfc93d5d50d06bbde89 openshift_node_group_name='node-config-infra'

    [nfs]
    load-balancer-0-3eba0c20dc494dfc93d5d50d06bbde89

    [openshift_ca]
    kube-master-2-3eba0c20dc494dfc93d5d50d06bbde89
    kube-master-1-3eba0c20dc494dfc93d5d50d06bbde89
    kube-master-0-3eba0c20dc494dfc93d5d50d06bbde89

</div>

</div>

**Note**

The /etc/resolv.conf must have write permissions.

<span class="kbd user-typing" v-pre="">Caveats and Troubleshooting
Instructions</span>

-   If a Java error occurs, install the
    `yum install java-1.8.0-openjdk-devel.x86_64` package and rerun
    `deploy_cluster`.

-   If the service\_catalog parameter does not pass but the cluster is
    operational, check whether the `/etc/resolv.conf` has <span
    class="cli" v-pre="">cluster.local</span> in its search line, and
    the nameserver as host IP address.

-   NTP is installed by OpenShift and must be synchronized by the user.
    This does not affect any Contrail functionality but is displayed in
    the <span class="cli" v-pre="">contrail-status</span> output.

-   If the <span class="cli" v-pre="">ansible\_service\_broker</span>
    component of OpenShift is not up and its <span class="cli"
    v-pre="">ansible\_service\_broker\_deploy</span> displays an error,
    it means that the <span class="cli"
    v-pre="">ansible\_service\_broker</span> pod did not come up
    properly. The most likely reason is that the <span class="cli"
    v-pre="">ansible\_service\_broker</span> pod failed its liveliness
    and readiness checks. Modify the liveliness and readiness checks of
    this pod when it’s brought online to make it operational. Also,
    verify that the <span class="cli"
    v-pre="">ansible\_service\_broker</span> pod uses the correct URL
    from Red Hat.

 
