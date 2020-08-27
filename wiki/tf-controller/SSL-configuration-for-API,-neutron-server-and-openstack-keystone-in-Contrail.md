# Introduction

Provisioning keystone, api-server and neutron-server with SSL. This is achieved by configuring keystone with native SSL and api-server/neutron-server through SSL termination using Haproxy.

# Section1: Keystone Settings for SSL

## 1. Create ssl directories and assign ownership

        # In Keystone Node,
        mkdir -p /etc/keystone/ssl; chown keystone:keystone /etc/keystone/ssl

## 2. Download the script to create self-signed certs

Download the script from github, if provisionig contrail release less than 3.0.3.2.
otherwise the script will be available at /opt/contrail/bin/create-ssl-certs.sh when 
installing contrail-setup package.

        wget --no-check-certificate https://raw.githubusercontent.com/Juniper/contrail-provisioning/master/contrail_provisioning/common/scripts/create-ssl-certs.sh

## 3. Create self-signed SSL certs for Keystone

        # In Keystone Node,
        chmod +x create-ssl-certs.sh
        create-ssl-certs.sh <KeystoneNodeIP|VIP> /etc/keystone/ssl/ keystone

## 4. Sync SSL certs with the all other keystone nodes

        scp -R /etc/keystone/ssl/ <user>@<KeystoneNodeIp2>:/etc/keystone/ssl/
        scp -R /etc/keystone/ssl/ <user>@<KeystoneNodeIp3>:/etc/keystone/ssl/

## 5. Configure keystone.conf, nova.conf, glance-api.conf, glance-registry.conf & local_settings

        openstack-config --set /etc/keystone/keystone.conf ssl enable true
        openstack-config --set /etc/keystone/keystone.conf ssl certfile /etc/keystone/ssl/certs/keystone.pem
        openstack-config --set /etc/keystone/keystone.conf ssl keyfile /etc/keystone/ssl/private/keystone.key
        openstack-config --set /etc/keystone/keystone.conf ssl ca_certs /etc/keystone/ssl/certs/keystone_ca.pem
        openstack-config --set /etc/keystone/keystone.conf eventlet_server_ssl enable true
        openstack-config --set /etc/keystone/keystone.conf eventlet_server_ssl certfile /etc/keystone/ssl/certs/keystone.pem
        openstack-config --set /etc/keystone/keystone.conf eventlet_server_ssl keyfile /etc/keystone/ssl/private/keystone.key
        openstack-config --set /etc/keystone/keystone.conf eventlet_server_ssl ca_certs /etc/keystone/ssl/certs/keystone_ca.pem
        
        # Update /etc/nova/nova.conf
        openstack-config --set /etc/nova/nova.conf keystone_authtoken insecure true
        openstack-config --set /etc/nova/nova.conf keystone_authtoken auth_protocol https
        openstack-config —set /etc/nova/nova.conf DEFAULT neutron_api_insecure True
        openstack-config —set /etc/nova/nova.conf DEFAULT neutron_admin_auth_url https://<KeystoneNodeIp>:35357/v2.0/
        openstack-config —set /etc/nova/nova.conf DEFAULT neutron_url https://<neutron nodeIP>:9696/
        
    
        service nova-api restart
  
        # Update glance-api.conf
        openstack-config --set /etc/glance/glance-api.conf keystone_authtoken insecure true
        openstack-config --set /etc/glance/glance-api.conf keystone_authtoken auth_protocol https
 
        service glance-api restart

        # Update glance-registry.conf
        openstack-config --set /etc/glance/glance-registry.conf keystone_authtoken insecure true
        openstack-config --set /etc/glance/glance-registry.conf keystone_authtoken auth_protocol https

        service glance-registry restart

        # Update nova.conf on all the compute nodes

        openstack-config --set /etc/nova/nova.conf keystone_authtoken insecure true
        openstack-config --set /etc/nova/nova.conf keystone_authtoken auth_protocol https
        openstack-config —set /etc/nova/nova.conf DEFAULT neutron_api_insecure True
        openstack-config —set /etc/nova/nova.conf DEFAULT neutron_admin_auth_url https://<KeystoneNodeIp>:35357/v2.0/
        openstack-config —set /etc/nova/nova.conf DEFAULT neutron_url https://<neutron nodeIP>:9696/

        # Update Local settings for Dashboard
        Make sure the following is updated in /etc/openstack-dashboard/local_settings
        
        OPENSTACK_SSL_NO_VERIFY = True // Uncomment it
        OPENSTACK_KEYSTONE_URL = "https://%s:5000/v2.0" % OPENSTACK_HOST // Change to https
   
