.. _how-to-install-tf-networking-and-red-hat-openshift-44:

How to Install Tungsten Fabric and Red Hat OpenShift 4.4
========================================================

:date: 2020-11-12

You can install Tungsten Fabric with Red Hat Openshift 4.4 in
multiple environments.

This document shows one method of installing Red Hat Openshift 4.4 with
Tungsten Fabric in two separate contexts—on a VM running in a KVM
module and within Amazon Web Services (AWS). There are many
implementation and configuration options available for installing and
configuring Red Hat OpenShift 4.4 and the scope of all options is beyond
this document. For additional information on Red Hat Openshift 4.4
implementation options, see the `OpenShift Container Platform 4.4
Documentation <https://docs.openshift.com/container-platform/4.4/welcome/index.html>`__
from Red Hat.

This document includes the following sections:

.. _how-to-install-tf-networking-and-red-hat-openshift-44-using-a-vm-running-in-a-kvm-module:

How to Install Tungsten Fabric and Red Hat OpenShift 4.4 using a VM Running in a KVM Module
-----------------------------------------------------------------------------------------------
This section illustrates how to install Tungsten Fabric with Red Hat
OpenShift 4.4 orchestration, where Tungsten Fabric and Red Hat
Openshift are running on virtual machines (VMs) in a Kernel-based
Virtual Machine (KVM) module. This procedure can also be performed to
configure an environment where Tungsten Fabric and Red Hat OpenShift
4.4 are running on a bare metal server.

When to Use This Procedure
~~~~~~~~~~~~~~~~~~~~~~~~~~

This procedure is used to install Tungsten Fabric and Red Hat
OpenShift 4.4 orchestration on a virtual machine (VM) running in a
Kernel-based Virtual Machine (KVM) module. Support for Tungsten Fabric
installations onto VMs in Red Hat OpenShift 4.4 environments
is introduced in Tungsten Fabric Release 2011. See `Contrail
Networking Supported
Platforms <https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf>`__  .

You can also use this procedure to install Tungsten Fabric and Red
Hat OpenShift 4.4 orchestration on a bare metal server.

This procedure should work with all versions of Openshift 4.4.

Prerequisites
~~~~~~~~~~~~~

This document makes the following assumptions about your environment:

-  the KVM environment is operational.

-  the server meets the platform requirements for the installation. See
   `Tungsten Fabric Supported
   Platforms <https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf>`__  .

-  Minimum server requirements:

   -  Primary nodes: 8 CPU, 40GB RAM, 250GB SSD storage

   -  Backup nodes: 4 CPU, 16GB RAM, 120GB SSD storage

   -  Helper node: 4 CPU, 8GB RAM, 30GB SSD storage

-  In single node deployments, do not use spinning disk arrays with low
   Input/Output Operations Per Second (IOPS) when using Tungsten Fabric
   with Red Hat Openshift. Higher IOPS disk arrays are
   required because the control plane always operates as a high
   availability setup in single node deployments.

   IOPS requirements vary by environment due to multiple factors beyond
   Tungsten Fabric and Red Hat Openshift. We, therefore, provide
   this guideline but do not provide direct guidance around IOPS
   requirements.

.. _install-tf-networking-and-red-hat-openshift-44:

Install Tungsten Fabric and Red Hat Openshift 4.4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Perform these steps to install Tungsten Fabric and Red Hat OpenShift
4.4 using a VM running in a KVM module:
Create a Virtual Network or a Bridge Network for the Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a virtual network or a bridge network for the installation:

1. Log onto the server that will host the VM that will run Tungsten Fabric.

   Download the ``virt-net.xml`` virtual network configuration file from
   the Red Hat repository.

   ::

      # wget https://raw.githubusercontent.com/RedHatOfficial/ocp4-helpernode/master/docs/examples/virt-net.xml

2. Create a virtual network using the ``virt-net.xml`` file.

   You may need to modify your virtual network for your environment.

   *Example:*

   ::

      # virsh net-define --file virt-net.xml

3. Set the OpenShift 4.4 virtual network to autostart on bootup:

   ::

      # virsh net-autostart openshift4
      # virsh net-start openshift4

Create a Helper Node with a Virtual Machine Running CentOS 7 or 8
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This procedure requires a helper node with a virtual machine that is
running either CentOS 7 or 8.

To create this helper node:

