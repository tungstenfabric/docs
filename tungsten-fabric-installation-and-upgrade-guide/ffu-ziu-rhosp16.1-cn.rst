.. _upgrading-contrail-networking-release-19xx-with-rhosp13-to-contrail-networking-release-2011-with-rhosp161:

Upgrading Tungsten Fabric Release 19xx with RHOSP13 to Tungsten Fabric Release 2011 with RHOSP16.1
==========================================================================================================

:data: 2020-12-11

The goal of this topic is to provide a combined procedure to upgrade Red
Hat OpenStack Platform (RHOSP) from RHOSP 13 to RHOSP 16.1 by leveraging
Red Hat Fast Forward Upgrade (FFU) procedure while simultaneously
upgrading Tungsten Fabric from Release 19xx to Release 2011. The
procedure leverages the Zero Impact Upgrade (ZIU) procedure from
TF to minimize the downtime.

The downtime will be reduced by not requiring extra server reboots in
addition to the ones that the RHOSP FFU procedure already requires for
Kernel/RHEL upgrades.

Refer to `Red Hat OpenStack Framework for Upgrades (13
to16.1) <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/pdf/framework_for_upgrades_13_to_16.1/Red_Hat_OpenStack_Platform-16.1-Framework_for_Upgrades_13_to_16.1-en-US.pdf>`__  
documentation for details on RHOSP 13 to RHOSP 16.1 Fast Forward Upgrade
(FFU) procedure of OpenStack Platform environment from one long life
version to the next long life version.

Access ``ContrailImageTag`` located at :ref:`Getting Started with Tungsten Fabric Guide <GettingStarted>`

1. Follow *chapter 2—Planning and preparation for an in-place upgrade*
   through *chapter 8.3— Copying the Leapp data to the overcloud nodes*
   of `Red Hat OpenStack Framework for Upgrades (13
   to16.1) <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/pdf/framework_for_upgrades_13_to_16.1/Red_Hat_OpenStack_Platform-16.1-Framework_for_Upgrades_13_to_16.1-en-US.pdf>`__  
   procedure.

2. Use predictable NIC names for overcloud nodes

   1. Log in to the undercloud as the stack user.

   2. Run the ``playbook-nics.yaml`` playbook on all overcloud nodes.

      $ ansible-playbook -i ~/inventory.yaml playbook-nics.yaml

      The playbook sets the new NIC prefix to em. To set a different NIC
      prefix, set the prefix variable when running the playbook:

      $ ansible-playbook -i ~/inventory.yaml -e prefix="mynic"
      playbook-nics.yaml

   3. Run the ``playbook-nics-vhost0.yaml`` playbook on all overcloud
      compute nodes.

      $ ansible-playbook -i inventory.yaml -l overcloud_Compute
      $my_dir/playbook-nics-vhost0.yaml

      For details, see
      https://github.com/tungstenfabric/tf-deployment-test/blob/master/rhosp/ffu_ziu_13_16/tf_specific/playbook-nics-vhost0.yaml.

   4. Reboot overcloud nodes using the standard reboot procedures. For
      more information, see `Red Hat rebooting
      nodes <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/director_installation_and_usage/sect-rebooting_the_overcloud>`__
      documentation.

3. Follow *chapter 8.5—Copying the Leapp data to the overcloud nodes*
   through *chapter 19.2—Upgrading Controller nodes with external Ceph
   deployments* of `Red Hat OpenStack Framework for Upgrades (13
   to16.1) <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/pdf/framework_for_upgrades_13_to_16.1/Red_Hat_OpenStack_Platform-16.1-Framework_for_Upgrades_13_to_16.1-en-US.pdf>`__  
   procedure.

4. Upgrade compute nodes to OpenStack Platform 16.1.
   
   .. note:: 

      If you are not using the default stack name (overcloud), set your
      stack name with the --stack STACK NAME option replacing STACK NAME
      with the name of your stack.

   1. Source the ``stackrc`` file.

      $ source ~/stackrc

   2. Migrate your instances. For details, see `RedHat Migrating virtual
      machine instances between Compute
      nodes <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/html/instances_and_images_guide/migrating-virtual-machines-between-compute-nodes>`__
      documentation.

   3. Run the upgrade command with the system_upgrade_prepare and
      system_upgrade_run tags.

      $ openstack overcloud upgrade run --stack STACK NAME --tags
      system_upgrade_prepare --limit overcloud-compute-0

      $ openstack overcloud upgrade run --stack STACK NAME --tags
      system_upgrade_run --limit overcloud-compute-0

      To upgrade multiple Compute nodes in parallel, set the --limit
      option to a comma-separated list of nodes that you want to
      upgrade.

   4. Run the upgrade command with no tags to perform Red Hat OpenStack
      Platform upgrade.

      $ openstack overcloud upgrade run --stack STACK NAME --limit
      overcloud-compute-0

5. Follow *chapter 19.4—Synchronizing the overcloud stack* through
   *chapter 21.4—Synchronizing the overcloud stack* of `Red Hat
   OpenStack Framework for Upgrades (13
   to16.1) <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/pdf/framework_for_upgrades_13_to_16.1/Red_Hat_OpenStack_Platform-16.1-Framework_for_Upgrades_13_to_16.1-en-US.pdf>`__  
   procedure to complete the upgrade.

 
