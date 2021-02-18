Upgrading Tungsten Fabric using In-Place Upgrade Procedure
==========================================================

:date: 2021-01-19

.. note::

   This procedure can be used for Tungsten Fabric upgrades to Tungsten Fabric 
   Release 2003 or earlier only.

If you are upgrading to Tungsten Fabric Release 2005 or later using
an in-place upgrade procedure, see `How to Perform a Zero Impact Tungsten Fabric Upgrade using the Ansible Deployer <How to Perform a Zero Impact Tungsten Fabric Upgrade using the Ansible Deployer>`_.

This document provides steps to upgrade Tungsten Fabric using
in-place upgrade procedure.

The procedure supports incremental model and you can use it to upgrade
from Tungsten Fabric Release ``N-1`` to ``N``.

.. tip::

   You must take snapshots of your current system before proceeding with
   the upgrade process.

For a list of supported platforms for all Tungsten Fabric releases,
see `Tungsten Fabric Supported Platforms
List <https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf>`__  .

1. Update kernel version on all the compute nodes.

   ``yum -y update kernel*``

   .. note::

      You must not update kernel version if you are upgrading from Contrail
      Networking Release 1910 to Release 1911.

2. Update ``CONTRAIL_VERSION`` and ``CONTRAIL_CONTAINER_TAG`` to the
   desired version tag in this ``instances.yml`` file.

   Access ``CONTRAIL_CONTAINER_TAG`` located at `README Access to
   Tungsten Fabric Registry
   20xx <https://www.juniper.net/documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf>`__  .

3. Run the following commands from ``contrail-ansible-deployer``
   directory.

   For TF with OpenStack deployment:

   | ``cd contrail-ansible-deployer``
   | ``ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/configure_instances.yml``
   | ``ansible-playbook -e orchestrator=openstack -i inventory/ playbooks/install_contrail.yml``

4. Reboot the compute node.

5. Check the status of Contrail service on the compute node.

   All services must be ``active`` .

   ``sudo contrail-status``

The ansible playbook logs are available on the terminal during
execution. You can also access it at ``/var/log/ansible.log``.

 
