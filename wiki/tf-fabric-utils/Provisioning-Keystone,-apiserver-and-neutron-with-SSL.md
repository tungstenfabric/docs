# Introduction
Provisioning keystone, api-server and neutron with SSL through contrail-fabric-utils. This is achieved by
configuring keystone with native SSL and api-server/neutron through SSL termination using Haproxy.

# Knobs in testbed.py
1. env.keystone section in testbed.py is populated with auth_protocol as 'https' to enable keystone SSL
        
        env.keystone = {
            'auth_protocol'   : 'https'
        }
2. env.cfgm section ins testbed.py is populated with auth_protocol as 'https' to enable api-server/neutron SSL

        env.cfgm = {
            'auth_protocol'   : 'https'
        }

# Provisioning

With the above knobs are set in testbed.py.

fab setup_all will, 

1. Create certificates for keystone in openstack node
2. Copy over certificates to other openstack nodes in case of HA setup.
3. Configures and brings up keystone service with SSL
4. Create certificates for api-server/neutron in config|cfgm node
5. Copy over certificates to other config|cfgm nodes in case of HA setup.
6. Configures SSL termination for api-server/neutron using Haproxy
7. Brings up other openstack and contrail services to make them interact with keystone/api-server/neutron over https protocol.

# Known Issues:
1. Nova boot fails due to permission issue
    https://bugs.launchpad.net/juniperopenstack/+bug/1613178

   Workaround:

        fab -R cfgm -- "usermod -a -G contrail neutron"
        fab -R cfgm -- "service neutron-server restart"

2. Heat fails with SSL enabled contrail cluster
    https://bugs.launchpad.net/juniperopenstack/+bug/1612826

   Workaround:

        fab -R openstack -- "openstack-config --set /etc/heat/heat.conf keystone_authtoken insecure True"
        fab -R openstack -- "openstack-config --set /etc/heat/heat.conf clients_keystone insecure True"
        fab -R openstack -- "openstack-config --set /etc/heat/heat.conf clients_neutron insecure True"
        fab -R openstack -- "openstack-config --set /etc/heat/heat.conf clients_contrail use_ssl True"
        
        followed by,

        Execute following only if config and openstack are same nodes:

        fab -R openstack -- "usermod -a -G contrail heat"

        Execute following only if config and openstack are different nodes:

        fab -R openstack -- "mkdir -p /etc/contrail/ssl/certs"
        fab -R openstack tasks.helpers.copy:/etc/contrail/vnc_api_lib.ini,/etc/contrail/
        fab -R openstack tasks.helpers.copy:/etc/contrail/ssl/certs,/etc/contrail/ssl
        fab -R openstack -- "chown -R heat:heat /etc/contrail"

        Execute following to restart services,
        fab -R openstack -- "service heat-api restart"
        fab -R openstack -- "service heat-engine restart"
        fab -R openstack -- "service heat-api-cfn restart"