1. Download the Kickstart file for the helper node from the Red Hat
   repository:

   *CentOS 8*

   ::

      # wget https://raw.githubusercontent.com/RedHatOfficial/ocp4-helpernode/master/docs/examples/helper-ks8.cfg -O helper-ks.cfg

   *CentOS 7*

   ::

      # wget https://raw.githubusercontent.com/RedHatOfficial/ocp4-helpernode/master/docs/examples/helper-ks.cfg -O helper-ks.cfg

2. If you haven’t already configured a root password and the NTP server
   on the helper node, enter the following commands:

   *Example Root Password*

   ::

      rootpw --plaintext password

   *Example NTP Configuration*

   ::

      timezone America/Los_Angeles --isUtc --ntpservers=0.centos.pool.ntp.org,1.centos.pool.ntp.org,2.centos.pool.ntp.org,3.centos.pool.ntp.org

3. Edit the ``helper-ks.cfg`` file for your environment and use it to
   install the helper node.

   The following examples show how to install the helper node without
   having to take further actions:

   *CentOS 8*

   ::

      # virt-install --name="ocp4-aHelper" --vcpus=2 --ram=4096 \
      --disk path=/var/lib/libvirt/images/ocp4-aHelper.qcow2,bus=virtio,size=50 \
      --os-variant centos8 --network network=openshift4,model=virtio \
      --boot hd,menu=on --location /var/lib/libvirt/iso/CentOS-8.2.2004-x86_64-dvd1.iso \
      --initrd-inject helper-ks.cfg --extra-args "inst.ks=file:/helper-ks.cfg" --noautoconsole

   *CentOS 7*

   ::

      # virt-install --name="ocp4-aHelper" --vcpus=2 --ram=4096 \
      --disk path=/var/lib/libvirt/images/ocp4-aHelper.qcow2,bus=virtio,size=30 \
      --os-variant centos7.0 --network network=openshift4,model=virtio \
      --boot hd,menu=on --location /var/lib/libvirt/iso/CentOS-7-x86_64-Minimal-2003.iso \
      --initrd-inject helper-ks.cfg --extra-args "inst.ks=file:/helper-ks.cfg" --noautoconsole

   The helper node is installed with the following settings, which are
   pulled from the ``virt-net.xml`` file:

   -  HELPER_IP: 192.168.7.77

   -  NetMask: 255.255.255.0

   -  Default Gateway: 192.168.7.1

   -  DNS Server: 8.8.8.8

4. Monitor the helper node installation progress in the viewer:

   ::

      # virt-viewer --domain-name ocp4-aHelper

   When the installation process is complete, the helper node shuts off.

5. Start the helper node:

   ::

      # virsh start ocp4-aHelper

Prepare the Helper Node
^^^^^^^^^^^^^^^^^^^^^^^

To prepare the helper node after the helper node installation:

1. Login to the helper node:

   ::

      # ssh -l root HELPER_IP

   **Note**

   The default ``HELPER_IP``, which was pulled from the ``virt-net.xml``
   file, is 192.168.7.77.

2. Install Enterprise Linux and update CentOS.

   ::

      # yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(rpm -E %rhel).noarch.rpm
      # yum -y update

3. Install Ansible and Git and clone the ``helpernode`` repository onto
   the helper node.

   ::

      # yum -y install ansible git
      # git clone https://github.com/RedHatOfficial/ocp4-helpernode
      # cd ocp4-helpernode

4. Copy the vars.yaml file into the top-level directory:

   ::

      # cp docs/examples/vars.yaml .

   Review the vars.yml file. Consider changing any value that requires
   changing in your environment.

   The following values should be reviewed especially carefully:

   -  The domain name, which is defined using the ``domain:`` parameter
      in the ``dns:`` hierarchy. If you are using local DNS servers,
      modify the forwarder parameters—``forwarder1:`` and
      ``forwarder2:`` are used in this example—to connect to these DNS
      servers.

   -  Hostnames for primary and worker nodes. Hostnames are defined
      using the ``name:`` parameter in either the ``primaries:`` or
      ``workers:`` hierarchies.

   -  IP and DHCP settings. If you are using a custom bridge network,
      modify the IP and DHCP settings accordingly.

   -  VM and BMS settings.

      If you are using a VM, set the ``disk:`` parameter as
      ``disk: vda``.

      If you are using a BMS, set the ``disk:`` parameter as
      ``disk: sda``.

   A sample vars.yml file:

   ::

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

