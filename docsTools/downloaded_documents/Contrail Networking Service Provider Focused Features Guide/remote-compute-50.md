# Remote Compute

 

<div id="intro">

<div class="mini-toc-intro">

Contrail Networking supports remote compute, a method of managing a
Contrail deployment across many small distributed data centers
efficiently and cost effectively.

</div>

</div>

## Remote Compute Overview

Remote compute enables the deployment of Contrail Networking in many
small distributed data centers, up to hundreds or even thousands, for
telecommunications point-of-presence (PoPs) or central offices (COs).
Each small data center has only a small number of computes, typically
5-20 in a rack, running a few applications such as video caching,
traffic optimization, and virtual Broadband Network Gateway (vBNG). It
is not cost effective to deploy a full Contrail controller cluster of
nodes of control, configuration, analytics, database, and the like, in
each distributed PoP on dedicated servers. Additionally, manually
managing hundreds or thousands of clusters is not feasible
operationally.

## Remote Compute Features

Remote compute is implemented by means of a subcluster that manages
compute nodes at remote sites to receive configurations and exchange
routes.

The key concepts of Contrail remote compute include:

-   Remote compute employs a subcluster to manage remote compute nodes
    away from the primary data center.

-   The Contrail control cluster is deployed in large centralized data
    centers, where it can remotely manage compute nodes in small
    distributed small data centers.

-   A lightweight version of the controller is created, limited to the
    control node, and the config node, analytics, and analytics database
    are shared across several control nodes.

-   Many lightweight controllers are co-located on a small number of
    servers to optimize efficiency and cost.

-   The control nodes peer with the remote compute nodes by means of
    XMPP and peer with local gateways by means of MP-eBGP.

## Remote Compute Operations

A subcluster object is created for each remote site, with a list of
links to local compute nodes that are represented as vrouter objects,
and a list of links to local control nodes that are represented as BGP
router objects, with an ASN as property.

The subclusters are identified in the provision script. The vrouter and
bgp-router provision scripts take each subcluster as an optional
argument to link or delink with the subcluster object.

It is recommended to spawn the control nodes of the remote cluster in
the primary cluster, and they are IGBP-meshed among themselves within
that subcluster. The control nodes BGP-peer with their respective SDN
gateway, over which route exchange occurs with the primary control
nodes.

Compute nodes in the remote site are provisioned to connect to their
respective control nodes to receive configuration and exchange routes.
Data communication among workloads between these clusters occurs through
the provider backbone and their respective SDN gateways. The compute
nodes and the control nodes push analytics data to analytics nodes
hosted on the primary cluster.

### Subcluster Properties

The Contrail Web UI shows a list of subcluster objects, each with a list
of associated vrouters and BGP routers that are local in that remote
site and the ASN property.

General properties of subclusters include:

-   A subcluster control node never directly peers with another
    subcluster control node or with primary control nodes.

-   A subcluster control node has to be created, and is referred to, in
    virtual-router and bgp-router objects.

-   A subcluster object and the control nodes under it should have the
    same ASN.

-   The ASN cannot be modified in a subcluster object.

**Note**

Multinode service chaining across subclusters is not supported.

## Inter Subcluster Route Filtering

<span id="jd0e85">Contrail Networking Release 2005 supports inter
subcluster route filtering (Beta).</span> With this release, a new
extended community called `origin-sub-cluster` (similar to `origin-vn`)
is added to all routes originating from a subcluster.

The format of this new extended community is
`subcluster:<``asn``>:<``id``>`.

This new extended community is added by encoding the subcluster ID in
the ID field within the extended community. The subcluster ID helps you
determine the subcluster from which the route originated, and is unique
for each subcluster. For a 2-byte ASN format, type/subtype is 0x8085 and
subcluster ID can be 4-byte long. For a 4-byte ASN format, type/subtype
is 0x8285 and subcluster ID can be 2-byte long.

