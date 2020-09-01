# Introduction

Contrail RBAC provides access control at API (operation) and resource level. Previously with multi-tenancy, only resource level access control modeled after unix style permissions for user, group (role) and others (world) was available .

RBAC currently works in conjunction with Keystone relying on user credentials obtained from keystone from token present in the API request. Credentials include user, role, tenant and domain information.

API level access is controlled by list of rules. Attachment point for the rules is global-system-config, domain and project. Resource level access is controlled by permissions embedded in the object.

# API Level access control

If RBAC feature is turned on, API server requires a valid token to be present in the **X-Auth-Token** of incoming request. If token is missing or is invalid, HTTP error 401 will be returned. API server trades token for user credentials (role, domain, project etc) from keystone.

api-access-list object holds rules of the form:

    <object, field> => list of <role:CRUD>

object refers to an API resource such as network or subnet. Field refers to any property or reference within the resource. Field is optional in which case the CRUD operation refers to entire resource. Each rule also specifies list of roles and their corresponding permissions as a subset of CRUD operations.

For example, ACL object for a project might look like this:

    <virtual-network, network-policy> => admin:CRUD
    <virtual-network, network-ipam> => admin:CRUD
    <virtual-network, *>    => admin:CRUD, Development:CRUD

Thus admin and users with role <em>Development</em> can perform CRUD operations on network in a project, only admin can perform CRUD operations for policy and IPAM inside a network.

Role is Keystone role name. Field can be resource property or Reference. Field can be multi level, for example network.ipam.host-routes (in first release only one level is supported).

Rule set for validation is union of rules from api-access-list object attached to :
 - user Project
 - user domain 
 - default-domain 

It is possible for project or domain ACL object to be empty. Access is only granted if a rule in the combined Rule set allows access. There is no explicit deny rule.

ACL object can be shared within a domain. Thus multiple projects can point to same ACL object (such as default).

# Object level access control

perms2 property of an object allows fine grained access control per resource. It has the following fields:
 - Owner (tenant uuid)
 - share list (list of (tenant/domain UUID, Permissions) tuple) 
 - globally shared flag (plus Permissions)

Owner field is populated at the time of creation as per the logic in section 'Object level RBAC ownership' below. Share list gets built as object is selected for sharing with other users. Sharing can be enabled at tenant or domain level.

Permission field has following meaning:
  - R (Read object)
  - W (Create/Update object)
  - X (Link or refer to object)

Access is allowed if:
   - user is owner and permissions allow (rwx) or
   - user tenant or domain in shared list and permissions allow or
   - world access is allowed

# Configuration

## aaa-mode
RBAC is controlled by a new knob named **aaa-mode**. It can be set to following values:

 - *no-auth* (no authentication is performed and full access is granted to all)
 - *cloud-admin* (authentication is performed and only cloud-admin role has access - default cloud-admin role is "admin") 
 - *rbac* RBAC (authentication is performed and access granted based on role and configured rules)

With release of RBAC, multi-tenancy flag is being deprecated. Multi-tenancy name was a misnomer because Multi tenancy is an inherent feature of Contrail while the knob enforced admin only access.  

Multi-tenancy knob must not be set in configuration files for RBAC to take effect. If multi-tenancy flag is present in configuration file, aaa-mode setting will be ignored. 

## cloud_admin_role
User with cloud admin role has full access to everything. Name of this role is configured by **cloud_admin_role** knob in API server. By default this is set to "admin". This role must be configured in keystone. Set cloud_admin_role in /etc/contrail/contrail-api.conf on controller node and restart the API server to take affect.

A user with cloud admin role in one tenant must include that role in other tenants if user has any role in them. User with cloud admin role doesn't need to have a role in all tenants but if has a role in a tenant, it must include cloud admin role.

Following configuration files contain cloud admin credentials and should be modified if cloud-admin role is changed:
* /etc/contrail/contrail-keystone-auth.conf
* /etc/neutron/plugins/opencontrail/ContrailPlugin.ini
* /etc/contrail/contrail-webui-userauth.js

After changing the files above, restart API server, neutron server and WEBUI
* service supervisor-config restart
* service neutron-server restart
* service supervisor-webui restart

Note the `user_token` filter must not be set in the neutron `api-paste.ini` file.

## global_read_only_role
Role configured as global_read_only_role allows read-only access to all contrail resources. This role must be configured in keystone. By default this is not set to any value. global_read_only_role user can view the global configuration of contrail default setting from WebUI. Admin has to set global_read_only_role in contrail api (/etc/contrail/contrail-api.conf) and restart contrail-api service (service contrail-api restart). 

    global_read_only_role = <new-admin-read-role>

