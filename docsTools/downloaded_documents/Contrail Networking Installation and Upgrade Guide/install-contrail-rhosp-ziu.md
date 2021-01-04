# Updating Contrail Networking using the Zero Impact Upgrade Process in an Environment using Red Hat Openstack

 

<div id="intro">

<div class="mini-toc-intro">

This document provides the steps needed to update a Contrail Networking
deployment that is using Red Hat Openstack as it’s orchestration
platform. The procedure provides a zero impact upgrade (ZIU) with
minimal disruption to network operations.

</div>

</div>

## When to Use This Procedure

This procedure is used to upgrade Contrail Networking when it is running
in environments using RHOSP13.

The procedure in this document has been validated for the following
Contrail Networking upgrade scenarios:

Table 1: Contrail Networking with RHOSP13 Validated Upgrade Scenarios

| Starting Contrail Networking Release | Target Upgraded Contrail Networking Release |
|:-------------------------------------|:--------------------------------------------|
| 1912.L0                              | 1912.L1                                     |
| 1912.L0                              | 2003                                        |
| 2003                                 | 2005                                        |
| 2005                                 | 2008                                        |

A different procedure is followed for upgrading to earlier target
Contrail Networking releases in environments using RHOSP13
orchestration. See [Upgrading Contrail Networking with Red Hat Openstack
13 using ISSU](../configuration/contrail-issu.html).

If you want to use this procedure to upgrade your Contrail Networking
release to other releases, you must engage Juniper Networks professional
services. Contact your Juniper representative for additional
information.

## Prerequisites

This document makes the following assumptions about your environment:

-   A Contrail Networking deployment using Red Hat Openstack version 13
    (RHOSP13) as the orchestration platform is already operational.

-   The overcloud nodes in the RHOSP13 environment have an enabled Red
    Hat Enterprise Linux (RHEL) subscription.

-   Your environment is running Contrail Release 1912 and upgrading to
    Contrail Release 1912-L1 or to Contrail Release 2003 or later.

-   If you are updating Red Hat Openstack simultaneously with Contrail
    Networking, we assume that the undercloud node is updated to the
    latest minor version and that new overcloud images are prepared for
    an upgrade if needed for the upgrade. See the [Upgrading the
    Undercloud](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/keeping_red_hat_openstack_platform_updated/assembly-upgrading_the_undercloud)
    section of the [Keeping Red Hat OpenStack Platform
    Updated](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/keeping_red_hat_openstack_platform_updated/index)
    guide from Red Hat.

    If the undercloud has been updated and a copy of the heat templates
    are used for the deployment, update the copy of the heat template
    from the Red Hat’s core heat template collection at <span
    class="cli"
    v-pre="">/usr/share/openstack-tripleo-heat-templates</span>. See the
    [Understanding Heat
    Templates](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/advanced_overcloud_customization/sect-understanding_heat_templates)
    document from Red Hat for information on this process.

## Before You Begin

We recommend performing these procedures before starting the update:

-   Backup your Contrail configuration database before starting this
    procedure. See [How to Backup and Restore Contrail Databases in JSON
    Format](../../concept/backup-using-json-50.html).

-   Each compute node agent will go down during this procedure, causing
    some compute node downtime. The estimated downtime for a compute
    node varies by environment, but typically took between 12 and 15
    minutes in our testing environments.

    If you have compute nodes with workloads that cannot tolerate this
    downtime, consider migrating workloads or taking other steps to
    accommodate this downtime in your environment.

-   If you are updating Red Hat Openstack simultaneously with Contrail
    Networking, update Red Hat Openstack to the latest minor release
    version and ensure that the new overcloud images are prepared for
    the upgrade. See the [Upgrading the
    Undercloud](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/keeping_red_hat_openstack_platform_updated/assembly-upgrading_the_undercloud)
    section of the [Keeping Red Hat OpenStack Platform
    Updated](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/keeping_red_hat_openstack_platform_updated/index)
    guide from Red Hat for additional information.

    If the undercloud has been updated and a copy of the heat templates
    are used for the deployment, update the Heat templates from Red
    Hat’s core Heat template collection at <span class="cli"
    v-pre="">/usr/share/openstack-tripleo-heat-templates</span>. See the
    [Understanding Heat
    Templates](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/advanced_overcloud_customization/sect-understanding_heat_templates)
    document from Red Hat for additional information.

## Updating Contrail Networking in an Environment using Red Hat Openstack

To update Contrail Networking in an environment that is using Red Hat
Openstack as the orchestration platform:

1.  <span id="jd0e152">Prepare your docker registry. The registry is
    often included in the undercloud, but it can also be a separate
    node.</span>

    Docker registry setup is environment independent. See [Docker
    Registry](https://docs.docker.com/registry/) from Docker for
    additional information on Docker registry setup.

2.  <span id="jd0e160">Backup the Contrail TripleO Heat Templates. See
    [Using the Contrail Heat
    Template](https://www.juniper.net/documentation/en_US/contrail20/topics/task/configuration/heat-template-vnc.html).</span>

3.  <span id="jd0e166">Get the Contrail TripleO Heat Templates
    (Stable/Queens branch) from
    <https://github.com/Juniper/contrail-tripleo-heat-templates>.</span>

4.  <span id="jd0e172">(Optional) Update the Contrail TripleO Puppet
    module to the latest version and prepare Swift Artifacts, as
    applicable.</span>

    Below are sample commands entered in the undercloud:

    <div id="jd0e177" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        [stack@queensa ~]$ mkdir -p ~/usr/share/openstack-puppet/modules/tripleo
        [stack@queensa ~]$ git clone -b stable/queens https://github.com/Juniper/contrail-tripleo-puppet usr/share/openstack-puppet/modules/tripleo
        [stack@queensa ~]$ tar czvf puppet-modules.tgz usr/
        [stack@queensa ~]$ upload-swift-artifacts -c contrail-artifacts -f puppet-modules.tgz

    </div>

    </div>

5.  <span id="jd0e180">Update the parameter `ContrailImageTag` to the
    new version.</span>

    The location of the `ContrailImageTag` variable varies by
    environment. In the most commonly-used environments, this variable
    is set in the `contrail-services.yaml` file.

    You can obtain the `ContrailImageTag` parameter from the [README
    Access to Contrail Registry
    20XX](/documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf)  .

6.  <span id="jd0e202">(Recommended) If you are upgrading to Contrail
    Networking Release 2005 or later, check and, if needed, enable
    kernel vRouter huge page support to support future compute node
    upgrades without rebooting.</span>

    You can enable or verify kernel-mode vRouter huge page support in
    the <span class="kbd user-typing"
    v-pre="">contrail-services.yaml</span> file using either the <span
    class="kbd user-typing" v-pre="">ContrailVrouterHugepages1GB:</span>
    and <span class="kbd user-typing"
    v-pre="">ContrailVrouterHugepages2MB:</span> parameters:

    <div id="jd0e216" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        parameter_defaults:
          …
          ContrailVrouterHugepages1GB: ‘2’

    </div>

    </div>

    <div id="jd0e219" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        parameter_defaults:
          …
         # ContrailVrouterHugepages2MB: ‘1024’

    </div>

    </div>

    Notes about kernel-mode vRouter huge page support in Red Hat
    Openstack environments:

    -   Kernel-mode vRouter huge page support was introduced in Contrail
        Networking Release 2005, and is configured to support 2 1GB huge
        pages by default in Contrail Networking Release 2005 or later.

        A compute node has to be rebooted once for a huge page
        configuration to finalize. After this initial reboot, the
        compute node can perform future Contrail Networking software
        upgrades without rebooting.

        Notably, a compute node in an environment running Contrail
        Networking 2005 or later has not enabled huge page support for
        kernel-mode vRouters until it is rebooted. The 2x1GB huge page
        support configuration is present by default, but it isn’t
        enabled until the compute node is rebooted.

    -   We recommend only using 1GB or 2MB kernel-mode vRouter huge
        pages in most environments. You can, however, simultaneously
        enable 1GB or 2MB kernel-mode vRouter huge pages in Red Hat
        Openstack environments if your environment requires enablement
        of both huge page options.

    -   Changing vRouter huge page configuration settings in a Red Hat
        Openstack environment typically requires a compute node reboot.

        -   1 GB pages: Reboot required.

        -   2 MB: Reboot usually required. The reboot is sometimes
            avoided in environments where memory isn’t highly fragmented
            or the required number of pages can be easily allocated.

    -   We recommend allotting 2GB of memory—either using the default
        1024x2MB huge page size setting or the 2x1GB size setting—for
        huge pages in most environments. Some larger environments might
        require additional huge page memory settings for scale. Other
        huge page size settings should only be set by expert users in
        specialized circumstances.

    -   If the <span class="kbd user-typing"
        v-pre="">ContrailVrouterHugepages1GB:</span> and <span
        class="kbd user-typing"
        v-pre="">ContrailVrouterHugepages2MB:</span> parameters are set
        to empty value in the <span class="kbd user-typing"
        v-pre="">contrail-services.yaml</span> file, vRouter huge pages
        are disabled.

7.  <span id="overcloud-prepare-step">Update the overcloud by entering
    the <span class="cli" v-pre="">openstack overcloud update
    prepare</span> command and include the files that were updated
    during the previous steps with the overcloud update.</span>

    Example:

    <div id="jd0e268" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        openstack overcloud update prepare 
        --templates tripleo-heat-templates/
        --roles-file tripleo-heat-templates/roles_data_contrail_aio.yaml -e
        environment-rhel-registration.yaml -e
        tripleo-heat-templates/extraconfig/pre_deploy/rhel-registration/rhel-registrationresource-registry.yaml -e
        tripleo-heat-templates/environments/contrail/contrail-services.yaml -e
        tripleo-heat-templates/environments/contrail/contrail-net-single.yaml -e
        tripleo-heat-templates/environments/contrail/contrail-plugins.yaml -e
        misc_opts.yaml -e
        contrail-parameters.yaml -e
        docker_registry.yaml

    </div>

    </div>

8.  <span id="jd0e271">Prepare the overcloud nodes that include Contrail
    containers for the update.</span>
    -   Pull the images in the repository onto the overcloud nodes.

        There are multiple methods for performing this step. Commonly
        used methods for performing this operation include using the
        <span class="cli" v-pre="">docker pull</span> command for Docker
        containers and the <span class="cli" v-pre="">openstack
        overcloud container image upload</span> command for Openstack
        containers, or running the <span class="cli"
        v-pre="">tripleo-heat-templates/upload.containers.sh</span> and
        <span class="cli"
        v-pre="">tools/contrail/update\_contrail\_preparation.sh</span>
        scripts.

    -   (Not required in all setups) Provide export variables for the
        script if the predefined values aren’t appropriate for your
        environment. The script location:

        <div id="jd0e295" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            ~/tripleo-heat-templates/tools/contrail/update_contrail_preparation.sh

        </div>

        </div>

        The following variables within the script are particularly
        significant for this upgrade:

        -   <span class="cli"
            v-pre="">CONTRAIL\_NEW\_IMAGE\_TAG</span>—The image tag of
            the target upgrade version of Contrail. The default value is
            <span class="cli" v-pre="">latest</span>.

            If needed, you can obtain this parameter for a specific
            image from the [README Access to Contrail Registry
            20XX](/documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf)  .

            **Note**

            Some older deployments use the <span class="cli"
            v-pre="">CONTRAIL\_IMAGE\_TAG</span> variable in place of
            the <span class="cli"
            v-pre="">CONTRAIL\_NEW\_IMAGE\_TAG</span> variable. Both
            variables are recognized by the <span class="cli"
            v-pre="">update\_contrail\_preparation.sh</span> script and
            perform the same function.

        -   <span class="cli" v-pre="">SSH\_USER</span>—The SSH username
            for logging into overcloud nodes. The default value is <span
            class="cli" v-pre="">heat-admin</span>.

        -   <span class="cli" v-pre="">SSH\_OPTIONS</span>—Custom SSH
            option values.

            The default SSH options for your environment are typically
            pre-defined. You are typically only changing this value if
            you want to customize your update.

        -   <span class="cli" v-pre="">STOP\_CONTAINERS</span>—The list
            of containers that must be stopped before the upgrade can
            proceed. The default value is <span class="cli"
            v-pre="">contrail\_config\_api
            contrail\_analytics\_api</span>.

    -   Run the script:

        **Caution**

        Contrail services stop working when the script starts running.

        <div id="jd0e355" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            ~/tripleo-heat-templates/tools/contrail/update_contrail_preparation.sh

        </div>

        </div>

9.  <span id="jd0e358">Update the Contrail Controller nodes:</span>
    -   Run the <span class="cli" v-pre="">openstack overcloud update
        run</span> command on the first Contrail controller and, if
        needed, on a Contrail Analytics node. The purpose of this step
        is to update one Contrail Controller and one Contrail Analytics
        node to support the environment so the other Contrail
        Controllers and analytics nodes can be updated without incurring
        additional downtime.

        Example:

        <div id="jd0e370" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            openstack overcloud update run --nodes overcloud-contrailcontroller-0

        </div>

        </div>

        Ensure that the contrail status is <span class="cli"
        v-pre="">ok</span> on overcloud-contrailcontroller-0 before
        proceeding.

        If the analytics and the analyticsdb nodes are on separate
        nodes, you may have to update the nodes individually:

        <div id="jd0e380" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            openstack overcloud update run --nodes overcloud-contrailcontroller-0
            openstack overcloud update run --roles ContrailAnalytics,ContrailAnalyticsDatabase

        </div>

        </div>

    -   After the upgrade, check the docker container status and
        versions for the Contrail Controllers and the Contrail Analytics
        and AnalyticsDB nodes.

        <div id="jd0e386" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            docker ps -a

        </div>

        </div>

    -   Update the remaining Contrail Controller nodes:

        Example:

        <div id="jd0e394" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            openstack overcloud update run --nodes overcloud-contrailcontroller-1
            openstack overcloud update run --nodes overcloud-contrailcontroller-2
            openstack overcloud update run --nodes overcloud-contrailcontroller-3
            ...

        </div>

        </div>

10. <span id="jd0e397">Update the Openstack Controllers using the <span
    class="cli" v-pre="">openstack overcloud update run</span>
    commands:</span>

    Example:

    <div id="jd0e405" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        openstack overcloud update run --nodes overcloud-controller-0
        openstack overcloud update run --nodes overcloud-controller-1
        openstack overcloud update run --nodes overcloud-controller-2
        ...

    </div>

    </div>

11. <span id="jd0e408">Individually update the compute
    nodes.**Note**</span>

    The compute node agent will be down during this step. The estimated
    downtime varies by environment, but is typically between 1 and 5
    minutes.

    Consider migrating workloads that can’t tolerate this downtime
    before performing this step

    <div id="jd0e416" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        openstack overcloud update run --nodes overcloud-novacompute-1
        openstack overcloud update run --nodes overcloud-novacompute-2
        openstack overcloud update run --nodes overcloud-novacompute-3
        ...

    </div>

    </div>

    Reboot your compute node to complete the update.

    **Note**

    A reboot is required to complete this procedure only if a kernel
    update is also needed. If you would like to avoid rebooting your
    compute node, check the log files in the <span class="cli"
    v-pre="">/var/log/yum.log</span> file to see if kernel packages were
    updated during the compute node update. A reboot is required only if
    kernel updates occurred as part of the compute node update
    procedure.

    <div id="jd0e427" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        sudo reboot

    </div>

    </div>

    Use the <span class="cli" v-pre="">contrail-status</span> command to
    monitor upgrade status. Ensure all pods reach the `running` state
    and all services reach the `active` state.

    This <span class="cli" v-pre="">contrail-status</span> command
    provides output after a successful upgrade:

    **Note**

    Some output fields and data have been removed from this <span
    class="cli" v-pre="">contrail-status</span> command sample for
    readability.

    <div id="jd0e452" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        Pod             Service        Original Name                     State
        analytics       api            contrail-analytics-api            running
        analytics       collector      contrail-analytics-collector      running
        analytics       nodemgr        contrail-nodemgr                  running
        analytics       provisioner    contrail-provisioner              running
        analytics       redis          contrail-external-redis           running
        analytics-alarm alarm-gen      contrail-analytics-alarm-gen      running
        analytics-alarm kafka          contrail-external-kafka           running
        analytics-alarm nodemgr        contrail-nodemgr                  running
        analytics-alarm provisioner    contrail-provisioner              running
        analytics-alarm zookeeper      contrail-external-zookeeper       running
        analytics-snmp  nodemgr        contrail-nodemgr                  running
        analytics-snmp  provisioner    contrail-provisioner              running
        analytics-snmp  snmp-collector contrail-analytics-snmp-collector running
        analytics-snmp  topology       contrail-analytics-snmp-topology  running
        config          api            contrail-controller-config-api    running
        <trimmed>

        == Contrail control ==
        control: active
        nodemgr: active
        named: active
        dns: active

        == Contrail analytics-alarm ==
        nodemgr: active
        kafka: active
        alarm-gen: active

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

    </div>

    </div>

12. <span id="jd0e580">Enter the <span class="cli" v-pre="">openstack
    overcloud update converge</span> command to finalize the
    update.**Note**</span>

    The options used in the <span class="cli" v-pre="">openstack
    overcloud update converge</span> in this step will match the options
    used with the <span class="cli" v-pre="">openstack overcloud update
    prepare</span> command entered in
    [7](install-contrail-rhosp-ziu.html#overcloud-prepare-step).

    <div id="jd0e597" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        openstack overcloud update converge 
        --templates tripleo-heat-templates/
        --roles-file tripleo-heat-templates/roles_data_contrail_aio.yaml -e
        environment-rhel-registration.yaml -e
        tripleo-heat-templates/extraconfig/pre_deploy/rhel-registration/rhel-registrationresource-registry.yaml -e
        tripleo-heat-templates/environments/contrail/contrail-services.yaml -e
        tripleo-heat-templates/environments/contrail/contrail-net-single.yaml -e
        tripleo-heat-templates/environments/contrail/contrail-plugins.yaml -e
        misc_opts.yaml -e
        contrail-parameters.yaml -e
        docker_registry.yaml

    </div>

    </div>

    Monitor screen messages indicating `SUCCESS` to confirm that the
    updates made in this step are successful.

 
