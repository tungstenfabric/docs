# Role- and Resource-Based Access Control for the Contrail Analytics API

 

In previous releases of Contrail, any user can access the Contrail
analytics API by using queries to get historical information and by
using UVEs to get state information.

With Contrail, it is possible to restrict access such that only the
`cloud-admin` user can access the Contrail analytics API.

Implementation details are as follows:

-   An external user makes a REST API call to `contrail-analytics-api`,
    passing a token representing the user with the HTTP header
    X-Auth-Token.

-   Based on the user role, `contrail-analytics-api` will only allow
    access for the `cloud-admin` user and reject the request
    (`HTTPUnauthorized`) for other users.

To set the `cloud_admin` user, use the following fields in
`/etc/contrail/contrail-analytics-api.conf`:

-   `aaa_mode`—Takes one of these values:

    -   `no-auth`

    -   `cloud-admin`

-   `cloud_admin_role`—The user with this role has full access to
    everything. By default, this is set to "admin". This role must be
    configured in Keystone.

 