## /etc/neutron/api-paste.ini
Contrail RBAC is based on user token received in _X-Auth-Token_ header in API requests. To force neutron to pass actual user token in requests to Contrail API server, following change in /etc/neutron/api-paste.ini is needed.

    keystone = user_token request_id catch_errors ....
    ...
    ...
    [filter:user_token]
    paste.filter_factory = neutron_plugin_contrail.plugins.opencontrail.neutron_middleware:token_factory

Note that if RBAC is enabled while provisions via fab (See provisioning section below), /etc/neutron/api-paste.ini will be updated automatically.

# Provisioning through fab

To enable RBAC while provisioning through fab, set the aaa_mode in testbed.py as follows:

    aaa_mode='rbac'

# Utilities
## rbacutil.py
to manage api-access-list rules. It allows adding, removing and viewing of rules. For example:

Read RBAC rule-set using UUID or FQN

    python /opt/contrail/utils/rbacutil.py --uuid 'b27c3820-1d5f-4bfd-ba8b-246fefef56b0' --op read
    python /opt/contrail/utils/rbacutil.py --name 'default-domain:default-api-access-list' --op read
    python /opt/contrail/utils/rbacutil.py --name 'default-global-system-config:default-api-access-list' --op read

Create RBAC rule-set using FQN domain/project

    python /opt/contrail/utils/rbacutil.py --name 'default-domain:api-access-list' --op create

Delete RBAC group using FQN or UUID

    python /opt/contrail/utils/rbacutil.py --name 'default-domain:api-access-list' --op delete
    python /opt/contrail/utils/rbacutil.py --uuid 71ef050f-3487-47e1-b628-8b0949530bee --op delete

Add rule to existing RBAC group

    python /opt/contrail/utils/rbacutil.py --uuid <uuid> --rule "* Member:R" --op add-rule
    python /opt/contrail/utils/rbacutil.py --uuid <uuid> --rule "useragent-kv *:CRUD" --op add-rule

Delete rule from RBAC group - specify rule number or exact rule

    python /opt/contrail/utils/rbacutil.py --uuid <uuid> --rule 2 --op del-rule
    python /opt/contrail/utils/rbacutil.py --uuid <uuid> --rule "useragent-kv *:CRUD" --op del-rule

The script requires administrative credentials. Note that a few rules are pre-configured at global level as software defaults. These are needed for system operations. If removed, these rules will be added when API server is restarted.

    root@b4s3:/opt/contrail/utils# python /opt/contrail/utils/rbacutil.py --name "default-global-system-config:default-api-access-list" --op read
    AAA mode is rbac

    Oper       =  read
    Name       = ['default-global-system-config', 'default-api-access-list']
    UUID       = None
    API Server =  127.0.0.1:8082
    
    Rules (5):
    ----------
     1 fqname-to-id                       *:CRUD,
     2 useragent-kv                       *:CRUD,
     3 documentation                      *:R,
     4 id-to-fqname                       *:CRUD,
     5 /                                  *:R,

## chmod2.py
This allows updating object permissions:
- ownership (specify new owner tenant UUID)
- enable/disable sharing with other tenants (specify <tenant, permissions>)
- enable/disable sharing with world (specify permissions)

# Upgrading from previous releases

multi_tenancy flag is deprecated in 3.1. It should be removed from config and replaced with aaa_mode parameter.

# Contrail UI
For Contrail UI to work with RBAC, set aaa_mode to no_auth in /etc/contrail/contrail-analytics-api.conf and restart analytics-api service (service contrail-analytics-api restart)

    aaa_mode = no-auth

## Object level RBAC ownership
Once a request gets past API level RBAC access, object level RBAC kicks in. RBAC defines a owner field in each object, to limit the scope of object access. The access scope is limited to in that owner by any role that got passed RBAC API access check.

We recommend owner to be explicitly set by users, while the objects are being created.
If however the ownership is not defined, here is the order in which this is populated.
1. We derive the ownership from the parent’t owner.
2. For domain children, we derive the ownership from the tenant context in which this object is created.
3. If there is no parent for an object we limit the scope of the object to the project context which it was created.
4. Global-system-config children would have cloud-admin as owner, unless project scope is explicitly set. Such objects, where project scope is not set, have to be explicitly shared with the tenants that need access.

To extend the scope of the object access, that object can be shared across tenants or domains with various permission levels.

Objects from outside the scope of the owner can't be accessed, unless they are shared. However could-admin has no restrictions and can access any object.

## Brown field migration
Before enabling RBAC in brown field. Object's owner have to be correct. The ownership of the objects may be validated and or corrected as per logic defined in section 'Object level RBAC ownership' using the script chownproj.py. Instructions of execution is available in that script.

It is always recommended to take a backup of the database using the script db_json_exim.py before modifying the data. Instructions on how to run db_json_exim.py is also available in that script.

## Rule configuration changes from 3.2.6 onwards.
From 3.2.6 all the CRUD requests would be subjected to respective singular object-type rules.