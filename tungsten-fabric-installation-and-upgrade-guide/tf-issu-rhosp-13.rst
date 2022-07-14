.. _rhosp13-issu:

Upgrading Tungsten Fabric with Red Hat Openstack 13 using ISSU
==================================================================

      This document provides steps to upgrade Tungsten Fabric with
      an in-service software upgrade (ISSU) in an environment using Red
      Hat Openstack Platform 13 (RHOSP13).

 When to Use This Procedure

   Use this procedure to upgrade Tungsten Fabric when it is running
   in environments using RHOSP13.

   This procedure has been validated for the following Tungsten Fabrci upgrades:

   .. container:: table-wrap

      .. container:: tbody

         Table 1: Tungsten Fabric with RHOSP13 Validated Upgrade
         Scenarios

         +----------------------------------+----------------------------------+
         | Starting Tungsten Fabric         | Target Tungsten Fabric           |
         | Release                          | Upgrade Release                  |
         +==================================+==================================+
         | 5.1                              | 1907                             |
         +----------------------------------+----------------------------------+
         | 1907                             | 1908                             |
         +----------------------------------+----------------------------------+
         | 1908                             | 1909                             |
         +----------------------------------+----------------------------------+
         | 1909                             | 1910                             |
         +----------------------------------+----------------------------------+
         | 1910                             | 1911                             |
         +----------------------------------+----------------------------------+
         | 1911                             | 1912                             |
         +----------------------------------+----------------------------------+

   Starting in Tungsten Fabric Releases R2011, use the
   Zero Impact Upgrade (ZIU) procedure to upgrade Tungsten Fabric in
   environments using Red Hat Openstack orchestration. See `Updating
   Tungsten Fabric using the Zero Impact Upgrade Process in an
   Environment using Red Hat
   Openstack <ffu-ziu-rhosp16.1-cn.rst>`.

   .. rubric:: Before you begin
      :name: id-before-you-begin

   -  Obtain the ``ContrailImageTag`` value for your Tungsten Fabric
      release. You can obtain this value from the readme files at the
      following locations:

      -  Tungsten Fabric Release Tags: :ref:`Getting Started with Tungsten Fabric <GettingStarted>`

   -  Enable RHEL subscription for the overcloud nodes.

   -  Enable SSH migration for the Compute nodes if you do not have CEPH
      or alike storage.

      Upgrading the compute nodes requires workload migrations and CEPH
      or alike storage allows VM migration.

      -  Modify ``MigrationSshKey`` value at
         ``~/tripleo-heat-templates/environments/contrail/contrail-services.yaml``
         file.

         The ``MigrationSshKey`` parameter with SSH keys for migration
         is typically provided during the overcloud deployment. The
         parameter is used to pass SSH keys between computes nodes to
         allow a VM to migrate from one compute node to another. The
         ``MigrationSshKey`` parameter is an optional parameter that can
         be added to the contrail-services.yaml file. The parameter is
         not included in the contrail-services.yaml file by default.

         Run the following commands to find out the SSH keys:

         ``(undercloud) [stack@queensa ~]$ cat .ssh/id_rsa``

         ``(undercloud) [stack@queensa ~]$ cat .ssh/id_rsa.pub``

   -  Backup the Tungsten Fabric configuration database.

      See `How to Backup and Restore TF Databases in JSON Format <How to Backup and Restore TF databases in JSON Format>`.

   .. rubric:: Procedure
      :name: id-procedure

   1.  Get TF TripleO Heat Templates (Stable/Queens branch) from
       https://github.com/Juniper/contrail-tripleo-heat-templates.

       Take a back up of the existing directory if you are copying the
       latest directory, ``contrail-tripleo-heat-templates``. You need
       to restore the configuration in ``contrail-net.yaml``,
       ``contrail-services.yaml``, ``compute-nic-config.yaml`` (for
       compute node running kernel mode), and
       ``contrail-dpdk-nic-config.yaml`` (for compute node running dpdk
       mode) files.

   2.  Update TF TripleO Puppet module to the latest version and
       prepare Swift Artifacts, as applicable.

         .. code-block ::

                      (undercloud) [stack@queensa ~]$ mkdir -p ~/usr/share/openstack-puppet/modules/tripleo
                      (undercloud) [stack@queensa ~]$ git clone -b stable/queens https://github.com/Juniper/contrail-tripleo-puppet usr/share/openstack-puppet/modules/tripleo
                      (undercloud) [stack@queensa ~]$ tar czvf puppet-modules.tgz usr/
                      (undercloud) [stack@queensa ~]$ upload-swift-artifacts -c contrail-artifacts -f puppet-modules.tgz

   3.  Prepare docker registry with Tungsten Fabric images. It can
       be undercloud or a separate node.

   4.  Update the version of Red Hat running in the undercloud.

             **Note**
             This procedure updates the version of Red Hat running in
             the undercloud before deploying the Tungsten Fabric Controller 
             In-Service Software Upgrade (ISSU) node in .

             You can deploy the Tungsten Fabric Controller In-Service Software
             Upgrade (ISSU) node before performing this step if there is
             a reason to change the sequence in your environment.

       Before you begin the upgrade process:


       -  If you have updated the undercloud using a copy of the heat
          templates, copy the heat templates from
          ``/usr/share/openstack-tripleo-heat-templates`` to
          ``/home/stack/tripleo-heat-templates``.

       -  Add the new server nodes as bare metal nodes, and run
          introspection on the nodes to make them ready for deployment.

       For details about performing this upgrade process, refer to
       `RedHat Chapter 3. Upgrading the
       undercloud <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/keeping_red_hat_openstack_platform_updated/assembly-upgrading_the_undercloud>`__.


   5.  Deploy the TF Controller In-Service Software Upgrade (ISSU)
       node.

       a. Prepare new server node and create flavor
          ``contrail-controller-issu`` for the ISSU node.
          The hardware requirements for ISSU node is the same as for the
          TF Controller Node.

       b. Prepare the parameters in the yaml file,
          ``~/tripleo-heat-templates/environments/contrail/contrail-issu.yaml``:

          -  ``ContrailIssuSshKey``—Generate and set the ssh keys. You
             require SSH access between ISSU and TF Controller
             nodes.

             ``ContrailIssuSshKey`` is same as ``MigrationSshKey``.

          -  ``ContrailIssuImageTag``—Set the new docker images tag for
             the upgrade procedure.

          -  ``ContrailControllerIssuCount``—Set the required number of
             ISSU nodes. The value can be ``1 or 3`` and is dependent on
             various cluster requirements including cluster size,
             expected upgrade duration, etc.

       c. Update ``ServiceNetMap`` parameter in the
          ``~/tripleo-heat-templates/environments/contrail/contrail-services.yaml``
          file.

          ``ContrailIssuControlNetwork``—Set the same value as
          ``ContrailControlNetwork``. The default value is tenant.

       d. Run ``deploy`` command with all the parameters used for
          deployment and the new environment file.

          .. container:: sample
             :name: jd0e304

             .. container::
                :name: jd0e305

                ``openstack overcloud deploy ...\-e ~/tripleo-heat-templates/environments/contrail/contrail-issu.yaml``

       e. Check the status of Tungsten Fabric service on the ISSU node.

          All services must be ``active`` .

          ``sudo contrail-status``

   6.  Prepare for the upgrade procedure.

       a. Update the parameter ``ContrailImageTag`` to the new version.

          .. container:: sample
             :name: jd0e330

             .. container::
                :name: jd0e331

                ``vi ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml``

       b. Download the new OpenStack container and use the new
          ``overcloud_images.yaml`` environment file which has the new
          containers.

          .. container:: sample
             :name: jd0e339

             .. container::
                :name: jd0e340

                ``openstack overcloud container image prepare \ --push-destination=192.x.x.1:8787  \ --tag-from-label {version}-{release} \ --output-images-file ~/local_registry_images.yaml  \ --namespace=registry.access.redhat.com/rhosp13  \ --prefix=openstack-  \ --tag-from-label {version}-{release}  \ --output-env-file ~/overcloud_images.yaml``

          Upload the OpenStack containers.

          .. container:: sample
             :name: jd0e358

             .. container::
                :name: jd0e359

                ``openstack overcloud container image upload --config-file ~/local_registry_images.yaml``

       c. Run the
          ``openstack overcloud upgrade prepare --stack overcloud --templates ~/tripleo-heat-templates``
          command with all the options from deploy and the ISSU node to
          update the heat templates.

          The files that are updated in this step vary by deployment. In
          the following example, the ``overcloud_images.yaml``,
          ``network-isolation.yaml``, ``contrail-plugins.yaml``,
          ``contrail-services.yaml``, ``contrail-net.yaml``,
          ``contrail-issu.yaml``, and ``roles_data.yam`` are prepared
          for the overcloud update.

          .. container:: sample
             :name: jd0e390

             .. container:: output

                .. code-block ::

                         openstack overcloud upgrade prepare --stack overcloud --templates ~/tripleo-heat-templates \
                          -e ~/overcloud_images.yaml \
                          -e ~/tripleo-heat-templates/environments/network-isolation.yaml \
                          -e ~/tripleo-heat-templates/environments/contrail/contrail-plugins.yaml \
                          -e ~/tripleo-heat-templates/environments/contrail/contrail-services.yaml \
                          -e ~/tripleo-heat-templates/environments/contrail/contrail-net.yaml \
                          -e ~/tripleo-heat-templates/environments/contrail/contrail-issu.yaml \
                          --roles-file ~/tripleo-heat-templates/roles_data.yaml

   7.  Run In-Service Software Upgrade (ISSU) sync.

       a. Make SSH connection to the ISSU node.

                **Note**
                If you have 3 ISSU nodes deployed, you must perform SSH
                operations and run scripts on the same node for the
                entire procedure.

       b. Locate ISSU directory.

          ``cd /etc/contrail/issu``

       c. Pair ISSU node with the old cluster.

          ``./issu_node_pair.sh``

       d. Check the status of tf service on the ISSU node.


                ..code-block ::

                         sudo contrail-status

          The ``config_devicemgr``, ``config_schema``, and
          ``config_svcmonitor`` containers should all be in the
          ``inactive`` state. All other containers should be in the
          ``active`` state.

       e. Run the ISSU ``sync`` container.

          ``./issu_node_sync.sh``

       f. Check ISSU container logs.

          .. container:: sample
             :name: jd0e450

             .. container::
                :name: jd0e451

                ``sudo docker logs issu-run-sync``

             .. container:: output

                .. container:: code-block

                   .. container:: code-body

                      ::

                         Config Sync initiated...
                         Config Sync done...
                         Started runtime sync...
                         Start Compute upgrade…

          .. container:: sample
             :name: jd0e455

             .. container::
                :name: jd0e456

                ``sudo docker exec issu-run-sync cat /var/log/contrail/issu_contrail_run_sync.log``

             .. container:: output

                .. container:: code-block

                   .. container:: code-body

                      ::

                         …
                         2019-02-21 17:03:56,769 SYS_DEBUG Control on node 192.168.206.115 has CID 427885c366a5
                         2019-02-21 17:03:56,875 SYS_INFO Signal sent to process. exit_code = 0, stdout = "[u'427885c366a5\n']", stderr="[]"
                         2019-02-21 17:03:56,878 SYS_INFO Start Compute upgrade...

       g. Restart ``contrail_control_control`` container on all the ISSU
          nodes.

          .. container:: sample
             :name: jd0e466

             .. container::
                :name: jd0e467

                ``openstack server list --name issu -c Networks -f value | cut -d'=' -f2 | xargs -i ssh heat-admin@{} sudo docker restart contrail_control_control``


                **Note**
                The ``issu_node_sync`` script is run in step.

                ISSU nodes are not rebooted during this upgrade
                procedure when these instructions can be precisely
                followed. ISSU node reboots, however, are sometimes
                required in specialized circumstances.

                If an ISSU node is rebooted after step , rerun the ``issu_node_sync`` script:

                .. container:: sample
                   :name: jd0e486

                   .. container:: output

                      .. container:: code-block

                         .. container:: code-body

                            ::

                               ./issu_node_sync

                This script starts the ``issu_node_sync`` container and
                stops the ``config_devicemgr``, ``config_schema``, and
                ``config_svcmonitor`` containers.

                After running the ``issu_node_sync`` script, you can
                verify that the *issu-run-sync* container is active and
                running:

                ``docker ps -a | grep issu-run-sync``

                You must also restart the ``contrail_control_control``
                container on all the ISSU nodes after the
                ``issu_node_sync`` script is run:

                .. container:: sample
                   :name: jd0e522

                   .. container:: output

                      .. container:: code-block

                         .. container:: code-body

                            ::

                               openstack server list --name issu -c Networks -f value | cut -d'=' -f2 | xargs -i ssh heat-admin@{} sudo docker restart contrail_control_control

   8.  Upgrade the Compute nodes.

       Perform these steps on all the Compute Nodes.

       a. Select the Compute node for upgrade and migrate workload from
          it.

          .. container:: sample
             :name: jd0e534

             .. container:: output

                .. container:: code-block

                   .. container:: code-body

                      ::

                         openstack server migrate  --wait instance_<name>
                         openstack server resize --confirm instance_<name>

       b. Verify the migrated instance has ``active`` state.

          .. container:: sample
             :name: jd0e543

             .. container::
                :name: jd0e544

                ``openstack server show instance_<name>``

       c. Upgrade the selected Compute Nodes.

          You can use comma-separated list for the various Compute
          nodes.

          .. container:: sample
             :name: jd0e551

             Run the following commands on the undercloud node:

             .. container::
                :name: jd0e554

                ``nodes=overcloud-novacompute-0;openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml``

             Run the following commands on the undercloud node:

             .. container::
                :name: jd0e558

                ``openstack overcloud upgrade run --nodes $nodes --playbook deploy_steps_playbook.yaml``

       d. If the compute nodes use a new kernel or new system-level
          components after step , perform the following steps:

          i.  Reboot the selected nodes.

          ii. For kernel-mode compute nodes:

              Make SSH connection to the upgrades nodes.

              .. container:: sample
                 :name: jd0e574

                 .. container::
                    :name: jd0e575

                    ``sudo docker stop contrail_vrouter_agentsudo ifdown vhost0sudo docker start contrail-vrouter-kernel-initsudo ifup vhost0sudo docker start contrail_vrouter_agent``

       e. If reboot is not required after step, re-initialize ``vhost0`` interfaces on all the DPDK mode compute nodes.

          Make SSH connection to the upgraded Compute nodes and run the
          following commands:

          .. container:: sample
             :name: jd0e595

             .. container::
                :name: jd0e596

                ``ifdown vhost0ifup vhost0``

       f. Check the status of tf service on the upgraded Compute
          nodes.

          ``sudo contrail-status``

          The status must be ``active``.

   9.  Upgrade Tungsten Fabric Plugins including ``Neutron, Heat,`` etc. on
       OpenStack controllers and connect them to the ISSU node.

       Example for environment with a single OpenStack controller:

       .. container:: sample
          :name: jd0e619

          .. container:: output

             .. container:: code-block

                .. container:: code-body

                   ::

                      nodes=overcloud-controller-0
                      openstack overcloud upgrade run --nodes $nodes  --playbook upgrade_steps_playbook.yaml
                      openstack overcloud upgrade run --nodes $nodes  --playbook deploy_steps_playbook.yaml

       Example for environment with multiple Openstack controllers (3
       controllers shown):

       .. container:: sample
          :name: jd0e624

          .. container:: output

             .. container:: code-block

                .. container:: code-body

                   ::

                      nodes=overcloud-controller-0,overcloud-controller-1,overcloud-controller-2
                      openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml
                      openstack overcloud upgrade run --nodes $nodes --playbook deploy_steps_playbook.yaml

   10. Disconnect the ISSU node from the Tungsten Fabric control plane.

       a. Make SSH connection to ISSU node.

       b. Run the following commands:

          .. container:: sample
             :name: jd0e637

             .. container::
                :name: jd0e638

                ``cd /etc/contrail/issu/./issu_node_sync_post.sh./issu_node_pair.sh del``

       c. Check the status of Tungsten Fabric service on the ISSU node.

          ``sudo contrail-status``

          The status must be ``active`` or ``backup``.

   11. Upgrade the Tungsten Fabric control plane node.

       a. Run the following commands:

          .. container:: sample
             :name: jd0e665

             .. container::
                :name: jd0e666

                ``nodes=overcloud-contrailcontroller-0,overcloud-contrailcontroller-1,overcloud-contrailcontroller-2 openstack overcloud upgrade run --nodes $nodes  --playbook upgrade_steps_playbook.yaml``

             .. container::
                :name: jd0e668

                ``openstack overcloud upgrade run --nodes $nodes  --playbook deploy_steps_playbook.yamlopenstack overcloud upgrade run --nodes $nodes --playbook post_upgrade_steps_playbook.yaml``

       b. Check the status of Tungsten Fabric service on the Tungsten Fabric control
          plane node.

          ``sudo contrail-status``

          The status must be ``active`` or ``backup``.

   12. Upgrade TF Analytics and TF AnalyticsDB nodes:

       Example for an environment with three TF Analytics and
       three TF AnalyticsDB nodes:

       .. container:: sample
          :name: jd0e691

          .. container:: output

             .. container:: code-block

                .. container:: code-body

                   ::

                      nodes=contrailanalytics-0,contrailanalytics-1,contrailanalytics-2,contrailanalyticsdatabase-0,contrailanalyticsdatabase-1,contrailanalyticsdatabase-2
                      openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml
                      openstack overcloud upgrade run --nodes $nodes --playbook deploy_steps_playbook.yaml

   13. Connect the ISSU node to the upgraded TF control plane
       node.

       a. Make SSH connection to the ISSU node.

       b. Pair the ISSU node with upgraded Tungsten Fabric control plane.

          ``cd /etc/contrail/issu./issu_node_pair.sh add pair_with_new``

       c. Sync data with new Tungsten Fabric control plane.

          ``issu_config=issu_revert.conf ./issu_node_sync.sh``

       d. Restart ``control`` container on the upgraded nodes.

          Run the following command from the Director.

          ``openstack server list --name "overcloud-contrailcontroller-" -c Networks -f value | cut -d'=' -f2 | xargs -i ssh heat-admin@{} sudo docker restart contrail_control_control``

   14. Run the post upgrade task on the compute nodes and the Openstack
       controllers.

       .. container:: sample
          :name: jd0e729

          .. container::
             :name: jd0e730

             ``nodes=overcloud-novacompute-0,overcloud-novacompute-1 openstack overcloud upgrade run --nodes $nodes --playbook post_upgrade_steps_playbook.yaml``

          .. container::
             :name: jd0e732

             ``nodes=overcloud-controller-0 openstack overcloud upgrade run --nodes $nodes --playbook post_upgrade_steps_playbook.yaml``

   15. Disconnect ISSU and upgraded TF control plane.

       a. Make SSH connection to ISSU node.
       b. Un-pair ISSU node with the old Tungsten Fabric cluster.

          .. container:: sample
             :name: jd0e744

             .. container:: output

                .. code-block ::

                         cd /etc/contrail/issu/
                         issu_config=issu_revert.conf ./issu_node_sync_post.sh
                         ./issu_node_pair.sh del pair_with_new

   16. Reconnect the OpenStack nodes and Compute nodes to the upgraded
       control plane.

       Run the command with all the parameters from ``deploy``.

       .. container:: sample
          :name: jd0e755

          .. container::
             :name: jd0e756

             ``openstack overcloud upgrade converge  \--stack overcloud \...-e ~/tripleo-heat-templates/environments/contrail/contrail-issu.yaml``

   17. If the nodes use new kernel or new system level components,
       reboot the OpenStack controller and tf controller nodes.

       -  Reboot OpenStack controllers as mentioned in section 5.1 of
          `RedHat Rebooting the
          Overcloud <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/keeping_red_hat_openstack_platform_updated/rebooting-the-overcloud>`__
          chapter.

       -  Reboot controllers one by one.

          | Make SSH connection to each controller and perform sudo
            reboot.
          | You must wait till the node is rebooted and Tungsten Fabric 
            services are up.

          ``sudo contrail-status``

   18. Check the status of Tungsten Fabric service on all the upgrades nodes.

       ``sudo contrail-status``

       The status must be ``active``.

   19. Remove the ISSU node from the cluster.

       ``set ContrailControllerIssuCount: 0``

       Run stack deploy command with all the parameters.

       ``openstack overcloud deploy \…-e ~/tripleo-heat-templates/environments/contrail/contrail-issu.yaml``

   .. rubric:: Troubleshoot
      :name: id-troubleshoot


   .. rubric:: Failed upgrade run command for OpenStack controller
      :name: FailedUpgradeRunCommandForOpenStack-92CE4E9B

   .. rubric:: Problem
      :name: problem

   .. container::

      **Description:** You see the following error:

      .. container:: sample
         :name: jd0e828

         .. container:: output

            .. code-block ::

                     nodes=overcloud-controller-0
                     openstack overcloud upgrade run --nodes $nodes --playbook upgrade_steps_playbook.yaml
                     ...
                     TASK [Enable the cinder_volume cluster resource] *******************************
                     Thursday 25 July 2019  11:38:57 -0400 (0:00:00.887)       0:03:16.905 *********
                     FAILED - RETRYING: Enable the cinder_volume cluster resource (5 retries left).
                     FAILED - RETRYING: Enable the cinder_volume cluster resource (4 retries left).
                     FAILED - RETRYING: Enable the cinder_volume cluster resource (3 retries left).
                     FAILED - RETRYING: Enable the cinder_volume cluster resource (2 retries left).
                     FAILED - RETRYING: Enable the cinder_volume cluster resource (1 retries left).

                     fatal: [overcloud-controller-0]: FAILED! => {"attempts": 5, "changed": false, "error": "Error: resource 'openstack-cinder-volume' is not running on any node\n", "msg": "Failed, to set the resource openstack-cinder-volume to the state enable", "output": "", "rc": 1}

                     PLAY RECAP *********************************************************************
                     overcloud-controller-0     : ok=149  changed=68   unreachable=0    failed=1

                     Thursday 25 July 2019  11:39:31 -0400 (0:00:34.195)       0:03:51.101 *********

      For details, refer to https://access.redhat.com/solutions/4122571.

   .. rubric:: Solution
      :name: solution

   -  Make SSH connection to the OpenStack controller node.

   -  | Run the following command:
      | ``sudo docker rm cinder_volume_init_bundle``

   -  Check if the cinder volume is in failed resources list.

      ``sudo pcs status``

   -  Check if the cinder volume is not in failed resource list.

      ``sudo pcs resource cleanup``

   -  Re-run the upgrade ``run`` command.

   .. rubric:: Failed upgrade run command for any overcloud node
      :name: FailedUpgradeRunCommandForAnyOvercl-92D0DD56

   .. rubric:: Problem
      :name: problem-1

   .. container::

      **Description:** You see the following error:

      .. container:: sample
         :name: jd0e873

         .. container:: output

            .. code-block ::

                     ******************************************************
                     TASK [include_tasks] ***********************************************************
                     Wednesday 02 October 2019 09:21:02 -0400 (0:00:00.448) 0:00:29.101 *****
                     fatal: [overcloud-novacompute-1]: FAILED! => {"msg": "No variable found with this name: Compute_pre_deployments"}NO MORE HOSTS LEFT *******************************************************

   .. rubric:: Solution
      :name: solution-1

   This is a broken default behavior if a variable is missing.

   .. container:: sample
      :name: jd0e879

      Edit the ``tripleo-heat-templates/common/deploy-steps.j2`` to
      apply the following change:

      .. container:: output

         .. code-block ::

                  content_copyzoom_out_map
                  (undercloud) [stack@queensa common]$ diff -U 3 deploy-steps.j2.org deploy-steps.j2
                  --- deploy-steps.j2.org 2019-10-04 09:09:57.414000000 -0400
                  +++ deploy-steps.j2     2019-10-04 09:13:51.120000000 -0400
                  @@ -433,7 +433,7 @@
                                   - include_tasks: deployments.yaml
                                     vars:
                                       force: false
                  -                  with_items: "{{ '{{' }} lookup('vars', tripleo_role_name + '_pre_deployments')|default([]) {{ '}}' }}"
                  +                  with_items: "{{ '{{' }} hostvars[inventory_hostname][tripleo_role_name ~ '_pre_deployments']|default([]) {{ '}}' }}"
                                 tags:
                                   - overcloud
                                   - pre_deploy_steps
                  @@ -521,7 +521,7 @@
                                   - include_tasks: deployments.yaml
                                     vars:
                                       force: false
                  -                  with_items: "{{ '{{' }} lookup('vars', tripleo_role_name + '_post_deployments')|default([]) {{ '}}' }}"
                  +                  with_items: "{{ '{{' }} hostvars[inventory_hostname][tripleo_role_name ~ '_post_deployments']|default([]) {{ '}}' }}"
                                 tags:
                                   - overcloud
                                   - post_deploy_steps

   | After editing the ``deploy-steps.j2``, run the ``prepare`` command
     as given in step
     5.\ .
   | Once it is completed, continue the upgrade procedure where you left
     off.

