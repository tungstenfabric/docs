# Introduction:
Ansible inventory file has knobs to get the keystone related params and use it when bringing up contrail cluster using container. We don’t have playbook to provision open-stack using ansible, so we are now depending on fab to provision open-stack.

Also steps to provision contrail-neutron-plugin/neutron server in open-stack node and nova-compute in compute node are detailed here.

## Section1: Steps to bring up open-stack using FAB:
1. Copy/Install contrail-install-packages_<release>-<build>~<sku>_all.deb to the open-stack node

        dpkg -i /path/to/contrail-install-packages_<release>-<build>~<sku>_all.deb
        /opt/contrail/contrail_packages/setup.sh

2. Populate testbed.py with openstack role and provision openstack 
   Example: (http://10.84.5.120/cs-shared/ijohnson-dev/ansible/testbed.py)

        cd /opt/contrail/utils
        fab install_orchestrator
        fab setup_orchestrator

## Section2: Manual steps to provision neutron/neutron-plugin-contrail in open-stack node:

1. Install neutron-server/neutron-plugin-contrail and related packages

        apt-get install neutron-server neutron-plugin-contrail python-neutron-lbaas

2. Configure neutron.conf by executing,

        /opt/contrail/bin/quantum-server-setup.sh

3. Create neutron user/endpoint and service tenant by executing,

        /opt/contrail/bin/setup-quantum-in-keystone --ks_server_ip  <openstacknodeip> --quant_server_ip  <openstacknodeip> --tenant  admin --user admin --password contrail123 --svc_password contrail123 --svc_tenant_name  service --root_password None --region_name RegionOne  

4. Configure /etc/neutron/plugins/opencontrail/ContrailPlugin.ini

        openstack-config --set  /etc/neutron/plugins/opencontrail/ContrailPlugin.ini APISERVER api_server_ip <LB container ip>
        openstack-config --set  /etc/neutron/plugins/opencontrail/ContrailPlugin.ini APISERVER api_server_port 8082
        openstack-config --set  /etc/neutron/plugins/opencontrail/ContrailPlugin.ini APISERVER contrail_extensions ipam:neutron_plugin_contrail.plugins.opencontrail.contrail_plugin_ipam.NeutronPluginContrailIpam,policy:neutron_plugin_contrail.plugins.opencontrail.contrail_plugin_policy.NeutronPluginContrailPolicy,route-table:neutron_plugin_contrail.plugins.opencontrail.contrail_plugin_vpc.NeutronPluginContrailVpc,contrail:None
        openstack-config --set  /etc/neutron/plugins/opencontrail/ContrailPlugin.ini COLLECTOR analytics_api_ip <LB container ip>
        openstack-config --set  /etc/neutron/plugins/opencontrail/ContrailPlugin.ini COLLECTOR analytics_api_port 8081
        openstack-config --set  /etc/neutron/plugins/opencontrail/ContrailPlugin.ini KEYSTONE auth_url http://<openstacknodeip>1:35357/v2.0
        openstack-config --set  /etc/neutron/plugins/opencontrail/ContrailPlugin.ini KEYSTONE admin_user admin
        openstack-config --set  /etc/neutron/plugins/opencontrail/ContrailPlugin.ini KEYSTONE admin_password contrail123
        openstack-config --set  /etc/neutron/plugins/opencontrail/ContrailPlugin.ini KEYSTONE admin_tenant_name admin

5. Point neutron to the contrail neutron plugin config

        sed -i 's/^NEUTRON_PLUGIN_CONFIG/#NEUTRON_PLUGIN_CONFIG/g' /etc/default/neutron-server
        echo 'NEUTRON_PLUGIN_CONFIG="/etc/neutron/plugins/opencontrail/ContrailPlugin.ini"' >> /etc/default/neutron-server
        service neutron-server restart

## Section3: Steps to bring up contrail using ANSIBLE and integrate with existing open-stack:

1. Clone contrail-ansible (https://github.com/Juniper/contrail-ansible)

        git clone https://github.com/Juniper/contrail-ansible.git

2. Populate inventory with keystone params 
   Example: (http://10.84.5.120/cs-shared/ijohnson-dev/ansible/testbed.ini)

3. Use OS provided sources.list not the SM provided one

        cd contrail-ansible/playbooks
        ansible -i inventory/testbed.ini all:children -a "cp /etc/apt/sources.list.save /etc/apt/sources.list" -u root --ask-pass 
        ansible -i inventory/testbed.ini all:children -a "sed -i '57,65d' /etc/apt//sources.list" -u root --ask-pass  
        ansible -i inventory/testbed.ini all:children -a "apt-get update" -u root --ask-pass  #(apt-get update)

4. Provision contrail using containers

        cd contrail-ansible/playbooks
        ansible-playbook -i inventory/testbed.ini site.yml --user root --ask-pass

**NOTE**: We can avoid "--user root --ask-pass" args from **step3/4** If we have setup passwordless ssh to base hosts
      in the cluster by following **Step 1** in https://github.com/Juniper/contrail-ansible/wiki/Quickstart-Guide-with-ini-file-based-inventory

## Section 4: Manual steps to provision nova-compute in compute node:

1. Copy/Install contrail-install-packages_<release>-<build>~<sku>_all.deb in the compute node

Compute node refers to the base host where agent container is chosen to launched.

        dpkg -i /path/to/contrail-install-packages_<release>-<build>~<sku>_all.deb
        /opt/contrail/contrail_packages/setup.sh

2. Install nova-compute packages and prepare the compute host.

        apt-get install contrail-setup nova-compute 
        ln -sf /bin/true /sbin/chkconfig     

3. Create /etc/contrail/ctrl-details

        echo "export SERVICE_TOKEN=<serviceToken>" >> /etc/contrail/ctrl-details
        echo "export AUTH_PROTOCOL=http" >> /etc/contrail/ctrl-details
        echo "export QUANTUM_PROTOCOL=http" >> /etc/contrail/ctrl-details
        echo "export ADMIN_TOKEN=<adminToken>" >> /etc/contrail/ctrl-details
        echo "export CONTROLLER=<opensackIp>" >> /etc/contrail/ctrl-details
        echo "export AMQP_SERVER=<rabbitIp>" >> /etc/contrail/ctrl-details
        echo "export HYPERVISOR=libvirt" >> /etc/contrail/ctrl-details
        echo "export NOVA_PASSWORD=<novaPassword>" >> /etc/contrail/ctrl-details
        echo "export NEUTRON_PASSWORD=<neutronPassword>" >> /etc/contrail/ctrl-details
        echo "export SERVICE_TENANT_NAME=service" >> /etc/contrail/ctrl-details
        echo "export KEYSTONE_VERSION=v2.0" >> /etc/contrail/ctrl-details
        echo "export REGION_NAME=RegionOne" >> /etc/contrail/ctrl-details
        echo "export QUANTUM=<opensackIp>" >> /etc/contrail/ctrl-details
        echo "export QUANTUM_PORT=9696" >> /etc/contrail/ctrl-details
        echo "export COMPUTE=1<computeIp>" >> /etc/contrail/ctrl-details
        echo "export SELF_MGMT_IP=<computeIp>" >> /etc/contrail/ctrl-details
        echo "export CONTROLLER_MGMT=<opensackIp>" >> /etc/contrail/ctrl-details

4. Configure nova.conf and nova-compute.conf by executing,

        source /etc/contrail/ctrl-details
        /opt/contrail/bin/compute-server-setup.sh

5. Get /usr/bin/vrouter-port-control (Worksround for bug (https://bugs.launchpad.net/juniperopenstack/+bug/1655543)

        docker cp agent:/usr/bin/vrouter-port-control /usr/bin/vrouter-port-control
        # Delete lines 18 and 19        

6. Add cgroup_device_acl in the qemu.conf

        #Add the following in /etc/libvirt/qemu.conf,
        cgroup_device_acl = [
            "/dev/null", "/dev/full", "/dev/zero",
            "/dev/random", "/dev/urandom",
            "/dev/ptmx", "/dev/kvm", "/dev/kqemu",
            "/dev/rtc", "/dev/hpet","/dev/net/tun",
        ]
7. Restart libvirt-bin service

        service libvirt-bin restart