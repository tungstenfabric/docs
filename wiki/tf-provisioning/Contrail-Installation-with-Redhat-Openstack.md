

### Contrail With Red Hat Enterprise Linux OpenStack Platform
***

Contrail uses OpenStack, Keystone, and AMQP services from the Red Hat OpenStack (RHOSP) node. Before installing or provisioning Contrail, you should provision one or more RHOSP nodes or VMs running OpenStack services, including Keystone and AMQP, and bring up those services. The Contrail installation gets information about these services, such as IP address, username, password, and the like, from the testbed.py (explained later in this topic).

### Install and Configure RHOSP
***
Using the appropriate product version, install and bring up the RHOSP node. The following link provides installation and other information about RHOSP. Check your Red Hat customer portal for the most recent documentation.

https://access.redhat.com/documentation/en/red-hat-enterprise-linux-openstack-platform/

##### Update RHOSP nodes with Contrail Controller Information


###### 1. create a link to the Keystonrc file.

Copy or create a symlink to /root/keystonerc_admin at /etc/contrail/openstackrc:

```
ln -s /root/keystonerc_admin /etc/contrail/openstackrc
```


###### 2. Verify networking service.

Because the networking service will be provided by the Contrail controller, you must disable "neutron-server" if it is already enabled in the RHOSP nodes.

To check the status of neutron-server:
```
service neutron-server status
```

To disable neutron-server:
```
service neutron-server stop
```


###### 3. Update networking service configuration in nova.conf.

Because the Contrail controller provides Neutron services, set the Neutron URL after replacing \<controller-ip\>.

The \<controller-ip\> can be the first Contrail controller IP address, or the Contrail VIP address if the Contrail services are running in HA mode.

If using RHOSP6 or greater:
```
openstack-config --set /etc/nova/nova.conf neutron url http://<controller-ip>:9696
```

If using RHOSP5:
```
openstack-config --set /etc/nova/nova.conf DEFAULT neutron_url http://<controller-ip>:9696
```

Then set up the neutron_admin_auth_url, after replacing \<keystone-ip\> with the IP address of the Keystone server:

```
openstack-config --set /etc/nova/nova.conf DEFAULT neutron_admin_auth_url http://<keystone-ip>:35357/v2.0
```


###### 4. Update the networking service API endpoint.

Create the networking service API endpoint, after replacing \<controller-ip\>. The \<controller-ip\> can be the first Contrail controller IP address, or the Contrail VIP address if the Contrail services are running in HA mode.

Note: The networking service API endpoint could be pointing to the RHOSP node if neutron-server is installed in the RHOSP node. In this case, the existing endpoint must be removed prior to adding the above endpoint.

```
source /etc/contrail/openstackrc;
keystone endpoint-create --region <openstack-region-name> \
                         --service neutron \
                         --publicurl <http://<controller-ip>:9696> \
                         --adminurl <http://<controller-ip>:9696> \
                         --internalurl <http://<controller-ip>:9696>
```

For newer versions of OpenStack use the following command.

```
openstack endpoint create --region <openstack-region-name> \
                          --publicurl 'http://<controller-ip>:9696' \
                          --adminurl 'http://<controller-ip>:9696' \
                          --internalurl 'http://<controller-ip>:9696' neutron
```
To list endpoints:
```
source /etc/contrail/openstackrc; keystone endpoint-list
```

To delete an existing endpoint:

\<endpoint-id\> is the ID of the endpoint which can be seen in "keystone endpoint-list" output.

```
source /etc/contrail/openstackrc; keystone endpoint-delete <endpoint-id>
```


###### 5. Restart services.

Restart the following services to make all of your changes effective:

