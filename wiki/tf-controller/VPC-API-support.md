A subset of AWS VPC resources are supported in either directly via Contrail-API or via Neutron-API through [route-table extension.](https://github.com/Juniper/contrail-neutron-plugin/blob/master/neutron_plugin_contrail/extensions/vpcroutetable.py) Design details are present in this [blueprint.](https://wiki.openstack.org/wiki/Blueprint-aws-vpc-support)

Some of these resources can be used on their own even without VPC-API. For e.g. the external_gateway (in NAT mode) functionality on a Neutron router is implemented by

* creating a service-instance that does NAT in a netns
* creating a route-table in the project if it doesn't exist
* creating a 0.0.0.0/0 route with the service-instance as nexthop and add it to route-table
* associate this route-table to all virtual-networks connected to the logical-router

Examples of using Neutron-API to manipulate these new resources can be traced from [here.](https://github.com/Juniper/contrail-test/blob/5643fea6c0d1f5fcae864930a118081520977e0b/scripts/vpc/test_vpc.py#L528)
 