Configuring Role-Based Access Control for Analytics
===================================================

The analytics API uses role-based access control (RBAC) to provide the
ability to access UVE and query information based on the permissions of
the user for the UVE or queried object.

Tungsten Fabric extends authenticated access so that tenants can
view network monitoring information about the networks for which they
have read permissions.

The analytics API can map query and UVE objects to configuration objects
on which RBAC rules are applied, so that read permissions can be
verified using the VNC API.

RBAC is applied to analytics in the following ways:

-  For statistics queries, annotations are added to the Sandesh file so
   that indices and tags on statistics queries can be associated with
   objects and UVEs. These are used by the contrail-analytics-api to
   determine the object level read permissions.

-  For flow and log queries, the object read permissions are evaluated
   for each AND term in the where query.

-  For UVEs list queries (e.g. analytics/uve/virtual-networks/), the
   contrail-analytics-api gets a list of UVEs that have read permissions
   for a given token. For a UVE query for a specific resource (e.g.
   analytics/uves/virtual-network/vn1), contrail-analytics-api checks
   the object level read permissions using VNC API.

Tenants cannot view system logs and flow logs, those logs are displayed
for cloud-admin roles only.

A non-admin user can see only non-global UVEs, including:

-  virtual_network

-  virtual_machine

-  virtual_machine_interface

-  service_instance

-  service_chain

-  tag

-  firewall_policy

-  firewall_rule

-  address_group

-  service_group

-  aaplication_policy_set

In ``/etc/contrail/contrail-analytics-api.conf``, in the section
``DEFAULTS``, the parameter ``aaa_mode`` now supports ``rbac`` as one of
the values.

 
