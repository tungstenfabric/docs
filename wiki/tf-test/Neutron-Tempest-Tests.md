The tempest results for run on R4.1 Build 48 (newton) is [here](http://10.204.216.50/Docs/logs/4.1.0.0-48_2017-11-15_03:11:46/tempest_report.html)

Example tempest.conf used : 
```
[root@ansible-runner tempest]# cat etc/tempest.conf

[dashboard]
login_url = http://10.204.216.58/horizon/auth/login/
dashboard_url = http://10.204.216.58/horizon

[DEFAULT]
log_file = ./tempest.log
debug = True

[identity]
auth_version = v2
alt_tenant_name = alt_demo
alt_password = contrail123
alt_username = alt_demo
disable_ssl_certificate_validation = True
tenant_name = demo
password = contrail123
username = demo
uri_v3 = http://10.204.216.58:5000/v3/
uri = http://10.204.216.58:5000/v2.0/

[auth]
use_dynamic_credentials = True
admin_project_name = admin
admin_password = contrail123
admin_username = admin

[image]
http_image = http://10.204.216.50/images/cirros/cirros-0.3.5-x86_64-disk.img

[compute]
allow_tenant_isolation = true
image_alt_ssh_password = cubswin:)
image_alt_ssh_user = cirros
image_ref_alt = f0113a8d-cd4a-4d7b-b39e-8684d696a3ef
flavor_ref_alt = 8
flavor_ref = 7
min_compute_nodes = 3
image_ref = f0113a8d-cd4a-4d7b-b39e-8684d696a3ef
ssh_user = cirros

[validation]
run_validation = true
image_ssh_password = cubswin:)
image_ssh_user = cirros

[network]
floating_network_name = public_net
public_network_id = 71b45d3a-78d1-42d6-90f1-c43dda3a990e

[network-feature-enabled]
floating_ips = true
api_extensions = allowed-address-pairs,extra_dhcp_opt,security-group,floating_ips,port_security,ipv6,router,quotas,binding

[compute-feature-enabled]
scheduler_available_filters = RetryFilter, AvailabilityZoneFilter, RamFilter, DiskFilter, ComputeFilter, ComputeCapabilitiesFilter, ImagePropertiesFilter, ServerGroupAntiAffinityFilter, ServerGroupAffinityFilter
cold_migration = false
live_migration = false
[identity-feature-enabled]
api_v3 = false
api_v2_admin = false
api_v2 = false

[service_available]
manila = False
ironic = False
ceilometer = False
trove = False
sahara = False
swift = False
cinder = False
horizon = False
glance = True
heat = True
nova = True
neutron = True
```

### Known failures
```
test_update_subnet_gw_dns_host_routes_dhcp - https://bugs.launchpad.net/juniperopenstack/+bug/1617403

test_create_update_port_with_second_ip https://bugs.launchpad.net/juniperopenstack/+bug/1364677
test_update_port_with_security_group_and_extra_attributes : Bug https://bugs.launchpad.net/juniperopenstack/+bug/1604923

test_update_port_with_security_group_and_extra_attributes : https://bugs.launchpad.net/juniperopenstack/+bug/1604923

test_update_port_with_two_security_groups_and_extra_attributes : https://bugs.launchpad.net/juniperopenstack/+bug/1604923

tempest.api.network.test_routers.RoutersIpV6Test.test_update_delete_extra_route : https://bugs.launchpad.net/juniperopenstack/+bug/1729509

tempest.api.network.test_routers_negative.DvrRoutersNegativeTest.test_router_create_tenant_distributed_returns_forbidden : https://bugs.launchpad.net/juniperopenstack/+bug/1617403

tempest.api.network.test_tags.TagsTest.test_create_list_show_update_delete_tags : https://bugs.launchpad.net/juniperopenstack/+bug/1729511

tempest.api.compute.security_groups.test_security_group_rules_negative.SecurityGroupRulesNegativeTestJSON
test_create_security_group_rule_with_non_existent_id
test_delete_security_group_rule_with_non_existent_id
test_delete_nonexistent_security_group
test_security_group_get_nonexistent_group
test_update_non_existent_security_group
Multiple cases like above may sometimes fail with this bug : https://bugs.launchpad.net/juniperopenstack/+bug/1729775

test_update_router_set_gateway : https://bugs.launchpad.net/juniperopenstack/+bug/1725370

tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_update_router_admin_state  https://bugs.launchpad.net/juniperopenstack/+bug/1352822

tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops,: https://bugs.launchpad.net/juniperopenstack/+bug/1330903

```