5. Review the ``vars/main.yml`` file to ensure the file reflects the
   correct version of Red Hat OpenShift. If you need to change the Red
   Hat Openshift version in the file, change it.

   In the following sample ``main.yml`` file, Red Hat Openshift 4.4.21
   is installed:

   ::

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

6. Run the playbook to setup the helper node:

   ::

      # ansible-playbook -e @vars.yaml tasks/main.yml

7. After the playbook is run, gather information about your environment
   and confirm that all services are active and running:

   ::

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

Create the Ignition Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create Ignition configurations:

1.  On your hypervisor and helper nodes, check that your NTP server is
    properly configured in the ``/etc/chrony.conf`` file:

    ::

       chronyc tracking

    The installation fails with a
    ``X509: certificate has expired or is not yet valid`` message when
    NTP is not properly configured.

2.  Create a location to store your pull secret objects:

    ::

       # mkdir -p ~/.openshift

3.  From `Get Started with Openshift <https://www.openshift.com/try>`__
    website, download your pull secret and save it in the
    ``~/.openshift/pull-secret`` directory.

    ::

       # ls -1 ~/.openshift/pull-secret
       /root/.openshift/pull-secret

4.  An SSH key is created for you in the ``~/.ssh/helper_rsa`` directory
    after completing the previous step. You can use this key or create a
    unique key for authentication.

    ::

       # ls -1 ~/.ssh/helper_rsa
       /root/.ssh/helper_rsa

5.  Create an installation directory.

    ::

       # mkdir ~/ocp4
       # cd ~/ocp4

6.  Create an install-config.yaml file.

    An example file:

    ::

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

7.  Create the installation manifests:

    ::

       # openshift-install create manifests

8.  Set the mastersSchedulable: variable to false in the
    ``manifests/cluster-scheduler-02-config.yml`` file.

    ::

       # sed -i 's/mastersSchedulable: true/mastersSchedulable: false/g' manifests/cluster-scheduler-02-config.yml

    A sample cluster-scheduler-02-config.yml file after this
    configuration change:

    ::

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

    This configuration change is needed to prevent pods from being
    scheduled on control plane machines.

9.  Clone the TF operator repository:

    ::

       # git clone https://github.com/Juniper/contrail-operator.git
       # git checkout R2008

10. Create the TF operator configuration file.

    Example:

    ::

       # cat <<EOF > config_contrail_operator.yaml
       CONTRAIL_VERSION=2008.121
       CONTRAIL_REGISTRY=hub.juniper.net/contrail
       DOCKER_CONFIG=<this_needs_to_be_generated>
       EOF

    where:

    -  ``CONTRAIL_VERSION`` is the Tungsten Fabric container tag of
       the version of Tungsten Fabric that you are downloading.

       This procedure is initially supported in Tungsten Fabric
       Release 2008. You can obtain the Tungsten Fabric container
       tags for all Tungsten Fabric 20 releases in `README Access to
       Tungsten Fabric Registry
       20XX </documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf>`__  .

    -  ``CONTRAIL_REGISTRY`` is the path to the container registry. The
       default Juniper Contrail Container Registry contains the files
       needed for this installation and is located at
       ``hub.juniper.net/contrail``.

       If needed, email contrail-registry@juniper.net to obtain your
       username and password credentials to access the Contrail
       Container registry.

    -  ``DOCKER_CONFIG`` is the registry secret credential. Set the
       ``DOCKER_CONFIG`` to registry secret with proper data in base64.

       **Note**

       You can create base64 encoded values using a script. See
       `DOCKER_CONFIG
       generate <https://github.com/Juniper/contrail-operator/tree/master/deploy/openshift/tools/docker-config-generate>`__.

       To start the script:

       ::

          # ./contrail-operator/deploy/openshift/tools/docker-config-generate/generate-docker-config.sh

       You can copy output generated from the script and use it as the
       ``DOCKER_CONFIG`` value in this file.

11. Install TF manifests:

    ::

       # ./contrail-operator/deploy/openshift/install-manifests.sh --dir ./ --config ./config_contrail_operator.yaml

12. If your environment has to use a specific NTP server, set the
    environment using the steps in the `Openshift 4.x Chrony
    Configuration <https://github.com/Juniper/contrail-operator/blob/R2008/deploy/openshift/docs/chrony-ntp-configuration.md>`__
    document.

