How to Perform a Zero Impact Tungsten Fabric Upgrade using the Ansible Deployer
===============================================================================

:date: 2021-01-19

Starting in Tungsten Fabric Release 2005, you can perform a Zero
Impact Upgrade (ZIU) of Tungsten Fabric using the TF Ansible
Deployer container. The Tungsten Fabric Ansible Deployer container image can be
loaded from the Juniper Networks Contrail Container Registry hosted at
``hub.juniper.net/contrail``.

Use the procedure in this document to perform a Zero Impact Upgrade
(ZIU) of Tungsten Fabric using the Tungsten Fabric Ansible Deployer
container. This ZIU allows Tungsten Fabric to upgrade while
sustaining minimal network downtime.

Before you begin:

-  The target release for this upgrade must be Contrail Release 2005 or
   later.

-  You can use this procedure to incrementally upgrade to the next
   Tungsten Fabric release only. For instance, if you are running
   Tungsten Fabric Release 2003 and want to upgrade to the next
   TF Release—which is Tungsten Fabric Release 2005—you can
   use this procedure to perform the upgrade.

   This procedure is not validated for upgrades between releases that
   are two or more releases apart. For instance, it could not be used to
   upgrade from Tungsten Fabric Release 2002 to Tungsten Fabric
   Release 2005.

   For a list of Tungsten Fabric releases in a table that
   illustrates Tungsten Fabric release order, see `Contrail
   Networking Supported
   Platforms <https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf>`__  .

-  The Tungsten Fabric Ansible Deployer container can only be used in CentOS
   environments.

-  Take snapshots of your current configurations before you proceed with
   the upgrade process. For details, refer to :ref:`How to Backup and Restore TF databases in JSON Format`.

This procedure illustrates how to perform a ZIU using the Ansible
deployer container. It includes a representative example of the steps
being performed to upgrade from Tungsten Fabric Release 2005 to
Release 2008.

To perform the ZIU using the Ansible deployer:

1.  Pull the ``contrail-ansible-deployer`` file for the target upgrade
    release. This procedure is typically performed from a TF
    controller running in your environment, but it can also be performed
    from a separate server which has network connectivity to the
    deployment that is being upgraded.

    This procedure shows you how to load a 2008 image from the Juniper
    Networks Contrail Container Registry. You can, however, also change
    the values to load the file from a private registry.

    The Juniper Networks Contrail Container Registry is hosted at
    ``hub.juniper.net/contrail``. If you need the credentials to access
    the registry, email contrail-registry@juniper.net.

    Enter the following commands to pull the
    ``contrail-ansible-deployer`` file from the registry:

    ::

       sudo docker login -u <username> -p <password> hub.juniper.net 
       sudo docker pull hub.juniper.net/contrail/contrail-kolla-ansible-deployer:2008.<contrail_container_tag>

    where:

    -  ``username``—username to access the registry. Email
       contrail-registry@juniper.net if you need to obtain ``username``
       and ``password`` credentials.

    -  ``password``—password to access the registry. Email
       contrail-registry@juniper.net if you need to obtain ``username``
       and ``password`` credentials.

    -  ``contrail_container_tag``—the container tag ID for your target
       Tungsten Fabric release. The ``contrail_container_tag`` for
       any Contrail Release 20 software can be obtained from `README
       Access to Tungsten Fabric Registry
       20xx <https://www.juniper.net/documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf>`__  .

2.  Start the Tungsten Fabric Ansible Deployer:

    ::

       docker run -t --net host -d --privileged --name contrail-kolla-ansible-deployer hub.juniper.net/contrail/contrail-kolla-ansible-deployer:2008.<contrail_container_tag>

3.  Navigate to the ``instances.yaml`` file and open it for editing.

    The ``instances.yaml`` file was used to initially deploy the setup.
    The ``instances.yaml`` can be loaded into the TF Ansible
    Deployer and edited to supported the target upgrade version.

    *TF Release 2008 Target Upgrade Example using VI as the
    editor*:

    ::

       docker cp instances.yaml contrail-kolla-ansible-deployer:/root/contrail-ansible-deployer/config/instances.yaml
       docker exec -it contrail-kolla-ansible-deployer bash
       cd /root/contrail-ansible-deployer/config/
       vi instances.yaml

4.  Update the ``CONTRAIL_CONTAINER_TAG`` to the desired version tag in
    the ``instances.yaml`` file from the existing deployment. The
    ``CONTRAIL_CONTAINER_TAG`` variable is in the
    ``contrail_configuration:`` hierarchy within the ``instances.yaml``
    file.

    The ``CONTRAIL_CONTAINER_TAG`` for any TF Release 20 software
    can be obtained from `README Access to Tungsten Fabric Registry
    20xx <https://www.juniper.net/documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf>`__  .

    Here is an example instances.yml file configuration:

    ::

       contrail_configuration:
         CONTRAIL_CONTAINER_TAG: "2008.121"
         CONFIG_DATABASE_NODEMGR__DEFAULTS__minimum_diskGB: "2"
         DATABASE_NODEMGR__DEFAULTS__minimum_diskGB: "2"
         JVM_EXTRA_OPTS: "-Xms1g -Xmx2g"
         VROUTER_ENCRYPTION: FALSE
         LOG_LEVEL: SYS_DEBUG
         CLOUD_ORCHESTRATOR: kubernetes