```
service openstack-nova-api restart
service openstack-nova-conductor restart
service openstack-nova-scheduler restart
service openstack-nova-consoleauth restart
````


#### Bring up Contrail Services
***

##### RHEL Repos

The Contrail packages depend on a number of upstream RHEL packages that are hosted in RHEL repos. The relevant repos must be enabled in the node. When the Contrail packages are installed, all of the dependent packages are pulled from enabled RHEL repos and get installed automatically.

Use the following RHEL link to understand how to subscribe and enable RHEL repos:

For registering and subscription manager: https://access.redhat.com/solutions/253273

The following repos need to be enabled to successfully install Contrail controller.
Note: For each of the following, replace \<rhosp-version\> with your RHOSP version. For example: RHOSP7/Kilo - 7.0, RHOSP6/Juno - 6.0

```
subscription-manager repos --enable=rhel-7-server-extras-rpms
subscription-manager repos --enable=rhel-7-server-rpms
subscription-manager repos --enable=rhel-7-server-openstack-<rhosp-version>-rpms
```


Important Notes 

Read before proceeding with Contrail installation.

##### Contrail Wrapper Package Installation
Packages needed to bring up Contrail controller are provided as a wrapper package: 

contrail-install-packages-\<release\>-\<version\>~\<sku\>.el7.noarch.rpm.

###### Install contrail-install-packages:
Copy the Contrail wrapper package into the first Contrail controller node. Install the package and run setup.sh.

```
yum localinstall --disablerepo=* /path/to/contrail-install-packages-\<release\>-\<version\>~\<sku\>.el7.noarch.rpm
```

###### Execute setup.sh
The setup.sh execution creates a local repo with all Contrail packages under the directory: ```/opt/contrail/contrail_install_repo ``` and also installs basic required packages (contrail-fabric-utils, python-fabric and contrail-setup) in the node:

```
/opt/contrail/contrail_packages/setup.sh
```

##### Configure testbed.py
Configure a testbed.py at ```/opt/contrail/utils/fabfile/testbeds/testbed.py``` of the first Contrail Controller node. This testbed.py is the configuration file for Contrail installation and provisioning. Example testbeds  are available in the same directory. Also see Detailed Testbed Configuration document at Juniper Techwiki. 

##### Update testbed.py
Update RHOSP related info in the testbed.py in the following sections:

```
#In environments where Keystone is deployed outside of Contrail provisioning
#scripts, you can use the below options
#
# Note :
# "insecure" is applicable only when protocol is https
# The entries in env.keystone overrides the below options which used
# to be supported earlier :
#  service_token
#  keystone_ip
#  keystone_admin_user
#  keystone_admin_password
#  region_name
#
env.keystone = {
    'keystone_ip'     : '10.84.14.45', # IP Address of the Keystone Server (In case of OpenStack HA, provide OpenStack VIP)
    'auth_protocol'   : 'http',        # Auth Protocol used by Keystone
    'auth_port'       : '35357',       # Auth Port used by Keystone
    'admin_token' : '45b925b65ca44a3f90b2f55e67455dc2',  # Admin Token of Keystone
    'admin_user'      : 'admin',       # Admin user name of Keystone
    'admin_password'  : 'c0ntrail123', # Password of Admin user of Keystone 
    'nova_password' : '799b7e246efd43ef', # Password of nova service 
    'neutron_password' : '48f8fdeb541a43bb', # Password of networking service 
    'service_tenant' : 'services',    # Tenant name of services like nova, neutron, glance...etc.
    'admin_tenant'    : 'admin',      # Tenant name of admin user
    'region_name'     : 'regionOne',  # OpenStack region to use. Default is regionOne
    'insecure'        : 'False',      # Insecure option set for Keystone. Default is False
    'manage_neutron'  : 'no',         # Configure neutron user/role in keystone server. Default = 'yes' 
}

