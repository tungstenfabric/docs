# Contrail Provisioning using TGZ files

Contrail components are provided as a debian or an rpm package. There are a bunch of packages required for contrail packages installation. Contrail packages and its dependent packages are bundled in tarballs for easy installation.
These tar archives are provided in two flavors, contrail-cloud and contrail-networking. They're basically tar archives containing tar archives of following package groups

###### 1. Contrail Core packages

They are the packages containing core components of Contrail, natively developed and packaged by contrail.

###### 2. Contrail Third-party packages

Installation of contrail packages requires a lot of third-party packages. Such packages are usually available in Upstream repos or in developer's sites.
However there are some cases where a required version or a newer version or a required fix is not available upstream.
Contrail builds such packages with necessary fixes from sources in-house and are bundled in this tar archive

###### 3. Dependent packages

These are upstream packages either contrail is directly depends on or required by dependent packages of contrail packages. They're downloaded from Upstream repos or
developer's site, tested by contrail team.

###### 4. Contrail Openstack packages

Contrail modified openstack packages and openstack packages from Upstream are provided in this tarball.

##### contrail-cloud: (Complete Contrail Solution)
This tar archive contains all packages required for contrail cloud installation, basically a complete version of contrail including all four package groups.

##### contrail-networking: (Without Contrail-Openstack)
This is similar to contrail-cloud tar archive except that it does not contain openstack related packages and contrail installation will presume openstack packages either pre-installed by users or retrieves openstack packages from repos configured by users.


#### Contrail Repos:
Using these tar archives, user can create repos themselves or use contrail provided provisioning scripts to create local repos in the target nodes. Contrail installation presumes all required contrail packages are available during contrail installation.

#### Provisioning and Local Repo Configuration:
Provisioning of contrail components includes below steps

1. Contrail fabric utils installation

2. Testbed configuration

3. Install contrail-installer-packages in all nodes

4. Install Contrail packages

5. Setup contrail roles

##### Contrail-fabric-utils
contrail-fabric-utils package provides necessary scripts to install and provision contrail components. contrail-fabric-utils is contained in contrail-installer-packages.

###### Install contrail-installer-packages

Contrail-installer-packages contains contrail-fabric-utils packages plus third party packages needed for contrail-fabric-utils installation and local repo creation

1. Most recommended way to start contrail installation is to reimage nodes where you're planning to install contrail components. Also do not perform "apt-get upgrade" or "yum upgrade". This will ensure no package dependency issues during installation.

2. Copy contrail-installer-packages to the first node in the cluster. If your installation just involves a single node, contrail-installer-packages can be copied to the single node.

3. Install contrail-installer-packages

   3.1 Ubuntu: 

           dpkg -i /path/to/contrail-installer-packages_\<release\>-\<build-id\>~\<contrail-sku\>_all.deb

   3.2 Redhat/Centos:

           yum localinstall /path/to/contrail-installer-packages-\<release\>-\<build-id\>~\<contrail-sku\>.\<arch\>.rpm

4. Execute /opt/contrail/contrail-installer-packages/setup.sh. setup.sh will create a local repo containing packages required for contrail-fabric-utils and local repo creation as well as installation of contrail-fabric-utils.

###### Testbed configuration
contrail-installer-packages installation followed by setup.sh execution would have installed python-fabric plus contrail-fabric-utils and other dependent packages. Now a testbed.py needs to be configured so contrail components can be installed/provisioned in given nodes based on its roles.

1. Create /opt/contrail/utils/fabfile/testbeds/testbed.py. Please refer to Contrail Wiki on testbed.py configuration

2. Ensure below command is executed in all nodes. This is just to ensure if testbed.py is correctly populated.

        cd /opt/contrail/utils && fab all_command:"uname -r"

Note:

All fab tasks needs to be executed from /opt/contrail/utils directory. All fab tasks are executed from this first node of the cluster which in turn will provision contrail components in all nodes based on its roles.


###### Install contrail-installer-packages in all nodes
As said in previous section, contrail-installer-packages provides packages needed to create local repos and contrail-fabric-utils.
Since contrail-fabric-utils is configured in the first node of the cluster, fab tasks can be used to install contrail-installer-packages in all nodes.

Ubuntu:

        fab install_pkg_all:/path/to/contrail-installer-packages.deb

Redhat/Centos:

        fab install_pkg_all:/path/to/contrail-installer-packages.rpm

Note:

To Execute above command on a specific node:

    fab install_pkg_node:/path/to/contrail-installer-packages.deb,<host-id>

host-id = username@IP-ADDRESS-of-Node


###### Install Contrail packages

Contrail installation and provisioning is carried using fab tasks. A proper configuration of testbed.py would help execute fab tasks as expected.

Execute below command to install contrail components based on its roles defined in testbed.py

    fab install_contrail:/path/to/contrail-cloud.tgz

or for contrail-networking installation, use contrail-networking.tgz file

    fab install_contrail:/path/to/contrail-networking.tgz


Above fab task will mount its sub tar files into a local directory under /opt/contrail and configure it as a local repo to install packages.

Note:

If user preferred a central repo, such repo should have been configured and necessary repos are enabled before above fab task. In such a central repo case, execute below command.

    fab install_contrail


###### Setup contrail roles

Execute below fab task to setup the nodes based on its roles

    fab setup_all





Note:

This wiki just explains provisioning using TGZ. However we suggest to go through our TechWiki to acquire further knowledge on provisioning.
