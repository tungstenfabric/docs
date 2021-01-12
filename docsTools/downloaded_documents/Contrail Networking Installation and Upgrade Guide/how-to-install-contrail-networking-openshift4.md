# How to Install Contrail Networking and Red Hat OpenShift 4.4

 

<div id="intro">

<div class="mini-toc-intro">

You can install Contrail Networking with Red Hat Openshift 4.4 in
multiple environments.

This document shows one method of installing Red Hat Openshift 4.4 with
Contrail Networking in two separate contexts—on a VM running in a KVM
module and within Amazon Web Services (AWS). There are many
implementation and configuration options available for installing and
configuring Red Hat OpenShift 4.4 and the scope of all options is beyond
this document. For additional information on Red Hat Openshift 4.4
implementation options, see the [OpenShift Container Platform 4.4
Documentation](https://docs.openshift.com/container-platform/4.4/welcome/index.html)
from Red Hat.

This document includes the following sections:

</div>

</div>

## How to Install Contrail Networking and Red Hat OpenShift 4.4 using a VM Running in a KVM Module

<div class="mini-toc-intro">

This section illustrates how to install Contrail Networking with Red Hat
OpenShift 4.4 orchestration, where Contrail Networking and Red Hat
Openshift are running on virtual machines (VMs) in a Kernel-based
Virtual Machine (KVM) module. This procedure can also be performed to
configure an environment where Contrail Networking and Red Hat OpenShift
4.4 are running on a bare metal server.

</div>

-   [When to Use This
    Procedure](how-to-install-contrail-networking-openshift4.html#id-when-to-use-this-procedure-openshift44-kvm)

-   [Prerequisites](how-to-install-contrail-networking-openshift4.html#id-prerequisites-openshift44-kvm)

-   [Install Contrail Networking and Red Hat Openshift
    4.4](how-to-install-contrail-networking-openshift4.html#id-installing-contrail-networking-openshift44-kvm)

### When to Use This Procedure

This procedure is used to install Contrail Networking and Red Hat
OpenShift 4.4 orchestration on a virtual machine (VM) running in a
Kernel-based Virtual Machine (KVM) module. Support for Contrail
Networking installations onto VMs in Red Hat OpenShift 4.4 environments
is introduced in Contrail Networking Release 2008. See [Contrail
Networking Supported
Platforms](https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf)  .

You can also use this procedure to install Contrail Networking and Red
Hat OpenShift 4.4 orchestration on a bare metal server.

This procedure should work with all versions of Openshift 4.4.

### Prerequisites

This document makes the following assumptions about your environment:

-   the KVM environment is operational.

-   the server meets the platform requirements for the installation. See
    [Contrail Networking Supported
    Platforms](https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf)  .

-   Minimum server requirements:

    -   Primary nodes: 8 CPU, 40GB RAM, 250GB SSD storage

    -   Backup nodes: 4 CPU, 16GB RAM, 120GB SSD storage

    -   Helper node: 4 CPU, 8GB RAM, 30GB SSD storage

-   In single node deployments, do not use spinning disk arrays with low
    Input/Output Operations Per Second (IOPS) when using Contrail
    Networking with Red Hat Openshift. Higher IOPS disk arrays are
    required because the control plane always operates as a high
    availability setup in single node deployments.

    IOPS requirements vary by environment due to multiple factors beyond
    Contrail Networking and Red Hat Openshift. We, therefore, provide
    this guideline but do not provide direct guidance around IOPS
    requirements.

### Install Contrail Networking and Red Hat Openshift 4.4

<div class="mini-toc-intro">

Perform these steps to install Contrail Networking and Red Hat OpenShift
4.4 using a VM running in a KVM module:

</div>

-   [Create a Virtual Network or a Bridge Network for the
    Installation](how-to-install-contrail-networking-openshift4.html#id-create-a-virtual-network)

-   [Create a Helper Node with a Virtual Machine Running CentOS 7 or
    8](how-to-install-contrail-networking-openshift4.html#id-create-a-virtual-machine-running-red-hat-enterprise-linux-7-or-8)

-   [Prepare the Helper
    Node](how-to-install-contrail-networking-openshift4.html#id-prepare-the-helper-node)

-   [Create the Ignition
    Configurations](how-to-install-contrail-networking-openshift4.html#id-create-ignition-configurations)

-   [Launch the Virtual
    Machines](how-to-install-contrail-networking-openshift4.html#id-launch-the-virtual-machines)

-   [Monitor the Installation Process and Delete the Bootstrap Virtual
    Machine](how-to-install-contrail-networking-openshift4.html#id-monitoring-the-installation-process-and-deleting-the-bootstrap-virtual-machine)

-   [Finish the
    Installation](how-to-install-contrail-networking-openshift4.html#id-finish-the-installation)

#### Create a Virtual Network or a Bridge Network for the Installation

To create a virtual network or a bridge network for the installation:

1.  <span id="jd0e98">Log onto the server that will host the VM that
    will run Contrail Networking.</span>

    Download the `virt-net.xml` virtual network configuration file from
    the Red Hat repository.

    <div id="jd0e106" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # wget https://raw.githubusercontent.com/RedHatOfficial/ocp4-helpernode/master/docs/examples/virt-net.xml

    </div>

    </div>

2.  <span id="jd0e109">Create a virtual network using the `virt-net.xml`
    file.</span>

    You may need to modify your virtual network for your environment.

    *Example:*

    <div id="jd0e120" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # virsh net-define --file virt-net.xml

    </div>

    </div>

3.  <span id="jd0e123">Set the OpenShift 4.4 virtual network to
    autostart on bootup:</span>
    <div id="jd0e126" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # virsh net-autostart openshift4
        # virsh net-start openshift4

    </div>

    </div>

#### Create a Helper Node with a Virtual Machine Running CentOS 7 or 8

This procedure requires a helper node with a virtual machine that is
running either CentOS 7 or 8.

To create this helper node:

1.  <span id="jd0e140">Download the Kickstart file for the helper node
    from the Red Hat repository:</span>

    *CentOS 8*

    <div id="jd0e146" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # wget https://raw.githubusercontent.com/RedHatOfficial/ocp4-helpernode/master/docs/examples/helper-ks8.cfg -O helper-ks.cfg

    </div>

    </div>

    *CentOS 7*

    <div id="jd0e152" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # wget https://raw.githubusercontent.com/RedHatOfficial/ocp4-helpernode/master/docs/examples/helper-ks.cfg -O helper-ks.cfg

    </div>

    </div>

2.  <span id="jd0e155">If you haven’t already configured a root password
    and the NTP server on the helper node, enter the following
    commands:</span>

    *Example Root Password*

    <div id="jd0e161" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        rootpw --plaintext password

    </div>

    </div>

    *Example NTP Configuration*

    <div id="jd0e169" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        timezone America/Los_Angeles --isUtc --ntpservers=0.centos.pool.ntp.org,1.centos.pool.ntp.org,2.centos.pool.ntp.org,3.centos.pool.ntp.org

    </div>

    </div>

3.  <span id="jd0e172">Edit the `helper-ks.cfg` file for your
    environment and use it to install the helper node.</span>

    The following examples show how to install the helper node without
    having to take further actions:

    *CentOS 8*

    <div id="jd0e183" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # virt-install --name="ocp4-aHelper" --vcpus=2 --ram=4096 \
        --disk path=/var/lib/libvirt/images/ocp4-aHelper.qcow2,bus=virtio,size=50 \
        --os-variant centos8 --network network=openshift4,model=virtio \
        --boot hd,menu=on --location /var/lib/libvirt/iso/CentOS-8.2.2004-x86_64-dvd1.iso \
        --initrd-inject helper-ks.cfg --extra-args "inst.ks=file:/helper-ks.cfg" --noautoconsole

    </div>

    </div>

    *CentOS 7*

    <div id="jd0e189" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # virt-install --name="ocp4-aHelper" --vcpus=2 --ram=4096 \
        --disk path=/var/lib/libvirt/images/ocp4-aHelper.qcow2,bus=virtio,size=30 \
        --os-variant centos7.0 --network network=openshift4,model=virtio \
        --boot hd,menu=on --location /var/lib/libvirt/iso/CentOS-7-x86_64-Minimal-2003.iso \
        --initrd-inject helper-ks.cfg --extra-args "inst.ks=file:/helper-ks.cfg" --noautoconsole

    </div>

    </div>

    The helper node is installed with the following settings, which are
    pulled from the `virt-net.xml` file:

    -   <span class="kbd user-typing" v-pre="">HELPER\_IP</span>:
        192.168.7.77

    -   <span class="kbd user-typing" v-pre="">NetMask</span>:
        255.255.255.0

    -   <span class="kbd user-typing" v-pre="">Default Gateway</span>:
        192.168.7.1

    -   <span class="kbd user-typing" v-pre="">DNS Server</span>:
        8.8.8.8

4.  <span id="jd0e218">Monitor the helper node installation progress in
    the viewer:</span>

    <div id="jd0e221" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # virt-viewer --domain-name ocp4-aHelper

    </div>

    </div>

    When the installation process is complete, the helper node shuts
    off.

5.  <span id="jd0e226">Start the helper node:</span>
    <div id="jd0e229" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # virsh start ocp4-aHelper

    </div>

    </div>

#### Prepare the Helper Node

To prepare the helper node after the helper node installation:

1.  <span id="jd0e241">Login to the helper node:</span>

    <div id="jd0e244" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # ssh -l root HELPER_IP

    </div>

    </div>

    **Note**

    The default `HELPER_IP`, which was pulled from the `virt-net.xml`
    file, is 192.168.7.77.

2.  <span id="jd0e258">Install Enterprise Linux and update
    CentOS.</span>
    <div id="jd0e261" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(rpm -E %rhel).noarch.rpm
        # yum -y update

    </div>

    </div>

3.  <span id="jd0e264">Install Ansible and Git and clone the
    `helpernode` repository onto the helper node.</span>
    <div id="jd0e270" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # yum -y install ansible git
        # git clone https://github.com/RedHatOfficial/ocp4-helpernode
        # cd ocp4-helpernode

    </div>

    </div>

4.  <span id="jd0e273">Copy the vars.yaml file into the top-level
    directory:</span>

    <div id="jd0e276" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # cp docs/examples/vars.yaml .

    </div>

    </div>

    Review the vars.yml file. Consider changing any value that requires
    changing in your environment.

    The following values should be reviewed especially carefully:

    -   The domain name, which is defined using the `domain:` parameter
        in the `dns:` hierarchy. If you are using local DNS servers,
        modify the forwarder parameters—`forwarder1:` and `forwarder2:`
        are used in this example—to connect to these DNS servers.

    -   Hostnames for primary and worker nodes. Hostnames are defined
        using the `name:` parameter in either the `primaries:` or
        `workers:` hierarchies.

    -   IP and DHCP settings. If you are using a custom bridge network,
        modify the IP and DHCP settings accordingly.

    -   VM and BMS settings.

        If you are using a VM, set the `disk:` parameter as `disk: vda`.

        If you are using a BMS, set the `disk:` parameter as
        `disk: sda`.

    A sample vars.yml file:

    <div id="jd0e335" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        disk: vda
        helper:
          name: "helper"
          ipaddr: "192.168.7.77"
        dns:
          domain: "example.com"
          clusterid: "ocp4"
          forwarder1: "8.8.8.8"
          forwarder2: "8.8.4.4"
        dhcp:
          router: "192.168.7.1"
          bcast: "192.168.7.255"
          netmask: "255.255.255.0"
          poolstart: "192.168.7.10"
          poolend: "192.168.7.30"
          ipid: "192.168.7.0"
          netmaskid: "255.255.255.0"
        bootstrap:
          name: "bootstrap"
          ipaddr: "192.168.7.20"
          macaddr: "52:54:00:60:72:67"
        masters:
          - name: "master0"
            ipaddr: "192.168.7.21"
            macaddr: "52:54:00:e7:9d:67"
          - name: "master1"
            ipaddr: "192.168.7.22"
            macaddr: "52:54:00:80:16:23"
          - name: "master2"
            ipaddr: "192.168.7.23"
            macaddr: "52:54:00:d5:1c:39"
        workers:
          - name: "worker0"
            ipaddr: "192.168.7.11"
            macaddr: "52:54:00:f4:26:a1"
          - name: "worker1"
            ipaddr: "192.168.7.12"
            macaddr: "52:54:00:82:90:00"

    </div>

    </div>

5.  <span id="jd0e338">Review the `vars/main.yml` file to ensure the
    file reflects the correct version of Red Hat OpenShift. If you need
    to change the Red Hat Openshift version in the file, change
    it.</span>

    In the following sample `main.yml` file, Red Hat Openshift 4.4.21 is
    installed:

    <div id="jd0e349" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        ssh_gen_key: true
        install_filetranspiler: false
        staticips: false
        force_ocp_download: false
        ocp_bios: "https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.4/latest/rhcos-4.4.17-x86_64-metal.x86_64.raw.gz"
        ocp_initramfs: "https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.4/latest/rhcos-4.4.17-x86_64-installer-initramfs.x86_64.img"
        ocp_install_kernel: "https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.4/latest/rhcos-4.4.17-x86_64-installer-kernel-x86_64"
        ocp_client: "https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable-4.4/openshift-client-linux.tar.gz"
        ocp_installer: "https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable-4.4/openshift-install-linux.tar.gz"
        helm_source: "https://get.helm.sh/helm-v3.2.4-linux-amd64.tar.gz"
        chars: (\\_|\\$|\\\|\\/|\\=|\\)|\\(|\\&|\\^|\\%|\\$|\\#|\\@|\\!|\\*)
        ppc64le: false
        chronyconfig:
          enabled: false
        setup_registry:
          deploy: false
          autosync_registry: false
          registry_image: docker.io/library/registry:2
          local_repo: "ocp4/openshift4"
          product_repo: "openshift-release-dev"
          release_name: "ocp-release"
          release_tag: "4.4.21-x86_64"

    </div>

    </div>

6.  <span id="jd0e352">Run the playbook to setup the helper node:</span>
    <div id="jd0e355" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # ansible-playbook -e @vars.yaml tasks/main.yml

    </div>

    </div>

7.  <span id="jd0e358">After the playbook is run, gather information
    about your environment and confirm that all services are active and
    running:</span>
    <div id="jd0e361" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # /usr/local/bin/helpernodecheck services
        Status of services:
        ===================
        Status of dhcpd svc         ->    Active: active (running) since Mon 2020-09-28 05:40:10 EDT; 33min ago
        Status of named svc         ->    Active: active (running) since Mon 2020-09-28 05:40:08 EDT; 33min ago
        Status of haproxy svc   ->    Active: active (running) since Mon 2020-09-28 05:40:08 EDT; 33min ago
        Status of httpd svc         ->    Active: active (running) since Mon 2020-09-28 05:40:10 EDT; 33min ago
        Status of tftp svc      ->    Active: active (running) since Mon 2020-09-28 06:13:34 EDT; 1s ago
        Unit local-registry.service could not be found.
        Status of local-registry svc        ->

    </div>

    </div>

#### Create the Ignition Configurations

To create Ignition configurations:

1.  <span id="jd0e376">On your hypervisor and helper nodes, check that
    your NTP server is properly configured in the `/etc/chrony.conf`
    file:</span>

    <div id="jd0e382" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        chronyc tracking

    </div>

    </div>

    The installation fails with a
    `X509: certificate has expired or is not yet valid` message when NTP
    is not properly configured.

2.  <span id="jd0e390">Create a location to store your pull secret
    objects:</span>
    <div id="jd0e393" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # mkdir -p ~/.openshift

    </div>

    </div>

3.  <span id="jd0e396">From [Get Started with
    Openshift](https://www.openshift.com/try) website, download your
    pull secret and save it in the `~/.openshift/pull-secret`
    directory.</span>
    <div id="jd0e405" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # ls -1 ~/.openshift/pull-secret
        /root/.openshift/pull-secret

    </div>

    </div>

4.  <span id="jd0e408">An SSH key is created for you in the
    `~/.ssh/helper_rsa` directory after completing the previous step.
    You can use this key or create a unique key for
    authentication.</span>
    <div id="jd0e414" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # ls -1 ~/.ssh/helper_rsa
        /root/.ssh/helper_rsa

    </div>

    </div>

5.  <span id="jd0e417">Create an installation directory.</span>
    <div id="jd0e420" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # mkdir ~/ocp4
        # cd ~/ocp4

    </div>

    </div>

6.  <span id="jd0e423">Create an install-config.yaml file.</span>

    An example file:

    <div id="jd0e428" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # cat <<EOF > install-config.yaml
        apiVersion: v1
        baseDomain: example.com
        compute:
        - hyperthreading: Disabled
          name: worker
          replicas: 0
        controlPlane:
          hyperthreading: Disabled
          name: master
          replicas: 3
        metadata:
          name: ocp4
        networking:
          clusterNetworks:
          - cidr: 10.254.0.0/16
            hostPrefix: 24
          networkType: Contrail
          serviceNetwork:
          - 172.30.0.0/16
        platform:
          none: {}
        pullSecret: '$(< ~/.openshift/pull-secret)'
        sshKey: '$(< ~/.ssh/helper_rsa.pub)'
        EOF

    </div>

    </div>

7.  <span id="jd0e431">Create the installation manifests:</span>
    <div id="jd0e434" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # openshift-install create manifests

    </div>

    </div>

8.  <span id="jd0e437">Set the <span class="kbd user-typing"
    v-pre="">mastersSchedulable:</span> variable to <span
    class="kbd user-typing" v-pre="">false</span> in the
    `manifests/cluster-scheduler-02-config.yml` file.</span>

    <div id="jd0e449" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # sed -i 's/mastersSchedulable: true/mastersSchedulable: false/g' manifests/cluster-scheduler-02-config.yml

    </div>

    </div>

    A sample <span class="kbd user-typing"
    v-pre="">cluster-scheduler-02-config.yml</span> file after this
    configuration change:

    <div id="jd0e457" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # cat manifests/cluster-scheduler-02-config.yml
        apiVersion: config.openshift.io/v1
        kind: Scheduler
        metadata:
          creationTimestamp: null
          name: cluster
        spec:
          mastersSchedulable: false
          policy:
            name: ""
        status: {}

    </div>

    </div>

    This configuration change is needed to prevent pods from being
    scheduled on control plane machines.

9.  <span id="jd0e462">Clone the contrail operator repository:</span>
    <div id="jd0e465" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # git clone https://github.com/Juniper/contrail-operator.git
        # git checkout R2008

    </div>

    </div>

10. <span id="jd0e468">Create the Contrail operator configuration
    file.</span>

    Example:

    <div id="jd0e473" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # cat <<EOF > config_contrail_operator.yaml
        CONTRAIL_VERSION=2008.121
        CONTRAIL_REGISTRY=hub.juniper.net/contrail
        DOCKER_CONFIG=<this_needs_to_be_generated>
        EOF

    </div>

    </div>

    where:

    -   `CONTRAIL_VERSION` is the Contrail Networking container tag of
        the version of Contrail Networking that you are downloading.

        This procedure is initially supported in Contrail Networking
        Release 2008. You can obtain the Contrail Networking container
        tags for all Contrail Networking 20 releases in [README Access
        to Contrail Networking Registry
        20XX](/documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf)  .

    -   `CONTRAIL_REGISTRY` is the path to the container registry. The
        default Juniper Contrail Container Registry contains the files
        needed for this installation and is located at
        `hub.juniper.net/contrail`.

        If needed, email
        [contrail-registry@juniper.net](mailto:contrail-registry@juniper.net?subject=)
        to obtain your username and password credentials to access the
        Contrail Container registry.

    -   `DOCKER_CONFIG` is the registry secret credential. Set the
        `DOCKER_CONFIG` to registry secret with proper data in base64.

        **Note**

        You can create base64 encoded values using a script. See
        [DOCKER\_CONFIG
        generate](https://github.com/Juniper/contrail-operator/tree/master/deploy/openshift/tools/docker-config-generate).

        To start the script:

        <div id="jd0e518" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            # ./contrail-operator/deploy/openshift/tools/docker-config-generate/generate-docker-config.sh

        </div>

        </div>

        You can copy output generated from the script and use it as the
        `DOCKER_CONFIG` value in this file.

11. <span id="jd0e526">Install Contrail manifests:</span>
    <div id="jd0e529" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # ./contrail-operator/deploy/openshift/install-manifests.sh --dir ./ --config ./config_contrail_operator.yaml

    </div>

    </div>

12. <span id="jd0e532">If your environment has to use a specific NTP
    server, set the environment using the steps in the [Openshift 4.x
    Chrony
    Configuration](https://github.com/Juniper/contrail-operator/blob/R2008/deploy/openshift/docs/chrony-ntp-configuration.md)
    document.</span>

13. <span id="jd0e538">Generate the Ignition configurations:</span>
    <div id="jd0e541" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # openshift-install create ignition-configs

    </div>

    </div>

14. <span id="jd0e544">Copy the Ignition files in the Ignition directory
    for the webserver:</span>
    <div id="jd0e547" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # cp ~/ocp4/*.ign /var/www/html/ignition/
        # restorecon -vR /var/www/html/
        # restorecon -vR /var/lib/tftpboot/
        # chmod o+r /var/www/html/ignition/*.ign

    </div>

    </div>

#### Launch the Virtual Machines

To launch the virtual machines:

1.  <span id="jd0e559">From the hypervisor, use PXE booting to launch
    the virtual machine or machines. If you are using a bare metal
    server, use PXE booting to boot the servers.</span>

2.  <span id="jd0e562">Launch the bootstrap virtual machine:</span>

    <div id="jd0e565" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:60:72:67 --name ocp4-bootstrap --ram=8192 --vcpus=4 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-bootstrap.qcow2,size=120 --vnc

    </div>

    </div>

    The following actions occur as a result of this step:

    -   a bootstrap node virtual machine is created.

    -   the bootstrap node VM is connected to the PXE server. The PXE
        server is our helper node.

    -   an IP address is assigned from DHCP.

    -   A Red Hat Enterprise Linux CoreOS (RHCOS) image is downloaded
        from the HTTP server.

    The ignition file is embedded at the end of the installation
    process.

3.  <span id="jd0e585">Use SSH to run the helper RSA:</span>
    <div id="jd0e588" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # ssh -i ~/.ssh/helper_rsa core@192.168.7.20

    </div>

    </div>

4.  <span id="jd0e591">Review the logs:</span>
    <div id="jd0e594" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        journalctl -f

    </div>

    </div>

5.  <span id="jd0e597">On the bootstrap node, a temporary etcd and
    bootkube is created.</span>

    You can monitor these services when they are running by entering the
    <span class="kbd user-typing" v-pre="">sudo crictl ps</span>
    command.

    <div id="jd0e605" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        [core@bootstrap ~]$ sudo crictl ps
        CONTAINER      IMAGE         CREATED             STATE    NAME                            POD ID
        33762f4a23d7d  976cc3323...  54 seconds ago      Running  manager                         29a...
        ad6f2453d7a16  86694d2cd...  About a minute ago  Running  kube-apiserver-insecure-readyz  4cd...
        3bbdf4176882f  quay.io/...   About a minute ago  Running  kube-scheduler                  b3e...
        57ad52023300e  quay.io/...   About a minute ago  Running  kube-controller-manager         596...
        a1dbe7b8950da  quay.io/...   About a minute ago  Running  kube-apiserver                  4cd...
        5aa7a59a06feb  quay.io/...   About a minute ago  Running  cluster-version-operator        3ab...
        ca45790f4a5f6  099c2a...     About a minute ago  Running  etcd-metrics                    081...
        e72fb8aaa1606  quay.io/...   About a minute ago  Running  etcd-member                     081...
        ca56bbf2708f7  1ac19399...   About a minute ago  Running  machine-config-server           c11...

    </div>

    </div>

    **Note**

    Output modified for readability.

6.  <span id="jd0e614">From the hypervisor, launch the VMs on the
    primary nodes:</span>

    <div id="jd0e617" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:e7:9d:67 --name ocp4-master0 --ram=40960 --vcpus=8 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-master0.qcow2,size=250 --vnc
        # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:80:16:23 --name ocp4-master1 --ram=40960 --vcpus=8 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-master1.qcow2,size=250 --vnc
        # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:d5:1c:39 --name ocp4-master2 --ram=40960 --vcpus=8 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-master2.qcow2,size=250 --vnc

    </div>

    </div>

    You can login to the primary nodes from the helper node after the
    primary nodes have been provisioned:

    <div id="jd0e622" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # ssh -i ~/.ssh/helper_rsa core@192.168.7.21
        # ssh -i ~/.ssh/helper_rsa core@192.168.7.22
        # ssh -i ~/.ssh/helper_rsa core@192.168.7.23

    </div>

    </div>

    Enter the <span class="kbd user-typing" v-pre="">sudo crictl
    ps</span> at any point to monitor pod creation as the VMs are
    launching.

#### Monitor the Installation Process and Delete the Bootstrap Virtual Machine

To monitor the installation process:

1.  <span id="jd0e639">From the helper node, navigate to the `~/ocp4`
    directory.</span>

2.  <span id="jd0e645">Track the install process log:</span>

    <div id="jd0e648" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # openshift-install wait-for bootstrap-complete --log-level debug

    </div>

    </div>

    Look for the `DEBUG Bootstrap status: complete` and the
    `INFO It is now safe to remove the bootstrap resources` messages to
    confirm that the installation is complete.

    <div id="jd0e659" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        INFO Waiting up to 30m0s for the Kubernetes API at https://api.ocp4.example.com:6443...
        INFO API v1.13.4+838b4fa up
        INFO Waiting up to 30m0s for bootstrapping to complete...
        DEBUG Bootstrap status: complete
        INFO It is now safe to remove the bootstrap resources

    </div>

    </div>

    Do not proceed to the next step until you see these messages.

3.  <span id="jd0e669">From the hypervisor, delete the bootstrap VM and
    launch the worker nodes.</span>
    <div id="jd0e672" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:f4:26:a1 --name ocp4-worker0 --ram=16384 --vcpus=4 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-worker0.qcow2,size=120 --vnc

        # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:82:90:00 --name ocp4-worker1 --ram=16384 --vcpus=4 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-worker1.qcow2,size=120 --vnc

    </div>

    </div>

#### Finish the Installation

To finish the installation:

1.  <span id="jd0e684">Login to your Kubernetes cluster:</span>
    <div id="jd0e687" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # export KUBECONFIG=/root/ocp4/auth/kubeconfig

    </div>

    </div>

2.  <span id="jd0e690">Your installation might be waiting for worker
    nodes to approve the certificate signing request (CSR). The
    machineconfig node approval operator typically handles CSR
    approval.</span>

    CSR approval, however, sometimes has to be performed manually.

    To check pending CSRs:

    <div id="jd0e697" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # oc get csr

    </div>

    </div>

    To approve all pending CSRs:

    <div id="jd0e702" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs oc adm certificate approve

    </div>

    </div>

    You may have to approve all pending CSRs multiple times, depending
    on the number of worker nodes in your environment and other factors.

    To monitor incoming CSRs:

    <div id="jd0e709" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # watch -n5 oc get csr

    </div>

    </div>

    Do not move to the next step until incoming CSRs have stopped.

3.  <span id="jd0e714">Set your cluster management state to
    `Managed`:</span>
    <div id="jd0e720" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # oc patch configs.imageregistry.operator.openshift.io cluster --type merge --patch '{"spec":{"managementState":"Managed"}}'

    </div>

    </div>

4.  <span id="jd0e723">Setup your registry storage.</span>

    For most environments, see [Configuring registry storage for bare
    metal](https://docs.openshift.com/container-platform/4.5/installing/installing_bare_metal/installing-bare-metal.html#registry-configuring-storage-baremetal_installing-bare-metal)
    in the Red Hat Openshift documentation.

    For proof of concept labs and other smaller environments, you can
    set storage to `emptyDir`.

    <div id="jd0e736" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # oc patch configs.imageregistry.operator.openshift.io cluster --type merge --patch '{"spec":{"storage":{"emptyDir":{}}}}'

    </div>

    </div>

5.  <span id="jd0e739">If you need to make the registry
    accessible:</span>
    <div id="jd0e742" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # oc patch configs.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"defaultRoute":true}}'

    </div>

    </div>

6.  <span id="jd0e745">Wait for the installation to finish:</span>
    <div id="jd0e748" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # openshift-install wait-for install-complete
        INFO Waiting up to 30m0s for the cluster at https://api.ocp4.example.com:6443 to initialize...
        INFO Waiting up to 10m0s for the openshift-console route to be created...
        INFO Install complete!
        INFO To access the cluster as the system:admin user when using 'oc', run 'export KUBECONFIG=/root/ocp4/auth/kubeconfig'
        INFO Access the OpenShift web-console here: https://console-openshift-console.apps.ocp4.example.com
        INFO Login to the console with user: kubeadmin, password: XXX-XXXX-XXXX-XXXX

    </div>

    </div>

7.  <span id="jd0e754">Add a user to the cluster. See [How to Add a User
    After Completing the
    Installation](how-to-install-contrail-networking-openshift4.html#id-add-a-user).</span>

## How to Install Contrail Networking and Red Hat OpenShift 4.4 on Amazon Web Services

<div class="mini-toc-intro">

Follow these procedures to install Contrail Networking and Red Hat
Openshift 4.4 on Amazon Web Services (AWS):

</div>

-   [When to Use This
    Procedure](how-to-install-contrail-networking-openshift4.html#id-when-to-use-this-procedure-openshift44-aws)

-   [Prerequisites](how-to-install-contrail-networking-openshift4.html#id-prerequisites-openshift44-aws)

-   [Configure
    DNS](how-to-install-contrail-networking-openshift4.html#id-configure-dns)

-   [Configure AWS
    Credentials](how-to-install-contrail-networking-openshift4.html#id-configure-aws-credentials)

-   [Download the OpenShift Installer and the Command Line
    Tools](how-to-install-contrail-networking-openshift4.html#id-download-the-openshift-installer-and-the-command-line-tools)

-   [Deploy the
    Cluster](how-to-install-contrail-networking-openshift4.html#id-deploy-the-cluster)

### When to Use This Procedure

This procedure is used to install Contrail Networking and Red Hat
OpenShift 4.4 orchestration in AWS. Support for Contrail Networking and
Red Hat OpenShift 4.4 environments is introduced in Contrail Networking
Release 2008. See [Contrail Networking Supported
Platforms](https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf)  .

### Prerequisites

This document makes the following assumptions about your environment:

-   the server meets the platform requirements for the installation. See
    [Contrail Networking Supported
    Platforms](https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf)  .

### Configure DNS

A DNS zone must be created and available in Route 53 for your AWS
account before starting this installation. You must also register a
domain for your Contrail cluster in AWS Route 53. All entries created in
AWS Route 53 are expected to be resolvable from the nodes in the
Contrail cluster.

For information on configuring DNS zones in AWS Route 53, see the
`Amazon Route 53 Developer Guide` from AWS.

### Configure AWS Credentials

The installer used in this procedure creates multiple resources in AWS
that are needed to run your cluster. These resources include Elastic
Compute Cloud (EC2) instances, Virtual Private Clouds (VPCs), security
groups, IAM roles, and other necessary network building blocks.

AWS credentials are needed to access these resources and should be
configured before starting this installation.

To configure AWS credentials, see the [Configuration and credential file
settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
section of the [AWS Command Line Interface User
Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
from AWS.

### Download the OpenShift Installer and the Command Line Tools

To download the installer and the command line tools:

1.  <span id="jd0e843">Check which versions of the OpenShift installer
    are available:</span>
    <div id="jd0e846" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ curl -s https://mirror.openshift.com/pub/openshift-v4/clients/ocp/ | \
          awk '{print $5}'| \
          grep -o '4.[0-9].[0-9]*' | \
          uniq | \
          sort | \
          column

    </div>

    </div>

2.  <span id="jd0e849">Set the version and download the OpenShift
    installer and the CLI tool.</span>

    In this example output, the Openshift version is 4.4.20.

    <div id="jd0e854" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ VERSION=4.4.20
        $ wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/$VERSION/openshift-install-mac-$VERSION.tar.gz
        $ wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/$VERSION/openshift-client-mac-$VERSION.tar.gz

        $ tar -xvzf openshift-install-mac-4.4.20.tar.gz -C /usr/local/bin
        $ tar -xvzf openshift-client-mac-4.4.20.tar.gz -C /usr/local/bin

        $ openshift-install version
        $ oc version
        $ kubectl version

    </div>

    </div>

### Deploy the Cluster

To deploy the cluster:

1.  <span id="jd0e866">Generate an SSH private key and add it to the
    agent:</span>
    <div id="jd0e869" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ ssh-keygen -b 4096 -t rsa -f ~/.ssh/id_rsa -N ""

    </div>

    </div>

2.  <span id="jd0e872">Create a working folder:</span>

    In this example, a working folder named `aws-ocp4` is created and
    the user is then moved into the new directory.

    <div id="jd0e880" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ mkdir ~/aws-ocp4 ; cd ~/aws-ocp4

    </div>

    </div>

3.  <span id="jd0e883">Create an installation configuration file. See
    [Creating the installation configuration
    file](https://docs.openshift.com/container-platform/4.5/installing/installing_aws/installing-aws-customizations.html#installation-initializing_installing-aws-customizations)
    section of the [Installing a cluster on AWS with
    customizations](https://docs.openshift.com/container-platform/4.5/installing/installing_aws/installing-aws-customizations.html)
    document from Red Hat OpenShift.</span>

    <div id="jd0e892" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ openshift-install create install-config

    </div>

    </div>

    An `install-config.yaml` file needs to be created and added to the
    current directory. A sample `install-config.yaml` file is provided
    below.

    Be aware of the following factors while creating the
    `install-config.yaml` file:

    -   The `networkType` field is usually set as `OpenShiftSDN` in the
        YAML file by default.

        For configuration pointing at Contrail cluster nodes, the
        `networkType` field needs to be configured as `Contrail`.

    -   OpenShift primary nodes need larger instances. We recommend
        setting the type to `m5.2xlarge` or larger for OpenShift primary
        nodes.

    -   Most OpenShift worker nodes can use the default instance sizes.
        You should consider using larger instances, however, for high
        demand performance workloads.

    -   Many of the installation parameters in the YAML file are
        described in more detail in the [Installation configuration
        parameters](https://docs.openshift.com/container-platform/4.5/installing/installing_aws/installing-aws-customizations.html#installation-configuration-parameters_installing-aws-customizations)
        section of the [Installing a cluster on AWS with
        customizations](https://docs.openshift.com/container-platform/4.5/installing/installing_aws/installing-aws-customizations.html)
        document from Red Hat OpenShift.

    A sample `install-config.yaml` file:

    <div id="jd0e949" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        apiVersion: v1
        baseDomain: ovsandbox.com
        compute:
        - architecture: amd64
          hyperthreading: Enabled
          name: worker
          platform:
            aws:
              rootVolume:
                iops: 2000
                size: 500
                type: io1
              type: m5.4xlarge
          replicas: 3
        controlPlane:
          architecture: amd64
          hyperthreading: Enabled
          name: master
          platform:
            aws:
              rootVolume:
                iops: 4000
                size: 500
                type: io1
              type: m5.2xlarge
          replicas: 3
        metadata:
          creationTimestamp: null
          name: w1
        networking:
          clusterNetwork:
          - cidr: 10.128.0.0/14
            hostPrefix: 23
          machineNetwork:
          - cidr: 10.0.0.0/16
          networkType: Contrail
          serviceNetwork:
          - 172.30.0.0/16
        platform:
          aws:
            region: eu-west-1
        publish: External
        pullSecret: '{"auths"...}'
        sshKey: |
          ssh-rsa ...

    </div>

    </div>

4.  <span id="jd0e952">Create the installation manifests:</span>
    <div id="jd0e955" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # openshift-install create manifests

    </div>

    </div>

5.  <span id="jd0e958">Clone the Contrail operator repository:</span>
    <div id="jd0e961" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ git clone https://github.com/Juniper/contrail-operator.git
        $ git checkout R2008

    </div>

    </div>

6.  <span id="jd0e964">Create the Contrail operator configuration
    file.</span>

    Example:

    <div id="jd0e969" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # cat <<EOF > config_contrail_operator.yaml
        CONTRAIL_VERSION=2008.121
        CONTRAIL_REGISTRY=hub.juniper.net/contrail
        DOCKER_CONFIG=<this_needs_to_be_generated>
        EOF

    </div>

    </div>

    where:

    -   `CONTRAIL_VERSION` is the Contrail Networking container tag of
        the version of Contrail Networking that you are downloading.

        This procedure is initially supported in Contrail Networking
        Release 2008. You can obtain the Contrail Networking container
        tags for all Contrail Networking 20 releases in [README Access
        to Contrail Networking Registry
        20XX](/documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf)  .

    -   `CONTRAIL_REGISTRY` is the path to the container registry. The
        default Juniper Contrail Container Registry contains the files
        needed for this installation and is located at
        `hub.juniper.net/contrail`.

        If needed, email
        [contrail-registry@juniper.net](mailto:contrail-registry@juniper.net?subject=)
        to obtain your username and password credentials to access the
        Contrail Container registry.

    -   `DOCKER_CONFIG` is the registry secret credential. Set the
        `DOCKER_CONFIG` to registry secret with proper data in base64.

        **Note**

        You can create base64 encoded values using a script. See
        [DOCKER\_CONFIG
        generate](https://github.com/Juniper/contrail-operator/tree/master/deploy/openshift/tools/docker-config-generate).

        To start the script:

        <div id="jd0e1014" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            # ./contrail-operator/deploy/openshift/tools/docker-config-generate/generate-docker-config.sh

        </div>

        </div>

        You can copy output generated from the script and use it as the
        `DOCKER_CONFIG` value in this file.

7.  <span id="jd0e1022">Install Contrail manifests:</span>
    <div id="jd0e1025" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        # ./contrail-operator/deploy/openshift/install-manifests.sh --dir ./ --config ./config_contrail_operator.yaml

    </div>

    </div>

8.  <span id="jd0e1028">Create the cluster:</span>
    <div id="jd0e1031" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ openshift-install create cluster --log-level=debug

    </div>

    </div>

    -   Contrail Networking needs to open some networking ports for
        operation within AWS. These ports are opened by adding rules to
        security groups.

        Follow this procedure to add rules to security groups when AWS
        resources are manually created:

        1.  <span id="jd0e1041">Build the Contrail CLI tool for managing
            security group ports on AWS. This tool allows you to
            automatically open ports that are required for Contrail to
            manage security group ports on AWS that are attached to
            Contrail cluster resources.</span>

            To build this tool:

            <div id="jd0e1046" class="sample" dir="ltr">

            <div class="output" dir="ltr">

                go build .

            </div>

            </div>

            After entering this command, you should be in the binary
            contrail-sc-open in your directory. This interface is the
            compiled tool.

        2.  <span id="jd0e1051">Start the tool:</span>
            <div id="jd0e1054" class="sample" dir="ltr">

            <div class="output" dir="ltr">

                ./contrail-sc-open -cluster-name name of your Openshift cluster -region AWS region where cluster is located

            </div>

            </div>

9.  <span id="jd0e1062">When the service router-default is created in
    openshift-ingress, use the following command to patch the
    configuration:</span>
    <div id="jd0e1065" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ oc -n openshift-ingress patch service router-default --patch '{"spec": {"externalTrafficPolicy": "Cluster"}}'

    </div>

    </div>

10. <span id="jd0e1068">Monitor the screen messages.</span>

    Look for the `INFO Install complete!`.

    The final messages from a sample successful installation:

    <div id="jd0e1078" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        INFO Waiting up to 10m0s for the openshift-console route to be created...
        DEBUG Route found in openshift-console namespace: console
        DEBUG Route found in openshift-console namespace: downloads
        DEBUG OpenShift console route is created
        INFO Install complete!
        INFO To access the cluster as the system:admin user when using 'oc', run 'export KUBECONFIG=/Users/ovaleanu/aws1-ocp4/auth/kubeconfig'
        INFO Access the OpenShift web-console here: https://console-openshift-console.apps.w1.ovsandbox.com
        INFO Login to the console with user: kubeadmin, password: XXXxx-XxxXX-xxXXX-XxxxX

    </div>

    </div>

11. <span id="jd0e1081">Access the cluster:</span>
    <div id="jd0e1084" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ export KUBECONFIG=~/aws-ocp4/auth/kubeconfig

    </div>

    </div>

12. <span id="jd0e1087">Add a user to the cluster. See [How to Add a
    User After Completing the
    Installation](how-to-install-contrail-networking-openshift4.html#id-add-a-user).</span>

## How to Add a User After Completing the Installation

The process for adding an Openshift user is identical in KVM or on AWS.

Redhat OpenShift 4.4 supports a single kubeadmin user by default. This
kubeadmin user is used to deploy the initial cluster configuration.

You can use this procedure to create a Custom Resource (CR) to define a
HTTPasswd identity provider.

1.  <span id="jd0e1105">Generate a flat file that contains the user
    names and passwords for your cluster by using the HTPasswd identity
    provider:</span>

    <div id="jd0e1108" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ htpasswd -c -B -b users.htpasswd testuser MyPassword

    </div>

    </div>

    A file called users.httpasswd is created.

2.  <span id="jd0e1113">Define a secret password that contains the
    HTPasswd user file:</span>

    <div id="jd0e1116" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ oc create secret generic htpass-secret --from-file=htpasswd=/root/ocp4/users.htpasswd -n openshift-config

    </div>

    </div>

    This custom resource shows the parameters and acceptable values for
    an HTPasswd identity provider.

    <div id="jd0e1121" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ cat htpasswdCR.yaml
        apiVersion: config.openshift.io/v1
        kind: OAuth
        metadata:
          name: cluster
        spec:
          identityProviders:
          - name: testuser
            mappingMethod: claim
            type: HTPasswd
            htpasswd:
              fileData:
                name: htpass-secret

    </div>

    </div>

3.  <span id="jd0e1127">Apply the defined custom resource:</span>
    <div id="jd0e1130" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ oc create -f htpasswdCR.yaml

    </div>

    </div>

4.  <span id="jd0e1133">Add the user and assign the `cluster-admin `
    role:</span>
    <div id="jd0e1139" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        $ oc adm policy add-cluster-role-to-user cluster-admin testuser

    </div>

    </div>

5.  <span id="jd0e1142">Login using the new user credentials:</span>

    <div id="jd0e1145" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        oc login -u testuser
        Authentication required for https://api.ocp4.example.com:6443 (openshift)
        Username: testuser
        Password:
        Login successful.

    </div>

    </div>

    The kubeadmin user can now safely be removed. See the [Removing the
    kubeadmin
    user](https://docs.openshift.com/container-platform/4.5/authentication/remove-kubeadmin.html)
    document from Red Hat OpenShift.

## How to Install Earlier Releases of Contrail Networking and Red Hat OpenShift

If you have a need to install Contrail Networking with earlier versions
of Red Hat Openshift, Contrail Networking is also supported with Red Hat
Openshift 3.11.

For information on installing Contrail Networking with Red Hat Openshift
3.11, see the following documentation:

-   [Installing a Standalone Red Hat OpenShift Container Platform 3.11
    Cluster with Contrail Using Contrail OpenShift
    Deployer](../configuration/install-openshift-using-anible-311.html)

-   [Installing a Nested Red Hat OpenShift Container Platform 3.11
    Cluster Using Contrail Ansible
    Deployer](../configuration/install-nested-openshift-311-using-anible.html)

 