13. Generate the Ignition configurations:

    ::

       # openshift-install create ignition-configs

14. Copy the Ignition files in the Ignition directory for the webserver:

    ::

       # cp ~/ocp4/*.ign /var/www/html/ignition/
       # restorecon -vR /var/www/html/
       # restorecon -vR /var/lib/tftpboot/
       # chmod o+r /var/www/html/ignition/*.ign

Launch the Virtual Machines
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To launch the virtual machines:

1. From the hypervisor, use PXE booting to launch the virtual machine or
   machines. If you are using a bare metal server, use PXE booting to
   boot the servers.

2. Launch the bootstrap virtual machine:

   ::

      # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:60:72:67 --name ocp4-bootstrap --ram=8192 --vcpus=4 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-bootstrap.qcow2,size=120 --vnc

   The following actions occur as a result of this step:

   -  a bootstrap node virtual machine is created.

   -  the bootstrap node VM is connected to the PXE server. The PXE
      server is our helper node.

   -  an IP address is assigned from DHCP.

   -  A Red Hat Enterprise Linux CoreOS (RHCOS) image is downloaded from
      the HTTP server.

   The ignition file is embedded at the end of the installation process.

3. Use SSH to run the helper RSA:

   ::

      # ssh -i ~/.ssh/helper_rsa core@192.168.7.20

4. Review the logs:

   ::

      journalctl -f

5. On the bootstrap node, a temporary etcd and bootkube is created.

   You can monitor these services when they are running by entering the
   sudo crictl ps command.

   ::

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

   **Note**

   Output modified for readability.

6. From the hypervisor, launch the VMs on the primary nodes:

   ::

      # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:e7:9d:67 --name ocp4-master0 --ram=40960 --vcpus=8 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-master0.qcow2,size=250 --vnc
      # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:80:16:23 --name ocp4-master1 --ram=40960 --vcpus=8 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-master1.qcow2,size=250 --vnc
      # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:d5:1c:39 --name ocp4-master2 --ram=40960 --vcpus=8 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-master2.qcow2,size=250 --vnc

   You can login to the primary nodes from the helper node after the
   primary nodes have been provisioned:

   ::

      # ssh -i ~/.ssh/helper_rsa core@192.168.7.21
      # ssh -i ~/.ssh/helper_rsa core@192.168.7.22
      # ssh -i ~/.ssh/helper_rsa core@192.168.7.23

   Enter the sudo crictl ps at any point to monitor pod creation as the
   VMs are launching.

Monitor the Installation Process and Delete the Bootstrap Virtual Machine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To monitor the installation process:

1. From the helper node, navigate to the ``~/ocp4`` directory.

2. Track the install process log:

   ::

      # openshift-install wait-for bootstrap-complete --log-level debug

   Look for the ``DEBUG Bootstrap status: complete`` and the
   ``INFO It is now safe to remove the bootstrap resources`` messages to
   confirm that the installation is complete.

   ::

      INFO Waiting up to 30m0s for the Kubernetes API at https://api.ocp4.example.com:6443...
      INFO API v1.13.4+838b4fa up
      INFO Waiting up to 30m0s for bootstrapping to complete...
      DEBUG Bootstrap status: complete
      INFO It is now safe to remove the bootstrap resources

   Do not proceed to the next step until you see these messages.

3. From the hypervisor, delete the bootstrap VM and launch the worker
   nodes.

   ::

      # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:f4:26:a1 --name ocp4-worker0 --ram=16384 --vcpus=4 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-worker0.qcow2,size=120 --vnc

      # virt-install --pxe --network bridge=openshift4 --mac=52:54:00:82:90:00 --name ocp4-worker1 --ram=16384 --vcpus=4 --os-variant rhel8.0 --disk path=/var/lib/libvirt/images/ocp4-worker1.qcow2,size=120 --vnc

Finish the Installation
^^^^^^^^^^^^^^^^^^^^^^^

To finish the installation:

1. Login to your Kubernetes cluster:

   ::

      # export KUBECONFIG=/root/ocp4/auth/kubeconfig

2. Your installation might be waiting for worker nodes to approve the
   certificate signing request (CSR). The machineconfig node approval
   operator typically handles CSR approval.

   CSR approval, however, sometimes has to be performed manually.

   To check pending CSRs:

   ::

      # oc get csr

   To approve all pending CSRs:

   ::

      # oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs oc adm certificate approve

   You may have to approve all pending CSRs multiple times, depending on
   the number of worker nodes in your environment and other factors.

   To monitor incoming CSRs:

   ::

      # watch -n5 oc get csr

   Do not move to the next step until incoming CSRs have stopped.