## 6. Add keystone endpoint with https url

Update the existing keystone/neutron endpoint with'https' in url.
        
        For Keystone:
        mysql -u keystone -p keystone  -h localhost use keystone;
        select * from service; // Note down service ID for “keystone"
        select * from endpoint where service_id='<service ID of keystone>’; // Shows current configuration

        update endpoint set url='https://<IP Address of openstack node>:$(public_port)s/v2.0' where (service_id=‘<service ID of keystone>' and interface='public');
        update endpoint set url='https://<IP Address of openstack node>:$(admin_port)s/v2.0' where (service_id='<service ID of keystone>' and interface='admin');
        update endpoint set url='https://<IP Address of openstack node>:$(admin_port)s/v2.0' where (service_id='<service ID of keystone>' and interface='internal');

        select * from endpoint where service_id='<service ID of keystone>’;  // To print the updated information
        
        For Neutron:
        select * from service; // Note down service ID for “neutron"
        select * from endpoint where service_id='<service ID of neutron>’; // Shows current configuration
        update endpoint set url='https://<IP Address of Api server>:9696' where service_id='<service ID of neutron>';

        select * from endpoint where service_id='<service ID of neutron>’;  // To print the updated information

## 7. Restart keystone

    service keystone restart



# Section2: api-server SSL settings

## 1. Create ssl directories and assign ownership

        # In api-server Node,
        mkdir -p /etc/contrail/ssl; chown contrail:contrail /etc/contrail/ssl

## 2. Download the script to create self-signed certs

Download the script from github, if provisioning contrail release less than 3.0.3.2.
otherwise the script will be available at /opt/contrail/bin/create-ssl-certs.sh when 
installing contrail-setup package.

        wget --no-check-certificate https://raw.githubusercontent.com/Juniper/contrail-provisioning/master/contrail_provisioning/common/scripts/create-ssl-certs.sh\

## 3. Create self-signed SSL certs for api-server

        # In api-server Node,
        chmod +x create-ssl-certs.sh
        create-ssl-certs.sh <ConfigNodeIP|VIP> /etc/contrail/ssl/ apiserver

## 4. Create certificate bundle

Certificates bundle will be used in Haproxy for SSL termination,

        # In api-server Node,
        cd /etc/contrail/ssl/; cat certs/apiserver_ca.pem private/apiserver.key certs/apiserver.pem >> certs/apiservercertbundle.pem

## 5. Copy keystone certs to api-server node

keystone certificate and CA needs to be available in api-server node , so that
api-server can talk to keystone securely using keystone certs/CA.

        # From api-server node,
        scp <user>@<keystoneNodeIp>:/etc/keystone/ssl/certs/keystone.pem /etc/contrail/ssl/certs/
        scp <user>@<keystoneNodeIp>:/etc/keystone/ssl/certs/keystone_ca.pem /etc/contrail/ssl/certs/
        chown -R contrail:contrail /etc/contrail/ssl/certs/

## 6. Sync SSL certs with the all other config nodes

        scp -R /etc/contrail/ssl/ <user>@<ConfigNodeIp2>:/etc/contrail/ssl/
        scp -R /etc/contrail/ssl/ <user>@<ConfigNodeIp3>:/etc/contrail/ssl/

## 7. Configure api-server frontend/backend in haproxy

Ensure the api-server haproxy config looks like below in /etc/haproxy/haproxy.cfg

        frontend  contrail-api
            bind *:8082 ssl crt /etc/contrail/ssl/certs/apiservercertbundle.pem
            default_backend    contrail-api-backend
            timeout client 3m

        backend contrail-api-backend
            option nolinger
            option forwardfor
            balance     roundrobin
            http-request set-header X-Forwarded-Port %[dst_port]
            http-request add-header X-Forwarded-Proto https if { ssl_fc }
            server <ConfigHostIp1> <ConfigHostIp1>:9100 check inter 2000 rise 2 fall 3
            server <ConfigHostIp2> <ConfigHostIp2>:9100 check inter 2000 rise 2 fall 3
            server <ConfigHostIp3> <ConfigHostIp3>:9100 check inter 2000 rise 2 fall 3

Restart harproxy,

        service haproxy restart

## 8. Configure contrail-keystone-auth.conf & neutron.con

        openstack-config --set /etc/contrail/contrail-keystone-auth.conf KEYSTONE  auth_url https://<KeystoneIp>:<Port>/<version>  // Not needed for Icehouse release
        openstack-config --set /etc/contrail/contrail-keystone-auth.conf KEYSTONE  auth_protocol https
        openstack-config --set /etc/contrail/contrail-keystone-auth.conf KEYSTONE insecure False
        openstack-config --set /etc/contrail/contrail-keystone-auth.conf KEYSTONE certfile /etc/contrail/ssl/certs/keystone.pem
        openstack-config --set /etc/contrail/contrail-keystone-auth.conf KEYSTONE keyfile /etc/contrail/ssl/certs/keystone.pem
        openstack-config --set /etc/contrail/contrail-keystone-auth.conf KEYSTONE cafile /etc/contrail/ssl/certs/keystone_ca.pem

        openstack-config --set /etc/neutron/neutron.conf keystone_authtoken cafile /etc/neutron/ssl/certs/keystone.pem

        chown neutron:neutron /etc/neutron/ssl/certs/apiserver*

## 9. Configure vnc_api_lib.ini

        chown contrail:contrail /etc/contrail/vnc_api_lib.ini 

        openstack-config --set /etc/contrail/vnc_api_lib.ini global insecure False
        openstack-config --set /etc/contrail/vnc_api_lib.ini global certfile /etc/contrail/ssl/certs/apiserver.pem
        openstack-config --set /etc/contrail/vnc_api_lib.ini global keyfile /etc/contrail/ssl/certs/apiserver.pem
        openstack-config --set /etc/contrail/vnc_api_lib.ini global cafile /etc/contrail/ssl/certs/apiserver_ca.pem

        openstack-config --set /etc/contrail/vnc_api_lib.ini auth insecure False
        openstack-config --set /etc/contrail/vnc_api_lib.ini auth AUTHN_PROTOCOL https
        openstack-config --set /etc/contrail/vnc_api_lib.ini auth certfile /etc/contrail/ssl/certs/keystone.pem
        openstack-config --set /etc/contrail/vnc_api_lib.ini auth keyfile /etc/contrail/ssl/certs/keystone.pem
        openstack-config --set /etc/contrail/vnc_api_lib.ini auth cafile /etc/contrail/ssl/certs/keystone_ca.pem
        openstack-config --set /etc/contrail-svc-monitor.conf DEFAULTS api_server_use_ssl True
        openstack-config --set /etc/contrail-schema.conf DEFAULTS api_server_use_ssl True
        openstack-config --set /etc/contrail-device-manager.conf DEFAULTS api_server_use_ssl True

## 10. Restart api-server

        service supervisor-conifg restart



# Section3: neutron-server SSL settings

## 1. Create ssl directories and assign ownership

        # In neutron-server Node,
        mkdir -p /etc/neutron/ssl; chown neutron:neutron /etc/neutron/ssl

        # In api-server Node,
        mkdir -p /etc/contrail/ssl; chown contrail:contrail /etc/contrail/ssl

## 2. Download the script to create self-signed certs

Download the script from github, if provisionig contrail release less than 3.0.3.2.
otherwise the script will be available at /opt/contrail/bin/create-ssl-certs.sh when 
installing contrail-setup package.

        wget --no-check-certificate https://raw.githubusercontent.com/Juniper/contrail-provisioning/master/contrail_provisioning/common/scripts/create-ssl-certs.sh

## 3. Create self-signed SSL certs for neutron-server

        # In neutron-server Node,
        chmod +x create-ssl-certs.sh
        create-ssl-certs.sh <NeutronNodeIP|VIP> /etc/neutron/ssl/ neutron

## 4. Create certificate bundle

Certificates bundle will be used in Haproxy for SSL termination,

        # In neutron-server Node,
        cd /etc/neutron/ssl/; cat certs/neutron_ca.pem private/neutron.key certs/neutron.pem >> certs/neutroncertbundle.pem

## 5. Copy keystone certs to neutron-server node

keystone certificate and CA needs to be available in neutron-server node , so that
neutron-server can talk to keystone securely using keystone certs/CA.

        # From neutron-server node,
        scp <user>@<keystoneNodeIp>:/etc/keystone/ssl/certs/keystone.pem /etc/neutron/ssl/certs/
        scp <user>@<keystoneNodeIp>:/etc/keystone/ssl/certs/keystone_ca.pem /etc/neutron/ssl/certs/
        chown -R neutron:neutron /etc/neutron/ssl/certs/

## 6. Copy api-server certs to config node

api-server certificate and CA needs to be available in neutron-server node , so that
neutron-server can talk to api-server securely using api-server certs/CA.

        # From api-server node,
        scp <user>@<ConfigNodeIp>:/etc/contrail/ssl/certs/apiserver.pem /etc/neutron/ssl/certs/
        scp <user>@<ConfigNodeIp>:/etc/contrail/ssl/certs/apiserver_ca.pem /etc/neutron/ssl/certs/
        chown -R contrail:contrail /etc/contrail/ssl/certs/

## 6. Sync SSL certs with the all other neutron-server node

        scp -R /etc/neutron/ssl/ <user>@<NeutronNodeIp2>:/etc/neutron/ssl/
        scp -R /etc/neutron/ssl/ <user>@<NeutronNodeIp3>:/etc/neutron/ssl/

## 7. Configure neutron-server frontend/backend in haproxy

Ensure the neutron-server haproxy config looks like below in /etc/haproxy.cfg

        frontend neutron-server
            bind *:9696 ssl crt /etc/neutron/ssl/certs/neutroncertbundle.pem
            default_backend    neutron-server-backend

        backend neutron-server-backend
            option nolinger
            option forwardfor
            balance     roundrobin
            http-request set-header X-Forwarded-Port %[dst_port]
            http-request add-header X-Forwarded-Proto https if { ssl_fc }
            server <NeutronHostIp1> <NeutronHostIp1>:9697 check inter 2000 rise 2 fall 3
            server <NeutronHostIp2> <NeutronHostIp2>:9697 check inter 2000 rise 2 fall 3
            server <NeutronHostIp3> <NeutronHostIp3>:9697 check inter 2000 rise 2 fall 3

Restart harproxy,

        service haproxy restart

## 8. Configure neutron.conf

Add the keystone certificate information in keystone_authtoken section of neutron.conf

        openstack-config --set /etc/neutron/neutron.conf keystone_authtoken auth_protocol https
        openstack-config --set /etc/neutron/neutron.conf keystone_authtoken certfile /etc/neutron/ssl/certs/keystone.pem
        openstack-config --set /etc/neutron/neutron.conf keystone_authtoken keyfile /etc/neutron/ssl/certs/keystone.pem
        openstack-config --set /etc/neutron/neutron.conf keystone_authtoken cafile /etc/neutron/ssl/certs/keystone_ca.pem

## 9. Configure ContrailPlugin.ini

Add the api-server certificate information in APISERVER section of ContrailPlugin

        openstack-config --set /etc/neutron/plugins/opencontrail/ContrailPlugin.ini APISERVER use_ssl True
        openstack-config --set /etc/neutron/plugins/opencontrail/ContrailPlugin.ini APISERVER insecure False
        openstack-config --set /etc/neutron/plugins/opencontrail/ContrailPlugin.ini APISERVER certfile /etc/neutron/ssl/certs/apiserver.pem
        openstack-config --set /etc/neutron/plugins/opencontrail/ContrailPlugin.ini APISERVER keyfile /etc/neutron/ssl/certs/apiserver.pem
        openstack-config --set /etc/neutron/plugins/opencontrail/ContrailPlugin.ini APISERVER cafile /etc/neutron/ssl/certs/apiserver_ca.pem

## 10. Configure vnc_api_lib.ini

Configure vnc_api_lib.ini in neutron-server, which will be used by vnc_api client library to talk to api-server.
vnc_api library is used by neutron contrail plugin.

        chown contrail:contrail /etc/contrail/vnc_api_lib.ini 
        usermod -a -G contrail neutron

        # SKIP below commands in (8. Configure vnc_api_lib.ini), if neutron-server/plugin is in same node as config node.
        openstack-config --set /etc/contrail/vnc_api_lib.ini global insecure False
        openstack-config --set /etc/contrail/vnc_api_lib.ini global certfile /etc/neutron/ssl/certs/apiserver.pem
        openstack-config --set /etc/contrail/vnc_api_lib.ini global keyfile /etc/neutron/ssl/certs/apiserver.pem
        openstack-config --set /etc/contrail/vnc_api_lib.ini global cafile /etc/neutron/ssl/certs/apiserver_ca.pem

        openstack-config --set /etc/contrail/vnc_api_lib.ini auth insecure False
        openstack-config --set /etc/contrail/vnc_api_lib.ini auth AUTHN_PROTOCOL https
        openstack-config --set /etc/contrail/vnc_api_lib.ini auth certfile /etc/neutron/ssl/certs/keystone.pem
        openstack-config --set /etc/contrail/vnc_api_lib.ini auth keyfile /etc/neutron/ssl/certs/keystone.pem
        openstack-config --set /etc/contrail/vnc_api_lib.ini auth cafile /etc/neutron/ssl/certs/keystone_ca.pem

## 11. Restart neutron-server

        service neutron-server restart
