# Working with Neutron

 

<div id="intro">

<div class="mini-toc-intro">

OpenStack’s networking solution, Neutron, has representative elements
for Contrail elements for Network (VirtualNetwork), Port
(VirtualMachineInterface), Subnet (IpamSubnets), and Security-Group. The
Neutron plugin translates the elements from one representation to
another.

</div>

</div>

## Data Structure

Although the actual data between Neutron and Contrail is similar, the
listings of the elements differs significantly. In the Contrail API, the
networking elements list is a summary, containing only the UUID, FQ
name, and an href, however, in Neutron, all details of each resource are
included in the list.

The Neutron plugin has an inefficient list retrieval operation,
especially at scale, because it:

-   reads a list of resources (for example. `GET /virtual-networks`),
    then

-   iterates and reads in the details of the resource
    (`GET /virtual-network/<uuid>` ).

As a result, the API server spends most of the time in this type of GET
operation just waiting for results from the Cassandra database.

The following features in Contrail improve performance with Neutron:

-   An optional detail query parameter is added in the GET of
    collections so that the API server returns details of all the
    resources in the list, instead of just a summary. This is
    accompanied by changes in the Contrail API library so that a caller
    gets returned a list of the objects.

-   The existing Contrail list API takes in an optional `parent_id`
    query parameter to return information about the resource anchored by
    the parent.

-   The Contrail API server reads objects from Cassandra in a multiget
    format into `obj_uuid_cf`, where object contents are stored, instead
    of reading in an xget/get format. This reduces the number of
    round-trips to and from the Cassandra database.

## Network Sharing in Neutron

Using Neutron, a deployer can make a network accessible to other tenants
or projects by using one of two attributes on a network:

-   Set the `shared` attribute to allow sharing.

-   Set the `router:external` attribute, when the plugin supports an
    `external_net` extension.

*Using the Shared Attribute*

When a network has the `shared` attribute set, users in other tenants or
projects, including non-admin users, can access that network, using:

`neutron net-list --shared `

Users can also launch a virtual machine directly on that network, using:

` nova boot <other-parameters> –nic net-id=<shared-net-id>`

*Using the Router:External Attribute*

When a network has the `router:external` attribute set, users in other
tenants or projects, including non-admin users, can use that network for
allocating floating IPs, using:

`neutron floatingip-create <router-external-net-id>`

then associating the IP address pool with their instances.

**Note**

The VN hosting the FIP pool should be marked shared and external.

## Commands for Neutron Network Sharing

The following table summarizes the most common Neutron commands used
with Contrail.

| Action                                                      | Command                                          |
|:------------------------------------------------------------|:-------------------------------------------------|
| List all shared networks.                                   | `neutron net-list --shared`                      |
| Create a network that has the shared attribute.             | `neutron net-create <net-name> –shared`          |
| Set the shared attribute on an existing network.            | `neutron net-update <net-name> -shared`          |
| List all `router:external` networks.                        | `neutron net-list --router:external`             |
| Create a network that has the `router:external`attribute.   | `neutron net-create <net-name> -router:external` |
| Set the `router:external` attribute on an existing network. | `neutron net-update <net-name> -router:external` |

## Support for Neutron APIs

The OpenStack Neutron project provides virtual networking services among
devices that are managed by the OpenStack compute service. Software
developers create applications by using the OpenStack Networking API
v2.0 (Neutron).

Contrail provides the following features to increase support for
OpenStack Neutron:

-   Create a port independently of a virtual machine.

-   Support for more than one subnet on a virtual network.

-   Support for allocation pools on a subnet.

-   Per tenant quotas.

-   Enabling DHCP on a subnet.

-   External router can be used for floating IPs.

For more information about using OpenStack Networking API v2.0
(Neutron), refer to:
[http://docs.openstack.org/api/openstack-network/2.0/content/​](http://docs.openstack.org/api/openstack-network/2.0/content/​)
and the OpenStack Neutron Wiki at:
<http://wiki.openstack.org/wiki/Neutron>.

## Contrail Neutron Plugin

The Contrail Neutron plugin provides an implementation for the following
core resources:

-   Network

-   Subnet

-   Port

It also implements the following standard and upstreamed Neutron
extensions:

-   Security group

-   Router IP and floating IP

-   Per-tenant quota

-   Allowed address pair

The following Contrail-specific extensions are implemented:

-   Network IPAM

-   Network policy

-   VPC table and route table

-   Floating IP pools

The plugin does not implement native bulk, pagination, or sort
operations and relies on emulation provided by the Neutron common code.

## DHCP Options

In Neutron commands, DHCP options can be configured using
extra-dhcp-options in port-create.

<div id="jd0e302" class="example" dir="ltr">

### Example

    neutron port-create net1 --extra-dhcp-opt opt_name=<dhcp_option_name>,opt_value=<value>

</div>

The opt\_name and opt\_value pairs that can be used are maintained in
GitHub:
<https://github.com/Juniper/contrail-controller/wiki/Extra-DHCP-Options>
.

## Incompatibilities

In the Contrail architecture, the following are known incompatibilities
with the Neutron API.

-   Filtering based on any arbitrary key in the resource is not
    supported. The only supported filtering is by `id, name,` and
    `tenant_id`.

-   To use a floating IP, it is not necessary to connect the public
    subnet and the private subnet to a Neutron router. Marking a public
    network with `router:external` is sufficient for a floating IP to be
    created and associated, and packet forwarding to it will work.

-   The default values for quotas are sourced from
    `/etc/contrail/contrail-api.conf `and not
    from` /etc/neutron/neutron.conf.`

 