3. Set your cluster management state to ``Managed``:

   ::

      # oc patch configs.imageregistry.operator.openshift.io cluster --type merge --patch '{"spec":{"managementState":"Managed"}}'

4. Setup your registry storage.

   For most environments, see `Configuring registry storage for bare
   metal <https://docs.openshift.com/container-platform/4.5/installing/installing_bare_metal/installing-bare-metal.html#registry-configuring-storage-baremetal_installing-bare-metal>`__
   in the Red Hat Openshift documentation.

   For proof of concept labs and other smaller environments, you can set
   storage to ``emptyDir``.

   ::

      # oc patch configs.imageregistry.operator.openshift.io cluster --type merge --patch '{"spec":{"storage":{"emptyDir":{}}}}'

5. If you need to make the registry accessible:

   ::

      # oc patch configs.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"defaultRoute":true}}'

6. Wait for the installation to finish:

   ::

      # openshift-install wait-for install-complete
      INFO Waiting up to 30m0s for the cluster at https://api.ocp4.example.com:6443 to initialize...
      INFO Waiting up to 10m0s for the openshift-console route to be created...
      INFO Install complete!
      INFO To access the cluster as the system:admin user when using 'oc', run 'export KUBECONFIG=/root/ocp4/auth/kubeconfig'
      INFO Access the OpenShift web-console here: https://console-openshift-console.apps.ocp4.example.com
      INFO Login to the console with user: kubeadmin, password: XXX-XXXX-XXXX-XXXX

7. Add a user to the cluster. See :ref:`How to Add a User`.

.. _how-to-install-tf-networking-and-red-hat-openshift-44-on-amazon-web-services:

How to Install Tungsten Fabric and Red Hat OpenShift 4.4 on Amazon Web Services
-----------------------------------------------------------------------------------
Follow these procedures to install Tungsten Fabric and Red Hat
Openshift 4.4 on Amazon Web Services (AWS):

.. _when-to-use-this-procedure-1:

When to Use This Procedure
~~~~~~~~~~~~~~~~~~~~~~~~~~

This procedure is used to install Tungsten Fabric and Red Hat
OpenShift 4.4 orchestration in AWS. Support for Tungsten Fabric and
Red Hat OpenShift 4.4 environments is introduced in Tungsten Fabric
Release 2008. See `Tungsten Fabric Supported
Platforms <https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf>`__  .

.. _prerequisites-2:

Prerequisites
~~~~~~~~~~~~~

This document makes the following assumptions about your environment:

-  the server meets the platform requirements for the installation. See
   `Tungsten Fabric Supported
   Platforms <https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf>`__  .

Configure DNS
~~~~~~~~~~~~~

A DNS zone must be created and available in Route 53 for your AWS
account before starting this installation. You must also register a
domain for your TF cluster in AWS Route 53. All entries created in
AWS Route 53 are expected to be resolvable from the nodes in the
TF cluster.

For information on configuring DNS zones in AWS Route 53, see the
``Amazon Route 53 Developer Guide`` from AWS.

Configure AWS Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~

The installer used in this procedure creates multiple resources in AWS
that are needed to run your cluster. These resources include Elastic
Compute Cloud (EC2) instances, Virtual Private Clouds (VPCs), security
groups, IAM roles, and other necessary network building blocks.

AWS credentials are needed to access these resources and should be
configured before starting this installation.

To configure AWS credentials, see the `Configuration and credential file
settings <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html>`__
section of the `AWS Command Line Interface User
Guide <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html>`__
from AWS.

Download the OpenShift Installer and the Command Line Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To download the installer and the command line tools:

1. Check which versions of the OpenShift installer are available:

   ::

      $ curl -s https://mirror.openshift.com/pub/openshift-v4/clients/ocp/ | \
        awk '{print $5}'| \
        grep -o '4.[0-9].[0-9]*' | \
        uniq | \
        sort | \
        column

