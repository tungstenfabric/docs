# Upgrading Contrail Networking using In-Place Upgrade Procedure

 **Note**

This procedure can be used for Contrail Networking upgrades to Contrail
Networking Release 2003 or earlier only.

If you are upgrading to Contrail Networking Release 2005 or later using
an in-place upgrade procedure, see [How to Perform a Zero Impact
Contrail Networking Upgrade using
Ansible](../installation/installing-contrail-ansible-ziu.html).

This document provides steps to upgrade Contrail Networking using
in-place upgrade procedure.

The procedure supports incremental model and you can use it to upgrade
from Contrail Networking Release `N-1` to `N`.

**Best Practice**

You must take snapshots of your current system before proceeding with
the upgrade process.

For a list of supported platforms for all Contrail Networking releases,
see [Contrail Networking Supported Platforms
List](https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf)  .

1.  <span id="jd0e36">Update kernel version on all the compute
    nodes.</span>

    `yum -y update kernel*`

    **Note**

    You must not update kernel version if you are upgrading from
    Contrail Networking Release 1910 to Release 1911.

2.  <span id="jd0e45">Update `CONTRAIL_VERSION` and
    `CONTRAIL_CONTAINER_TAG` to the desired version tag in this
    `instances.yml` file.</span>

    Access `CONTRAIL_CONTAINER_TAG` located at [README Access to
    Contrail Networking Registry
    20xx](https://www.juniper.net/documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf)  .

3.  <span id="jd0e65">Run the following commands from
    `contrail-ansible-deployer` directory.</span>

    For Contrail with OpenStack deployment:

    `cd contrail-ansible-deployer`  
    `ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/configure_instances.yml`  
    `ansible-playbook -e orchestrator=openstack -i inventory/ playbooks/install_contrail.yml`

4.  <span id="jd0e82">Reboot the compute node.</span>

5.  <span id="jd0e85">Check the status of Contrail service on the
    compute node.</span>

    All services must be `active` .

    `sudo contrail-status`

The ansible playbook logs are available on the terminal during
execution. You can also access it at `/var/log/ansible.log`.

 
