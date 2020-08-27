## Setting up the undercloud environment.
   Use Centos7.5

Log in to your machine (baremetal or VM) where you want to install the undercloud as a non-root user (such as the stack user):
```
ssh root@<undercloud-machine>
```
```
yum install -y ipmitool
yum install -y python-requests
```
If you don’t have a non-root user created yet, log in as root and create one with following commands:
```
sudo useradd stack
sudo passwd stack  # specify a password

echo "stack ALL=(root) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/stack
sudo chmod 0440 /etc/sudoers.d/stack

su - stack
```
## Undercloud installation
Ensure that there is a FQDN hostname set and that the $HOSTNAME environment variable matches that value.You can set the hostname settings manually. The manual steps are as follows:

```
undercloud_name=`hostname -s`
undercloud_suffix=`hostname -d`
echo $undercloud_name
echo $undercloud_suffix
sudo hostnamectl set-hostname ${undercloud_name}.${undercloud_suffix}
sudo hostnamectl set-hostname --transient ${undercloud_name}.${undercloud_suffix}
```
Get the undercloud ip and set the correct entries in /etc/hosts, ie (assuming the mgmt nic is eth0):
```
undercloud_ip=`ip addr sh dev eth0 |grep "inet " |awk '{print $2}' |awk -F"/" '{print $1}'`
#Make sure the echoed value is showing your management ip
echo $undercloud_ip
In the /etc/host file have an entry like this
<mgmt_ip< <fqdn> <hostname>
# Make sure you have the FQDN entry in the /etc/hosts file like in the example given below
# 12.2.2.2 undercloud_hostname.domain_name undercloud_hostname
```
tripleo queens/current
```
tripeo_repos=`python -c 'import requests;r = requests.get("https://trunk.rdoproject.org/centos7-queens/current"); print r.text ' |grep python2-tripleo-repos|awk -F"href=\"" '{print $2}'|awk -F"\"" '{print $1}'`
sudo yum install -y https://trunk.rdoproject.org/centos7-queens/current/${tripeo_repos}
sudo tripleo-repos -b queens current
sudo yum install -y python-tripleoclient
cp /usr/share/instack-undercloud/undercloud.conf.sample ~/undercloud.conf
```
## Modify the undercloud.conf with the following entries:
```
[DEFAULT]
local_ip = 192.168.24.1/24
local_interface = <control_data_interface>
masquerade_network = 192.168.24.0/24
enable_node_discovery = true
discovery_default_driver = pxe_ipmitool
[ctlplane-subnet]
cidr = 192.168.24.0/24
dhcp_start = 192.168.24.5
dhcp_end = 192.168.24.24
inspection_iprange = 192.168.24.100,192.168.24.120
gateway = 192.168.24.1
```
Ensure you have 0644 permission to all interface files  under /etc/sysconfig/network-scripts/ifcfg-*
```
openstack undercloud install
```
## Overcloud image download and upload to glance
```
mkdir images
cd images
curl -O https://images.rdoproject.org/queens/rdo_trunk/current-tripleo-rdo/ironic-python-agent.tar
curl -O https://images.rdoproject.org/queens/rdo_trunk/current-tripleo-rdo/overcloud-full.tar
tar xvf ironic-python-agent.tar
tar xvf overcloud-full.tar
source ~/stackrc
openstack overcloud image upload
```

## Node discovery for BareMetal Servers
```

openstack baremetal node list (The output will be empty at this time)
```
Set the machine you want to be discovered and auto-enrolled in ironic using the ipmitool command

Set the machine to pxe boot and start it
```
ipmitool -I lanplus -H <ipmi_address> -U <ipmi_username> -P <ipmi_password> -L ADMINISTRATOR chassis bootdev pxe options=persistent
ipmitool -I lanplus -H  <ipmi_address> -U <ipmi_username> -P <ipmi_password> -L ADMINISTRATOR chassis power on
ipmitool -I lanplus -H <ipmi_address> -U <ipmi_username> -P <ipmi_password> -L ADMINISTRATOR chassis power cycle
```
Make sure no other dhcp servers responds to the pxe/dhcp request from the node that is getting discovered

Reboot the machine to be discovered.

Observe in the console if it pxe boots the introspection ramdisk from the undercloud machine. This may take a while
```
openstack baremetal node list
```
The above command should list the discovered node in the enroll state