2. Set the version and download the OpenShift installer and the CLI
   tool.

   In this example output, the Openshift version is 4.4.20.

   ::

      $ VERSION=4.4.20
      $ wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/$VERSION/openshift-install-mac-$VERSION.tar.gz
      $ wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/$VERSION/openshift-client-mac-$VERSION.tar.gz

      $ tar -xvzf openshift-install-mac-4.4.20.tar.gz -C /usr/local/bin
      $ tar -xvzf openshift-client-mac-4.4.20.tar.gz -C /usr/local/bin

      $ openshift-install version
      $ oc version
      $ kubectl version

Deploy the Cluster
~~~~~~~~~~~~~~~~~~

To deploy the cluster:

1.  Generate an SSH private key and add it to the agent:

    ::

       $ ssh-keygen -b 4096 -t rsa -f ~/.ssh/id_rsa -N ""

2.  Create a working folder:

    In this example, a working folder named ``aws-ocp4`` is created and
    the user is then moved into the new directory.

    ::

       $ mkdir ~/aws-ocp4 ; cd ~/aws-ocp4

3.  Create an installation configuration file. See `Creating the
    installation configuration
    file <https://docs.openshift.com/container-platform/4.5/installing/installing_aws/installing-aws-customizations.html#installation-initializing_installing-aws-customizations>`__
    section of the `Installing a cluster on AWS with
    customizations <https://docs.openshift.com/container-platform/4.5/installing/installing_aws/installing-aws-customizations.html>`__
    document from Red Hat OpenShift.

    ::

       $ openshift-install create install-config

    An ``install-config.yaml`` file needs to be created and added to the
    current directory. A sample ``install-config.yaml`` file is provided
    below.

    Be aware of the following factors while creating the
    ``install-config.yaml`` file:

    -  The ``networkType`` field is usually set as ``OpenShiftSDN`` in
       the YAML file by default.

       For configuration pointing at TF cluster nodes, the
       ``networkType`` field needs to be configured as ``Contrail``.

    -  OpenShift primary nodes need larger instances. We recommend
       setting the type to ``m5.2xlarge`` or larger for OpenShift
       primary nodes.

    -  Most OpenShift worker nodes can use the default instance sizes.
       You should consider using larger instances, however, for high
       demand performance workloads.

    -  Many of the installation parameters in the YAML file are
       described in more detail in the `Installation configuration
       parameters <https://docs.openshift.com/container-platform/4.5/installing/installing_aws/installing-aws-customizations.html#installation-configuration-parameters_installing-aws-customizations>`__
       section of the `Installing a cluster on AWS with
       customizations <https://docs.openshift.com/container-platform/4.5/installing/installing_aws/installing-aws-customizations.html>`__
       document from Red Hat OpenShift.

    A sample ``install-config.yaml`` file:

    ::

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

4.  Create the installation manifests:

    ::

       # openshift-install create manifests

5.  Clone the TF operator repository:

    ::

       $ git clone https://github.com/Juniper/contrail-operator.git
       $ git checkout R2008

6.  Create the TF operator configuration file.

    Example:

    ::

       # cat <<EOF > config_contrail_operator.yaml
       CONTRAIL_VERSION=2008.121
       CONTRAIL_REGISTRY=hub.juniper.net/contrail
       DOCKER_CONFIG=<this_needs_to_be_generated>
       EOF

    where:

    -  ``CONTRAIL_VERSION`` is the Tungsten Fabric container tag of
       the version of Tungsten Fabric that you are downloading.

       This procedure is initially supported in Tungsten Fabric
       Release 2008. You can obtain the Tungsten Fabric container
       tags for all Tungsten Fabric 20 releases in `README Access to
       Tungsten Fabric Registry
       20XX </documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf>`__  .

    -  ``CONTRAIL_REGISTRY`` is the path to the container registry. The
       default Juniper Contrail Container Registry contains the files
       needed for this installation and is located at
       ``hub.juniper.net/contrail``.

       If needed, email contrail-registry@juniper.net to obtain your
       username and password credentials to access the Contrail
       Container registry.

    -  ``DOCKER_CONFIG`` is the registry secret credential. Set the
       ``DOCKER_CONFIG`` to registry secret with proper data in base64.

       **Note**

       You can create base64 encoded values using a script. See
       `DOCKER_CONFIG
       generate <https://github.com/Juniper/contrail-operator/tree/master/deploy/openshift/tools/docker-config-generate>`__.

       To start the script:

       ::

          # ./contrail-operator/deploy/openshift/tools/docker-config-generate/generate-docker-config.sh

       You can copy output generated from the script and use it as the
       ``DOCKER_CONFIG`` value in this file.