5.  Upgrade the control plane by running the ziu.yml playbook file from
    inside the  container.

    -  For Tungsten Fabric Release 2005 to Tungsten Fabric
       Release 2008:

       Upgrade the control plane by running the ``ziu.yml`` playbook
       file.

       sudo -E ansible-playbook -v -e orchestrator=openstack -e
       config_file=instances.yaml playbooks/ziu.yml

    -  For Tungsten Fabric Release 2011 and later:

       Upgrade the control plane by running the controller stage of
       ``ziu.yml`` playbook file.

       sudo -E ansible-playbook -v -e stage=controller -e
       orchestrator=openstack -e config_file=../instances.yaml
       playbooks/ziu.yml

6.  Upgrade the Openstack plugin by running the install_openstack.yml
    playbook file.

    -  For Tungsten Fabric Release 2005 to Tungsten Fabric
       Release 2008:

       sudo -E ansible-playbook -v -e orchestrator=openstack -e
       config_file=instances.yaml playbooks/install_openstack.yml

    -  For Tungsten Fabric Release 2011 and later:

       sudo -E ansible-playbook -v -e stage=openstack -e
       orchestrator=openstack -e config_file=../instances.yaml
       playbooks/ziu.yml

7.  Enter the contrail-status command to monitor upgrade status. Ensure
    all pods reach the ``running`` state and all services reach the
    ``active`` state.

    This contrail-status command provides this output after a successful
    upgrade:

    .. note::

       Some output fields and data have been removed for readability.

    ::

                                       Original
       Pod             Service         Name                                   State
                        redis           contrail-external-redis                running
                        rsyslogd                                               running
       analytics        api             contrail-analytics-api                 running
       analytics        collector       contrail-analytics-collector           running
       analytics        nodemgr         contrail-nodemgr                       running
       analytics        provisioner     contrail-provisioner                   running
       analytics-alarm  alarm-gen       contrail-analytics-alarm-gen           running
       analytics-alarm  kafka           contrail-external-kafka                running
       analytics-alarm  nodemgr         contrail-nodemgr                       running
       analytics-alarm  provisioner     contrail-provisioner                   running
       analytics-snmp   nodemgr         contrail-nodemgr                       running
       analytics-snmp   provisioner     contrail-provisioner                   running
       analytics-snmp   snmp-collector  contrail-analytics-snmp-collector      running
       analytics-snmp   topology        contrail-analytics-snmp-topology       running
       config           api             contrail-controller-config-api         running
       config           device-manager  contrail-controller-config-devicemgr   running
       config           dnsmasq         contrail-controller-config-dnsmasq     running
       config           nodemgr         contrail-nodemgr                       running
       config           provisioner     contrail-provisioner                   running
       config           schema          contrail-controller-config-schema      running
       config           stats           contrail-controller-config-stats       running
       config           svc-monitor     contrail-controller-config-svcmonitor  running
       config-database  cassandra       contrail-external-cassandra            running
       <trimmed>

       vrouter kernel module is PRESENT
       == Contrail control ==
       control: active
       nodemgr: active
       named: active
       dns: active

       == Contrail analytics-alarm ==
       nodemgr: active
       kafka: active
       alarm-gen: active

       == Contrail kubernetes ==
       kube-manager: active

       == Contrail database ==
       nodemgr: active
       query-engine: active
       cassandra: active

       == Contrail analytics ==
       nodemgr: active
       api: active
       collector: active

       == Contrail config-database ==
       nodemgr: active
       zookeeper: active
       rabbitmq: active
       cassandra: active

       == Contrail webui ==
       web: active
       job: active

       == Contrail vrouter ==
       nodemgr: active
       agent: active

       == Contrail analytics-snmp ==
       snmp-collector: active
       nodemgr: active
       topology: active

       == Contrail config ==
       svc-monitor: active
       nodemgr: active
       device-manager: active
       api: active
       schema: active


8.  Migrate workloads VM from one group of compute nodes. Leave them
    uncommented in the instances.yaml file. Comment other computes not
    ready to upgrаde in instances.yaml.

9.  Upgrade compute nodes.

    -  For Tungsten Fabric Release 2005 to Tungsten Fabric
       Release 2008:

       Run the install_contrail.yml playbook file to upgrade the compute
       nodes that were uncommented in the instances.yaml file. Only the
       compute nodes that were left uncommented in step 8
       are upgraded to the target release in this step.

       sudo -E ansible-playbook -v -e orchestrator=openstack -e
       config_file=instances.yaml playbooks/install_contrail.yml

    -  For Tungsten Fabric Release 2011 and later:

       Run the compute stage of ziu.yml playbook file to upgrade the
       compute nodes that were uncommented in the instances.yaml file.
       Only the compute nodes that were left uncommented in step 8
       are upgraded to the target release in this step.

       sudo -E ansible-playbook -v -e stage=compute -e
       orchestrator=openstack -e config_file=../instances.yaml
       playbooks/ziu.yml

10. Repeat Steps 8 and 9 until all compute nodes are upgraded.

You can access the Ansible playbook logs of the upgrade at
``/var/log/ansible.log``.


.. note::
   
   Starting in Tungsten Fabric Release 2005, you can perform a Zero
   Impact Upgrade (ZIU) of Tungsten Fabric using the TF Ansible
   Deployer container.
