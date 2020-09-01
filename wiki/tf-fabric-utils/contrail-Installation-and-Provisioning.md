# Installation and Provisioning Roles

This section describes how to install the Contrail Controller software on multiple servers and 
provision on multiple servers.

# Preinstallation Checklist

This procedure assumes that you have first completed the following procedures:

* All of the servers are time synced.
* All servers can ping from one to another, both on management and on data and control, if part of the system.
* All servers can ssh and scp between one another.
* All host names are resolvable.
* If using CentOS or RHEL, SELinux has been disabled (/etc/sysconfig/selinux).

## Installation Overview

The Contrail Controller is typically installed on multiple servers. The base software image 
is installed on all servers to be used, then provisioning scripts are run that launch role-based 
components of the software.

The roles used for the installed system include:

    cfgm — Runs Contrail configuration manager (config-node)
    collector — Runs monitoring and analytics services
    compute — Runs vRouter service and launches tenant virtual machines (VMs)
    control — Runs the control plane service
    database — Runs analytics and configuration database services
    openstack — Runs OpenStack services such as Nova, Quantum, and the like
    webui — Runs the administrator web-based user interface service

The roles are run on multiple servers in an operating installation. A single node can have multiple roles. 

## Installing the Contrail Packages, Part One (CentOS or Ubuntu)

This procedure provides instructions for installing Contrail packages onto either a CentOS-based system or
an Ubuntu-based system. Ensure that a compatible base operating system has been installed, 
using the installation instructions for that system.

1. Download the appropriate Contrail install packages file 
    
        CentOS: contrail-install-packages-1.xx-xxx~openstack_version.el6.noarch.rpm
        Ubuntu: contrail-install-packages-1.xx-xxx~openstack_version_all.deb

   **Note:** where xx-xxx~openstack_version represents the release number, build number, and OpenStack common 
   version name (such as Havana or Icehouse)
    
2. Copy the downloaded Contrail install package file to /tmp directory on the first config node in your cluster.

        CentOS: scp <id@server>:/path/to/contrail-install-packages-1.x-xxx~openstack_version.el6.noarch.rpm /tmp
        Ubuntu: scp <id@server>:/path/to/contrail-install-packages-1.xx-xxx~openstack_version_all.deb /tmp  

3. Install the Contrail packages,

        CentOS: yum --disablerepo=* localinstall /tmp/contrail-install-packages-1.x-xxx~openstack_version.el6.noarch
        Ubuntu: dpkg -i /tmp/contrail-install-packages-1.xx-xxx~openstack_version_all.deb 

4. Run the setup.sh script. This step will create the Contrail packages repository as well as the Fabric 
utilities (located in /opt/contrail/utils ) needed for provisioning:

        cd /opt/contrail/contrail_packages;   ./setup.sh  

5. Populate the testbed.py definitions file, see Populating the Testbed Definitions File. 

   **Note:** As of Contrail Release 1.10, the Apache ZooKeeper resides on the database node. 
         Because a ZooKeeper ensemble operates most effectively with an uneven number of nodes, 
         it is required to have an uneven number (3, 5, 7, and so on) of database nodes in a Contrail system.

## Populating the Testbed Definitions File

You populate a testbed definitions file, /opt/contrail/utils/fabfile/testbeds/testbed.py, 
with parameters specific to your system, then run the fab commands  as instructed in section: 
Installing the Contrail Packages, Part Two, to launch the role-based installation and provisioning tasks.

You can view example testbed files on any node in the controller at:

    /opt/contrail/utils/fabfile/testbeds/testbed_multibox_example.py for a multiple server system
    /opt/contrail/utils/fabfile/testbeds/testbed_singlebox_example.py for a single server system

[testbed_multibox_example.py](https://github.com/Juniper/contrail-fabric-utils/blob/master/fabfile/testbeds/testbed_multibox_example.py)

[testbed_singlebox_example.py](https://github.com/Juniper/contrail-fabric-utils/blob/master/fabfile/testbeds/testbed_singlebox_example.py) 

For a list of all available Fabric commands,
 
refer to the file /opt/contrail/utils/[README.fabric​](https://github.com/Juniper/contrail-fabric-utils/blob/master/README)​

## Installing the Contrail Packages, Part Two (CentOS or Unbuntu) --- Installing on the Remaining Machines
### Preinstallation Checklist

This procedure assumes that you have first completed the following procedures:

* [Installing the Contrail Packages, Part One (CentOS or Ubuntu)](https://github.com/Juniper/contrail-fabric-utils/wiki/contrail-Installation-and-Provisioning#installing-the-contrail-packages-part-one-centos-or-ubuntu)
* [Populating the Testbed Definitions Files](https://github.com/Juniper/contrail-fabric-utils/wiki/contrail-Installation-and-Provisioning#populating-the-testbed-definitions-file)

Ensure that the testbed.py file has been created and populated with information specific to your cluster at /opt/contrail/utils/fabfile/testbeds.

**Note:** Fab commands are always run from /opt/contrail/utils/.

1. Run Fabric commands to install packages as follows:

        CentOS: /opt/contrail/utils/fab install_pkg_all:/tmp/contrail-install-packages-1.xx-xxx~openstack_version​.el6.noarch.rpm
        Ubuntu: /opt/contrail/utils/fab install_pkg_all:/tmp/contrail-install-packages-1.xx-xxx~openstack_version_all.deb 

2. **Ubuntu:** The recommended Kernel version for Ubuntu based system is 3.13.0-34. Nodes can be upgraded to kernel version 3.13.0-34 using below fabric-utils command​:

        fab  upgrade_kernel_all

   **Note:** This step upgrades the kernel version to 3.13.0-34 in all nodes and performs reboot. 
         Reconnect to perform remaining tasks. ​
    
3. To install the required Contrail packages in each node of the cluster:

        fab install_contrail

   To install Contrail with an already existing OpenStack node provisioned by users:

        fab install_without_openstack    # Script will install nova-compute in the compute node
        or
        fab install_without_openstack:manage_nova_compute=no    # User installs nova-compute in the compute node
    
4. If your installation has multiple interfaces (see Multiple Interface Support), run setup_interface:

        fab setup_interface
    
5. Provision the entire cluster:

        fab setup_all

   To provision Contrail with an existing OpenStack node node provisioned by users, use one of the following:

        fab setup_without_openstack    # Script provisions vrouter and nova-compute services in the compute nodes and the compute nodes are rebooted on completion
        or
        fab setup_without_openstack:manage_nova_compute=no    # Only vrouter services are provisioned, the nova-compute service is not provisioned and compute nodes are rebooted on completion
        or
        fab setup_without_openstack:manage_nova_compute=no,reboot=False    # Only vrouter services are provisioned, the nova-compute service is not provisioned and the compute nodes are not rebooted on completion
