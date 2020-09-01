## Introduction
OpenContrail Analytics exposes a rich variety of comprehensive and in-depth statistics related to the operational state of virtual machines or instances, virtual networks, floating IPs and other objects. Cloud operators using OpenContrail as the networking solution in an Openstack deployment benefit from having these statistics exposed to them. The OpenContrail Analytics API server provides a very fast and scalable REST API implementation to query these statistics. However for cloud operators who prefer to query the Ceilometer APIs to extract these statistics, OpenContrail provides a Ceilometer driver / plugin to expose these statistics. 

One of the important statistics for a cloud operator from an accounting, billing, and planning perspective is the traffic statistics for a particular floating IP or elastic IP assigned to a customer's virtual machine or instance. Further, traffic statistics for total traffic flowing from a customer's network to the public network are also needed.

## Proposal
Ceilometer currently does not have meters for traffic statistics for floating IPs and hence the proposal is to add the following meters to ceilometer -

    ip.floating.receive.bytes
    ip.floating.receive.packets
    ip.floating.transmit.bytes
    ip.floating.transmit.packets

Similarly, ceilometer currently does not meters for total traffic statistics from one virtual network to another (this is a generalization of the requirement for finding total traffic flowing from a customer's network to the public network). The proposal is to add the following meters to ceilometer -

    network.destination.network.receive.bytes
    network.destination.network.receive.packets
    network.destination.network.transmit.bytes
    network.destination.network.transmit.packets 

## Existing OpenContrail Ceilometer Driver Implementation
The OpenContrail ceilometer driver populates the `switch.port.receive.bytes`, `switch.port.receive.packets`, `switch.port.transmit.bytes`,  and `switch.port.transmit.packets` meters in ceilometer. 

The driver can be configured to populate these meters with the following options:

1. The floating IP statistics or the interface statistics

2. For a particular virtual machine / instance or all virtual machines / instances

3. For a particular virtual network or all virtual networks. 

The driver is configured using the `resource` field in the ceilometer pipeline configuration file - `pipeline.yaml`. For example, the below configuration in `pipeline.yaml` will configure the driver to populate the meters with the floating IP statistics for all virtual machines with destination virtual network `default-domain:demo:vn3-public`

    sources:
        - name: oc_source
          interval: 600
          meters:
            - "switch.port.receive.packets"
            - "switch.port.transmit.packets"
            - "switch.port.receive.bytes"
            - "switch.port.transmit.bytes"
          resources:
              - opencontrail://a6s23.contrail.juniper.net:8081/analytics/uves/virtual-machine/?resource=fip_stats_list&virtual_network=default-domain:demo:vn3-public
          sinks:
            - oc_network
    sinks:
        - name: oc_network
          publishers:
            - rpc://
          transformers:

## Enhancements to OpenContrail Ceilometer Driver Implementation
The driver will be enhanced to support populating the above proposed traffic statistics meters for floating IPs and virtual networks. For these meters, only the address of the analytics API server is needed from the `resources` URL above and rest of the URL parameters like `resource` will be ignored. For the floating IPs meters, the driver will query neutron to obtain the list of floating IPs and extract the virtual machines/instances associated with the floating IPs. It will then query the OpenContrail analytics REST API server to extract the floating IP statistics associated with those virtual machines and floating IPs and populate the meters. Similarly for the virtual network meters, the driver will query neutron/nova to obtain the list of networks and then query the OpenContrail analytics REST API server to extract the inter and intra virtual network statistics and populate the meters. 

For example, following is the `ceilometer meter-list` output for the floating IP meters:

    +-------------------------------+------------+-----------+-----------------------------------------------------------------------+----------------------------------+----------------------------------+
    | Name                          | Type       | Unit      | Resource ID                                                            | User ID                          | Project ID                       |
    +-------------------------------+------------+-----------+-----------------------------------------------------------------------+----------------------------------+----------------------------------+
    | ip.floating.receive.bytes     | cumulative | B         | 451c93eb-e728-4ba1-8665-6e7c7a8b49e2                                  | None                             | None                             |
    | ip.floating.receive.bytes     | cumulative | B         | 9cf76844-8f09-4518-a09e-e2b8832bf894                                  | None                             | None                             |
    | ip.floating.receive.packets   | cumulative | packet    | 451c93eb-e728-4ba1-8665-6e7c7a8b49e2                                  | None                             | None                             |
    | ip.floating.receive.packets   | cumulative | packet    | 9cf76844-8f09-4518-a09e-e2b8832bf894                                  | None                             | None                             |
    | ip.floating.transmit.bytes    | cumulative | B         | 451c93eb-e728-4ba1-8665-6e7c7a8b49e2                                  | None                             | None                             |
    | ip.floating.transmit.bytes    | cumulative | B         | 9cf76844-8f09-4518-a09e-e2b8832bf894                                  | None                             | None                             |
    | ip.floating.transmit.packets  | cumulative | packet    | 451c93eb-e728-4ba1-8665-6e7c7a8b49e2                                  | None                             | None                             |
    | ip.floating.transmit.packets  | cumulative | packet    | 9cf76844-8f09-4518-a09e-e2b8832bf894                                  | None                             | None                             |

The Resource ID in the meters above refers to the floating IP. Following is the `ceilometer resource-show -r 451c93eb-e728-4ba1-8665-6e7c7a8b49e2` output:

    +-------------+-------------------------------------------------------------------------+
    | Property    | Value                                                                   |
    +-------------+-------------------------------------------------------------------------+
    | metadata    | {u'router_id': u'None', u'status': u'ACTIVE', u'tenant_id':             |
    |             | u'ceed483222f9453ab1d7bcdd353971bc', u'floating_network_id':            |
    |             | u'6d0cca50-4be4-4b49-856a-6848133eb970', u'fixed_ip_address':           |
    |             | u'2.2.2.4', u'floating_ip_address': u'3.3.3.4', u'port_id': u'c6ce2abf- |
    |             | ad98-4e56-ae65-ab7c62a67355', u'id':                                    |
    |             | u'451c93eb-e728-4ba1-8665-6e7c7a8b49e2', u'device_id':                  |
    |             | u'00953f62-df11-4b05-97ca-30c3f6735ffd'}                                |
    | project_id  | None                                                                    |
    | resource_id | 451c93eb-e728-4ba1-8665-6e7c7a8b49e2                                    |
    | source      | openstack                                                               |
    | user_id     | None                                                                    |
    +-------------+-------------------------------------------------------------------------+

The `ceilometer statistics` and `ceilometer sample-list` output for the meter `ip.floating.receive.packets` are shown below:

    +--------+----------------------------+----------------------------+-------+-----+-------+--------+----------------+------------+----------------------------+----------------------------+
    | Period | Period Start               | Period End                 | Count | Min | Max   | Sum    | Avg            | Duration   | Duration Start             | Duration End               |
    +--------+----------------------------+----------------------------+-------+-----+-------+--------+----------------+------------+----------------------------+----------------------------+
    | 0      | 2015-02-13T19:50:40.795000 | 2015-02-13T19:50:40.795000 | 2892  | 0.0 | 325.0 | 1066.0 | 0.368603042877 | 439069.674 | 2015-02-13T19:50:40.795000 | 2015-02-18T21:48:30.469000 |
    +--------+----------------------------+----------------------------+-------+-----+-------+--------+----------------+------------+----------------------------+----------------------------+ 

    +--------------------------------------+-----------------------------+------------+--------+--------+----------------------------+
    | Resource ID                          | Name                        | Type       | Volume | Unit   | Timestamp                  |
    +--------------------------------------+-----------------------------+------------+--------+--------+----------------------------+
    | 9cf76844-8f09-4518-a09e-e2b8832bf894 | ip.floating.receive.packets | cumulative | 208.0  | packet | 2015-02-18T21:48:30.469000 |
    | 9cf76844-8f09-4518-a09e-e2b8832bf894 | ip.floating.receive.packets | cumulative | 208.0  | packet | 2015-02-18T21:48:30.469000 |
    | 451c93eb-e728-4ba1-8665-6e7c7a8b49e2 | ip.floating.receive.packets | cumulative | 325.0  | packet | 2015-02-18T21:48:28.354000 |
    | 451c93eb-e728-4ba1-8665-6e7c7a8b49e2 | ip.floating.receive.packets | cumulative | 325.0  | packet | 2015-02-18T21:48:28.354000 |
    | 9cf76844-8f09-4518-a09e-e2b8832bf894 | ip.floating.receive.packets | cumulative | 0.0    | packet | 2015-02-18T21:38:30.350000 |