1. Checkout the contrail-ansible-deployer repo 

  `git clone http://github.com/Juniper/contrail-ansible-deployer`

2. Go to the ../contrail-ansible-deployer/inventory/hosts.yml file and make the following modifications
   ```
   container_hosts:
      hosts:
         192.168.1.50: -->Make sure you put your ip here
            ansible_connection: local
    ```
3. Go to the ../contrail-ansible-deployer/inventory/group_vars/container_hosts.yml file and make the following modifications

   ```
   CONTAINER_REGISTRY: 192.168.121.21:5000
   REGISTRY_PRIVATE_SECURE: false
   REGISTRY_PRIVATE_INSECURE: true
   contrail_configuration:
     OPENSTACK_VERSION: pike
     LINUX_DISTR: centos7
     CONTRAIL_VERSION: 4.1.0.0-8
     CONTROLLER_NODES: 192.168.1.50
     CONTROL_NODES: 192.168.1.50
     CLOUD_ORCHESTRATOR: openstack
     AUTH_MODE: keystone
     KEYSTONE_AUTH_ADMIN_PASSWORD: c0ntrail123
     KEYSTONE_AUTH_HOST: 192.168.1.210
     KEYSTONE_AUTH_URL_VERSION=/v3
     RABBITMQ_NODE_PORT: 5673
     PHYSICAL_INTERFACE: eth2
     VROUTER_GATEWAY: 192.168.10.1
   roles:
     192.168.1.50:
       configdb:
       config:
       control:
       webui:
       analytics:
       analyticsdb:
       vrouter:
   ```
4. Go to the ../contrail-ansible-deployer/inventory/group_vars/all.yml file and make the following modifications
   ```
   BUILD_VMS: false
   CONFIGURE_VMS: true
   CREATE_CONTAINERS: true
   CENTOS_DOWNLOAD_URL: http://10.87.64.32/
   CENTOS_IMAGE_NAME: CentOS-7-x86_64-GenericCloud-1710.qcow2.xz
   CONTAINER_VM_ROOT_PWD: contrail123
   CONTAINER_VM_CONFIG:
    root_pwd: contrail123
    vcpu: 12
    vram: 64000
    vdisk: 100G
    network:
      subnet_prefix: 192.168.121.0
      subnet_netmask: 255.255.255.0
      gatway: 192.168.121.169
      nameserver: 10.84.5.100
      ntpserver: 192.168.121.169
      domainsuffix: local
   ```
5. Go to the  contrail-ansible-deployer directory and execute the command 

   ```
   ansible-playbook -i inventory/ playbooks/deploy.yml
   ```