7.  Install TF manifests:

    ::

       # ./contrail-operator/deploy/openshift/install-manifests.sh --dir ./ --config ./config_contrail_operator.yaml

8.  Create the cluster:

    ::

       $ openshift-install create cluster --log-level=debug

    -  Tungsten Fabric needs to open some networking ports for
       operation within AWS. These ports are opened by adding rules to
       security groups.

       Follow this procedure to add rules to security groups when AWS
       resources are manually created:

       1. Build the TF CLI tool for managing security group ports
          on AWS. This tool allows you to automatically open ports that
          are required for TF to manage security group ports on
          AWS that are attached to TF cluster resources.

          To build this tool:

          ::

             go build .

          After entering this command, you should be in the binary
          contrail-sc-open in your directory. This interface is the
          compiled tool.

       2. Start the tool:

          ::

             ./contrail-sc-open -cluster-name name of your Openshift cluster -region AWS region where cluster is located

9.  When the service router-default is created in openshift-ingress, use
    the following command to patch the configuration:

    ::

       $ oc -n openshift-ingress patch service router-default --patch '{"spec": {"externalTrafficPolicy": "Cluster"}}'

10. Monitor the screen messages.

    Look for the ``INFO Install complete!``.

    The final messages from a sample successful installation:

    ::

       INFO Waiting up to 10m0s for the openshift-console route to be created...
       DEBUG Route found in openshift-console namespace: console
       DEBUG Route found in openshift-console namespace: downloads
       DEBUG OpenShift console route is created
       INFO Install complete!
       INFO To access the cluster as the system:admin user when using 'oc', run 'export KUBECONFIG=/Users/ovaleanu/aws1-ocp4/auth/kubeconfig'
       INFO Access the OpenShift web-console here: https://console-openshift-console.apps.w1.ovsandbox.com
       INFO Login to the console with user: kubeadmin, password: XXXxx-XxxXX-xxXXX-XxxxX

11. Access the cluster:

    ::

       $ export KUBECONFIG=~/aws-ocp4/auth/kubeconfig

12. Add a user to the cluster. See :ref:`How to Add a User`.

.. _How to Add a User:

How to Add a User After Completing the Installation
---------------------------------------------------

The process for adding an Openshift user is identical in KVM or on AWS.

Redhat OpenShift 4.4 supports a single kubeadmin user by default. This
kubeadmin user is used to deploy the initial cluster configuration.

You can use this procedure to create a Custom Resource (CR) to define a
HTTPasswd identity provider.

1. Generate a flat file that contains the user names and passwords for
   your cluster by using the HTPasswd identity provider:

   ::

      $ htpasswd -c -B -b users.htpasswd testuser MyPassword

   A file called users.httpasswd is created.

2. Define a secret password that contains the HTPasswd user file:

   ::

      $ oc create secret generic htpass-secret --from-file=htpasswd=/root/ocp4/users.htpasswd -n openshift-config

   This custom resource shows the parameters and acceptable values for
   an HTPasswd identity provider.

   ::

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

3. Apply the defined custom resource:

   ::

      $ oc create -f htpasswdCR.yaml

4. Add the user and assign the ``cluster-admin`` role:

   ::

      $ oc adm policy add-cluster-role-to-user cluster-admin testuser

5. Login using the new user credentials:

   ::

      oc login -u testuser
      Authentication required for https://api.ocp4.example.com:6443 (openshift)
      Username: testuser
      Password:
      Login successful.

   The kubeadmin user can now safely be removed. See the `Removing the
   kubeadmin
   user <https://docs.openshift.com/container-platform/4.5/authentication/remove-kubeadmin.html>`__
   document from Red Hat OpenShift.

How to Install Earlier Releases of Tungsten Fabric and Red Hat OpenShift
------------------------------------------------------------------------

If you have a need to install Tungsten Fabric with earlier versions
of Red Hat Openshift, Tungsten Fabric is also supported with Red Hat
Openshift 3.11.

For information on installing Tungsten Fabric with Red Hat Openshift
3.11, see the following documentation:

-  :ref:`installing-a-standalone-red-hat-openshift-container-platform-311-cluster-with-tf-using-tf-openshift-deployer`

-  :ref:`installing-a-nested-red-hat-openshift-container-platform-311-cluster-using-tf-ansible-deployer`

 
