# Introduction


Contrail RBAC provides access control at API (operation) and resource level. Previously with multi-tenancy, only resource level access control modeled after Unix style permissions for user, group (role) and others (world) was available.

RBAC in OpenStack Helm currently works in conjunction with Keystone relying on user credentials obtained from Keystone from the token present in the API request. Credentials include user, role, tenant and domain information.

API level access is controlled by the list of rules. Attachment point for the rules is global-system-config, domain and project. Resource level access is controlled by permissions embedded in the object. 

## OpenStack and Contrail Helm RBAC support

There are no major changes in Contrail RBAC implementation so existing Contrail RBAC feature will fully work in Helm deployment as well. Please check reference link for more detail about RBAC feature

### Reference
[Contrail RBAC](https://github.com/Juniper/contrail-controller/wiki/RBAC)
.