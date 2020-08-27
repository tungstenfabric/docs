Users could manually populate tempest.conf and run the below selected tests or choose to auto-populate tempest.conf using the below steps 

#Initial Setup
    
    git clone https://github.com/Juniper/tempest
    cd tempest

    sudo apt-get update
    sudo apt-get install git python2.7-dev libxml2 libxml2-dev libxslt-dev python-pip libffi-dev sshpass

#Set environment for the run
    export TEMPEST_DIR=<path of checked out tempest code> 
    export WORKSPACE=$TEMPEST_DIR
    export KEYSTONE_SERVICE_HOST=<IP of keystone 
    export PUBLIC_NETWORK_NAME="public_net"
    export PUBLIC_NETWORK_SUBNET="10.204.219.200/29"
    export PUBLIC_NETWORK_RI_FQ_NAME="default-domain:admin:$PUBLIC_NETWORK_NAME:$PUBLIC_NETWORK_NAME"
    export PUBLIC_NETWORK_RT=10003
    export ROUTER_ASN=64510

    export HTTP_IMAGE_PATH="http://10.204.216.51/images/cirros/cirros-0.3.1-x86_64-uec.tar.gz"
    KEYSTONE_SERVICE_HOST_USER="root"
    KEYSTONE_SERVICE_HOST_PASSWORD="c0ntrail123"
    export API_SERVER_IP=<IP of Contrail Config node>
    export API_SERVER_HOST_USER="root"
    export API_SERVER_HOST_PASSWORD="c0ntrail123"
    
    export TENANT_ISOLATION=true
    cd $TEMPEST_DIR
    # openstacrc 
    export OS_USERNAME=admin
    export OS_PASSWORD=contrail123
    export OS_TENANT_NAME=admin
    export OS_AUTH_URL=http://$KEYSTONE_SERVICE_HOST:5000/v2.0/
    export OS_NO_CACHE=1
    
    rm -f $WORKSPACE/result.xml
    
#run neutron tempest cases
    bash -x $WORKSPACE/run_contrail_tempest.sh -p -V -r $WORKSPACE/result.xml -t -- tempest.api.network.test_networks tempest.api.network.test_routers tempest.api.network.test_ports.PortsTestJSON tempest.api.network.test_ports.PortsTestXML tempest.scenario.test_network_advanced_server_ops tempest.scenario.test_network_basic_ops tempest.api.network.test_security_groups tempest.api.network.test_floating_ips tempest.api.network.test_security_groups_negative tempest.api.network.test_extra_dhcp_options  tempest.api.network.test_networks_negative tempest.api.network.test_routers_negative tempest.api.compute.servers.test_attach_interfaces tempest.api.compute.servers.test_server_metadata tempest.api.compute.servers.test_server_addresses tempest.api.compute.servers.test_server_addresses_negative tempest.api.compute.servers.test_multiple_create 
Junit style test-results will be stored in $WORKSPACE/result.xml for post-analysis by tools like Jenkins

### Note
* run_contrail_tempest.sh : Primarily creates public VN(and its RT),  installs cirros image, and populates tempest.conf suitably
* The above cases assume that public network reachability is already setup (ex: peering with MX). If it is not done, you may want to avoid running tempest.scenario*, tempest.api.network.test_routers tests from the above and add the below tests : 
tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id tempest.api.network.test_routers.RoutersTest.test_create_router_setting_tenant_id tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router tempest.api.network.test_routers.RoutersTest.test_update_router_admin_state tempest.api.network.test_routers.RoutersTest.test_update_router_unset_gateway

* Router extra-route tests, filtering by router-id, multiple IPs on the same port, and updating enable-snat option in router-gateway are not supported