You create a routing policy matching this new extended community to be
able to filter routes. Routing policies are always applied to primary
routes. However, a routing policy is applied to a secondary route in the
following scenarios:

-   There is no subcluster extended community associated with the route.

-   Self subcluster ID does not match the subcluster ID associated with
    the route.

[Figure 1](remote-compute-50.html#subcluster) shows a data center
network topology. All routing policies are configured on virtual
networks in the main data center, POP0. Consider the following example
routing policy:

<div id="jd0e124" class="sample" dir="ltr">

<div id="jd0e125" dir="ltr">

`From 0/0 & subcluster:<asn>:1 then LP=150`

</div>

<div id="jd0e127" dir="ltr">

`From 0/0 & subcluster:<asn>:2  then LP=140`

</div>

<div id="jd0e129" dir="ltr">

`From 0/0 then reject `

</div>

Where, `1` and `2` are the subcluster IDs of subclusters POP1 and POP2
respectively.

</div>

In this example, for routes directed to POP0 from subclusters POP1 and
POP2, the LP will be changed. Routes that do not match the extended
community are rejected. Default routes with no extended community are
also rejected.

## Provisioning a Remote Compute Cluster

Contrail Networking enables you to provision remote compute using an
`instances.yaml` file. [Installing a Contrail Cluster using Contrail
Command and
instances.yml](../task/configuration/deploy-cluster-contrail-command-instances-yml.html)
shows a bare minimum configuration. The YAML file described in this
section builds upon that minimum configuration and uses
[Figure 1](remote-compute-50.html#subcluster) as an example data center
network topology.

![Figure 1: Example Multi-Cluster
Topology](documentation/images/g200469.png)

In this topology, there is one main data center (`pop0`) and two remote
data centers (`pop1` and `pop2`.) `pop0` contains two subclusters: one
for `pop1,` and the other for `pop2`. Each subcluster has two control
nodes. The control nodes within a subcluster, for example 10.0.0.9 and
10.0.0.10, communicate with each other through iBGP.

Communication between the control nodes within a subcluster and the
remote data center is through the SDN Gateway; there is no direct
connection. For example, the remote compute in pop1 (IP address
10.20.0.5) communicates with the control nodes (IP addresses 10.0.0.9
and 10.0.0.10) in subcluster 1 through the SDN Gateway.

To configure remote compute in the YAML file:

1.  <span id="jd0e183">First, create the remote locations or
    subclusters. In this example, we create data centers 2 and 3 (with
    the names `pop1` and `pop2`, respectively), and define unique ASN
    numbers for each. Subcluster names must also be unique.</span>
    <div id="jd0e192" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        remote_locations:
          pop1:
            BGP_ASN: 12345
            SUBCLUSTER: pop1
          pop2:
            BGP_ASN: 12346
            SUBCLUSTER: pop2

    </div>

    </div>
2.  <span id="jd0e195">Create the control nodes for pop1 and pop2 and
    assign an IP address and role. These IP addresses are the local IP
    address. In this example, there are two control nodes for each
    subcluster.</span>
    <div id="jd0e198" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        control_1_only_pop1:           # Mandatory. Instance name
            provider: bms              # Mandatory. Instance runs on BMS
            ip: 10.0.0.9
            roles:
              control:
                location: pop1
          control_2_only_pop1:         # Mandatory. Instance name
            provider: bms              # Mandatory. Instance runs on BMS
            ip: 10.0.0.10
            roles:
              control:
                location: pop1 
          control_1_only_pop2:         # Mandatory. Instance name
            provider: bms              # Mandatory. Instance runs on BMS
            ip: 10.0.0.11
            roles:                     # Optional. 
              control:
                location: pop2
          control_2_only_pop2:         # Mandatory. Instance name
            provider: bms              # Mandatory. Instance runs on BMS
            ip: 10.0.0.12
            roles:                     # Optional. 
              control:
                location: pop2

    </div>

    </div>
3.  <span id="jd0e201">Now, create the remote compute nodes for `pop1`
    and `pop2` and assign an IP address and role. In this example, there
    are two remote compute nodes for each data center. The 10.60.0.x
    addresses are the management IP addresses for the control
    service.</span>
    <div id="jd0e210" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        compute_1_pop1:                  # Mandatory. Instance name
            provider: bms                # Mandatory. Instance runs on BMS
            ip: 10.20.0.5
            roles:
              openstack_compute:         # Optional.
              vrouter:
                CONTROL_NODES: 10.60.0.9,10.60.0.10
                VROUTER_GATEWAY: 10.70.0.1
                location: pop1
          compute_2_pop1:                # Mandatory. Instance name
            provider: bms                # Mandatory. Instance runs on BMS
            ip: 10.20.0.6
            roles:
              openstack_compute:         # Optional. 
              vrouter:
                CONTROL_NODES: 10.60.0.9,10.60.0.10
                VROUTER_GATEWAY: 10.70.0.1
                location: pop1
          compute_1_pop2:                # Mandatory. Instance name
            provider: bms                # Mandatory. Instance runs on BMS
            ip: 10.30.0.5
            roles:
              openstack_compute:         # Optional.
              vrouter:
                CONTROL_NODES: 10.60.0.11,10.60.0.12
                VROUTER_GATEWAY: 10.80.0.1
                location: pop2
          compute_2_pop2:                # Mandatory. Instance name
            provider: bms                # Mandatory. Instance runs on BMS
            ip: 10.30.0.6
            roles:
              openstack_compute:         # Optional. 
              vrouter:
                CONTROL_NODES: 10.60.0.11,10.60.0.12
                VROUTER_GATEWAY: 10.80.0.1
                location: pop2

    </div>

    </div>

The entire YAML file is contained below.

<div id="jd0e215" class="sample" dir="ltr">

**Example instance.yaml with subcluster configuration**

<div class="output" dir="ltr">

    provider_config:
      bms:
        ssh_pwd: <password>
        ssh_user: <root_user>
        ntpserver: 10.84.5.100
        domainsuffix: local
    instances:
      openstack_node:                  # Mandatory. Instance name
        provider: bms                  # Mandatory. Instance runs on BMS
        ip: 10.0.0.4
        roles:                         # Optional. 
          openstack:
      all_contrail_roles_default_pop:  # Mandatory. Instance name
        provider: bms                  # Mandatory. Instance runs on BMS
        ip: 10.0.0.5
        roles:                         # Optional. 
          config_database:             # Optional.
          config:                      # Optional.
          control:                     # Optional.
          analytics_database:          # Optional.
          analytics:                   # Optional.
          webui:                       # Optional.
      compute_3_default_pop:           # Mandatory. Instance name
        provider: bms                  # Mandatory. Instance runs on BMS
        ip: 10.0.0.6
        roles:
          openstack_compute:
          vrouter:
            VROUTER_GATEWAY: 10.60.0.1
      compute_1_default_pop:           # Mandatory. Instance name
        provider: bms                  # Mandatory. Instance runs on BMS
        ip: 10.0.0.7
        roles:
          openstack_compute:
          vrouter:
            VROUTER_GATEWAY: 10.60.0.1
      compute_2_default_pop:          # Mandatory. Instance name
        provider: bms                 # Mandatory. Instance runs on BMS
        ip: 10.0.0.8
        roles:
          openstack_compute:
          vrouter:
            VROUTER_GATEWAY: 10.60.0.1
      control_1_only_pop1:            # Mandatory. Instance name
        provider: bms                 # Mandatory. Instance runs on BMS
        ip: 10.0.0.9
        roles:
          control:
            location: pop1
      control_2_only_pop1:            # Mandatory. Instance name
        provider: bms                 # Mandatory. Instance runs on BMS
        ip: 10.0.0.10
        roles:
          control:
            location: pop1 
      control_1_only_pop2:            # Mandatory. Instance name
        provider: bms                 # Mandatory. Instance runs on BMS
        ip: 10.0.0.11
        roles:                        # Optional.
          control:
            location: pop2
      control_2_only_pop2:            # Mandatory. Instance name
        provider: bms                 # Mandatory. Instance runs on BMS
        ip: 10.0.0.12
        roles:                        # Optional.
          control:
            location: pop2
      compute_1_pop1:                 # Mandatory. Instance name
        provider: bms                 # Mandatory. Instance runs on BMS
        ip: 10.20.0.5
        roles:
          openstack_compute:          # Optional.
          vrouter:
            CONTROL_NODES: 10.60.0.9,10.60.0.10
            VROUTER_GATEWAY: 10.70.0.1
            location: pop1
      compute_2_pop1:                 # Mandatory. Instance name
        provider: bms                 # Mandatory. Instance runs on BMS
        ip: 10.20.0.6
        roles:
          openstack_compute:          # Optional.
          vrouter:
            CONTROL_NODES: 10.60.0.9,10.60.0.10
            VROUTER_GATEWAY: 10.70.0.1
            location: pop1
      compute_1_pop2:                 # Mandatory. Instance name
        provider: bms                 # Mandatory. Instance runs on BMS
        ip: 10.30.0.5
        roles:
          openstack_compute:          # Optional. 
          vrouter:
            CONTROL_NODES: 10.60.0.11,10.60.0.12
            VROUTER_GATEWAY: 10.80.0.1
            location: pop2
      compute_2_pop2:                 # Mandatory. Instance name
        provider: bms                 # Mandatory. Instance runs on BMS
        ip: 10.30.0.6
        roles:
          openstack_compute:          # Optional.
          vrouter:
            CONTROL_NODES: 10.60.0.11,10.60.0.12
            VROUTER_GATEWAY: 10.80.0.1
            location: pop2
    global_configuration:
      CONTAINER_REGISTRY: 10.xx.x.81:5000
      REGISTRY_PRIVATE_INSECURE: True

    contrail_configuration:           # Contrail service configuration section
      CONTRAIL_VERSION: <contrail_version>
      CONTROLLER_NODES: 10.60.0.5
      CLOUD_ORCHESTRATOR: openstack
      KEYSTONE_AUTH_HOST: 10.60.0.100
      KEYSTONE_AUTH_URL_VERSION: /v3
      RABBITMQ_NODE_PORT: 5673
      PHYSICAL_INTERFACE: eth1
      CONTROL_DATA_NET_LIST: 10.60.0.0/24,10.70.0.0/24,10.80.0.0/24

    kolla_config:
      kolla_globals:
        network_interface: "eth1"
        enable_haproxy: "yes"
        contrail_api_interface_address: 10.60.0.5
        kolla_internal_vip_address: 10.60.0.100
        kolla_external_vip_address: 10.0.0.100
        kolla_external_vip_interface: "eth0"
      kolla_passwords:
        keystone_admin_password: <password>

    remote_locations:
      pop1:
        BGP_ASN: 12345
        SUBCLUSTER: pop1
      pop2:
        BGP_ASN: 12346
        SUBCLUSTER: pop2

</div>

</div>

**Note**

Replace `<contrail_version>` with the correct <span class="cli"
v-pre="">contrail\_container\_tag</span> value for your Contrail
Networking release. The respective <span class="cli"
v-pre="">contrail\_container\_tag</span> values are listed in [README
Access to Contrail
Registry](https://www.juniper.net/documentation/en_US/contrail19/information-products/topic-collections/release-notes/readme-contrail-19.pdf)  .

<div class="table">

<div class="caption">

Release History Table

</div>

<div class="table-row table-head">

<div class="table-cell">

Release

</div>

<div class="table-cell">

Description

</div>

</div>

<div class="table-row">

<div class="table-cell">

[2005](#jd0e85)

</div>

<div class="table-cell">

Contrail Networking Release 2005 supports inter subcluster route
filtering (Beta).

</div>

</div>

</div>

 