```

```
# In environments where OpenStack services are deployed independently
# from Contrail, you can use the following options
# service_token : Common service token for for all services like nova,
#                 neutron, glance, cinder etc. Is usually the same as the admin token
# amqp_host     : IP of AMQP Server to be used in OpenStack
# manage_amqp   : Default = 'no', if set to 'yes' provisions AMQP in OpenStack nodes and
#                 OpenStack services uses the AMQP in OpenStack nodes instead of config nodes.
#                 amqp_host is neglected if manage_amqp is set
#
env.openstack = {
    'service_token' : '45b925b65ca44a3f90b2f55e67455dc2', # the admin token can be used
    'amqp_host' : '10.84.14.45',          # IP of AMQP Server to be used in OpenStack node
    'manage_amqp' : 'no',                 # Manage seperate AMQP for OpenStack services in OpenStack nodes.
    'osapi_compute_workers' : 40,         # Default 40, For low memory system reduce the osapi compute workers thread.
    'conductor_workers' : 40,             # Default 40, For low memory system reduce the conductor workers thread.
}
```

```
#Config node related config knobs
#amqp_hosts : List of customer deployed AMQP servers to be used by config services.
#amqp_port : Port of the customer deployed AMQP servers.
env.cfgm = {
    'amqp_hosts' : ['10.84.14.45'],
    'amqp_port' : '5672'           
}
```

##### Contrail Controller Installation
When the testbed.py is configured, Contrail fabric utils can be used to install and provision the Contrail controller.

###### Pre-check
Make sure all nodes are reachable and properly updated in testbed.py. One simple way is to execute and see if it passes. Also see if the command was executed in all nodes.

```
fab all_command:"uname –a"
```

###### Multi-Node Setup
In case of a multi-node Contrail controller setup, contrail-install-packages must be installed in all nodes except the RHOSP nodes. From the first Contrail controller node, execute the following command:

```
fab install_pkg_all_without_openstack:/path/to/contrail-install-packages-\<release\>-\<version\>~\<sku\>.el7.noarch.rpm
```


###### Disable iptables:

Contrail install and setup needs iptables to be permanently disabled. This a Contrail known issue to be resolved at a later date.  

Iptables can be disabled by using the following fab tasks. Basically, ```fab all_command``` executes the given command in all nodes configured in testbed.py.

To disable IP tables in all nodes:

````
 fab all_command:"iptables --flush"
 fab all_command:"sudo service iptables stop; echo pass"
 fab all_command:"sudo service ip6tables stop; echo pass"
 fab all_command:"sudo systemctl stop firewalld; echo pass"
 fab all_command:"sudo systemctl status firewalld; echo pass"
 fab all_command:"sudo chkconfig firewalld off; echo pass"
 fab all_command:"sudo /usr/libexec/iptables/iptables.init stop; echo pass"
 fab all_command:"sudo /usr/libexec/iptables/ip6tables.init stop; echo pass"
 fab all_command:"sudo service iptables save; echo pass"
 fab all_command:"sudo service ip6tables save; echo pass"
````

###### Install Contrail Controller:
Because contrail-install-packages is installed in all Contrail controller nodes, and the testbed.py is configured, all Contrail packages required for Contrail controller installation are available in local repos in each node. Trigger Contrail controller installation with the following command:

```
fab install_without_openstack
```

or

```
fab install_without_openstack:manage_nova_compute=no (To Skip nova compute installation)
```

##### Contrail Controller Provisioning 
Use the following to provision Contrail controller. This step modifies the config files for each Contrail component and brings up Contrail services:

```
fab setup_without_openstack
```

or

```
fab setup_without_openstack:manage_nova_compute=no (To Skip nova compute service configurations)
```
###### Verify Setup
Use the commands ```contrail-status``` and ```openstack-status``` to verify the setup status:

````
fab all_command:”contrail-status; echo pass”
fab all_command:”openstack-status”

````


###### Important Notes:
1) Currently, Contrail must have IP tables disabled. 
To disable IP tables: 

```
iptables --flush
sudo service iptables stop
sudo service ip6tables stop
sudo systemctl stop firewalld
sudo systemctl status firewalld
sudo chkconfig firewalld off
sudo /usr/libexec/iptables/iptables.init stop
sudo /usr/libexec/iptables/ip6tables.init stop
sudo service iptables save
sudo service ip6tables save
```

2) Disable Network Manager:
Network Manager is enabled by default in RHEL. Disable it by executing the following commands in the target nodes:

```
service NetworkManager stop
chkconfig NetworkManager off
```

In each enabled interface, disable NM_CONTROLLED in the config file (available at /etc/sysconfig/network-scripts/) and ensure the following configuration is added:
```
NM_CONTROLLED=no
ONBOOT=yes
```

3) Services such as OVS from RHOSP are not compatible with Contrail services. Similarly, installing unnecessary packages in the Contrail nodes may lead to dependency failures, for example, some OpenStack packages have different dependencies than those of Contrail. Install only required services/packages in the node.

4) Always check the recommended kernel version to use with Contrail nodes before starting the installation.
   To see the current kernel version in the node:
   ```
   uname -r
   ```