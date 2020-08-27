(See also https://github.com/Juniper/contrail-controller/wiki/Simple-Gateway)
(See also Noel's network test script is at:  https://github.com/noelbk/devstack/blob/contrail/contrail/test_network.sh )

# Add This on LocalRC

```
CONTRAIL_VGW_INTERFACE=vgw
CONTRAIL_VGW_PUBLIC_SUBNET=10.99.99.0/24 # replace with your floating IP range
CONTRAIL_VGW_PUBLIC_NETWORK=default-domain:admin:public:public
```

# Setup public network in neutron

```
. openrc admin admin
neutron net-create public
public_id=`neutron net-list | awk '/public/{print $2}'`
neutron subnet-create --name public-subnet1 $public_id $CONTRAIL_VGW_PUBLIC_SUBNET --disable-dhcp
```

# Setup floating ip pool in contrail

```
   python /opt/stack/contrail/controller/src/config/utils/create_floating_pool.py --public_vn_name default-domain:admin:public --floating_ip_pool_name floatingip_pool
   python /opt/stack/contrail/controller/src/config/utils/use_floating_pool.py --project_name default-domain:admin --floating_ip_pool_name default-domain:admin:public:floatingip_pool
```

The "use_floating_pool" script associates the floating ip pool with a project that is allows to use the floating ip. Multiple projects can be associated with a single floating ip pool. This allows for fine grain control of what projects are allowed to use what pools.

# Setup Security Group

```
. openrc admin demo
nova secgroup-list
nova secgroup-list-rules default
nova secgroup-add-rule default tcp 22 22 0.0.0.0/0
nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0
nova secgroup-list-rules default
```

# Setup floating ip
```
neutron floatingip-create $public_id
neutron floatingip-associate $floatingip_id $port_id
```

The create a floating ip address in a project other than the project that owns the target network. Use the "--tenant_id" option to the "floatingip-create" neutron command. This assumes that the user invoking the command has provided credentials to the project owning the public network.

# Test it
neutron floatingip-show $floatingip_id
ssh cirros@$floatingip_ip
