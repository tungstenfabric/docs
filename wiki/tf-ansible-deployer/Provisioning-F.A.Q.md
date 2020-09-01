#### 1. Couldn't find kolla's file/directory:
```
[root@a6s14 contrail-ansible-deployer]# ansible-playbook -i inventory/ -e orchestrator=vcenter  playbooks/install_openstack.yml
...
...
ERROR! Unable to retrieve file contents
Could not find or access '/root/contrail-kolla-ansible/ansible/kolla-host.yml'
[root@a6s14 contrail-ansible-deployer]# 
```

**Resolution:** Please run the command below first before running the install_contrail play
```
ansible-playbook -i inventory/ playbooks/configure_instances.yml
```


#### 2. Absence of ipv4 in ansible's fact:
```
TASK [memcached : Copying over config.json files for services] *******************************************************************************************************************************
task path: /root/contrail-kolla-ansible/ansible/roles/memcached/tasks/config.yml:10
failed: [192.168.122.84] (item=memcached) => {
   "changed": false,
   "item": "memcached",
   "msg": "AnsibleUndefinedVariable: {{ hostvars[inventory_hostname]['ansible_' + api_interface]['ipv4']['address'] if orchestration_engine == 'ANSIBLE' else '0.0.0.0' }}: 'dict object' has no attribute 'ipv4'"
}
```

**Resolution:** Check if you have specified the right values for "network_interface" under "kolla_globals" section in your instances.yaml file. This interface must have an IP address.


#### 3. How to specify host specific parameters (for example, the interface names are different for the different servers in the cluster)?

**Resolution:** Check [the example here](https://github.com/Juniper/contrail-ansible-deployer/wiki/Configuration-Sample-for-Multi-Node-Openstack-HA-and-Contrail-(multi-interface)).


#### 4. Containers are not accessible (pulled) from private registry given as "CONTAINER_REGISTRY".

**Resolution:** Check that "REGISTRY_PRIVATE_INSECURE" is set to True. Example here:
[Sample instances.yaml](https://github.com/Juniper/contrail-ansible-deployer/wiki/Contrail-with-Kolla-Ocata#13-configure-necessary-parameters-configinstancesyaml-under-appropriate-parameters)


#### 5. vrouter module is not getting installed on the computes. vrouter container in error state and docker logs show the error like this: 

```
[srvr5] ~ # docker logs vrouter_vrouter-kernel-init_1
insmod: ERROR: could not insert module /opt/contrail/vrouter-kernel-modules/???/vrouter.ko: Unknown symbol in module
ERROR: Failed to insert vrouter kernel module
```

or logs in dmesg like this:

```
[161758.854712] entrypoint.sh (19521): drop_caches: 2
[161758.861953] vrouter: Unknown symbol __x86_indirect_thunk_r15 (err 0)
[161758.862025] vrouter: Unknown symbol __x86_indirect_thunk_r11 (err 0)
[161758.862043] vrouter: Unknown symbol __x86_indirect_thunk_rax (err 0)
[161758.862047] vrouter: disagrees about version of symbol napi_complete_done
[161758.862049] vrouter: Unknown symbol napi_complete_done (err -22)
[161758.862113] vrouter: Unknown symbol __x86_indirect_thunk_rdx (err 0)
[161758.862158] vrouter: Unknown symbol __x86_indirect_thunk_r14 (err 0)
[161758.862203] vrouter: Unknown symbol __x86_indirect_thunk_r13 (err 0)
[161758.862216] vrouter: disagrees about version of symbol __ethtool_get_link_ksettings
[161758.862218] vrouter: Unknown symbol __ethtool_get_link_ksettings (err -22)
[161758.862240] vrouter: Unknown symbol __x86_indirect_thunk_r10 (err 0)
[161758.862287] vrouter: Unknown symbol ether_setup_rh (err 0)
[161758.862306] vrouter: Unknown symbol __x86_indirect_thunk_rcx (err 0)
[161758.862327] vrouter: Unknown symbol __x86_indirect_thunk_r9 (err 0)
[161758.862358] vrouter: Unknown symbol __x86_indirect_thunk_r12 (err 0)
[161758.862381] vrouter: Unknown symbol napi_schedule_prep (err 0)
[161758.862444] vrouter: Unknown symbol genl_register_family (err 0)
[161758.862467] vrouter: Unknown symbol __x86_indirect_thunk_r8 (err 0)
```

**Resolution:** The vrouter module is now dependent on the host kernel being 3.10.0-862.3.2.el7.x86_64. Install this kernel version on the target nodes before running provision:

```
yum -y install kernel-3.10.0-862.3.2.el7.x86_64                                                                                                                                                    
yum update
reboot
```

Also you can just update to latest kernel - it should work. And one more option is to let contrail-ansible-deployer update your kernel:

```
contrail_configuration:
    UPGRADE_KERNEL: true
```


#### 6. Error retrieving container images: 

```
fatal: [10.87.70.19]: FAILED! => {“changed”: true, “msg”: “’Traceback (most recent call last):
File   \“/tmp/ansible_x7Zn20/ansible_module_kolla_docker.py\“, line 785, in main\\n    
result = bool(getattr(dw,  module.params.get(\\‘action\\‘))())\\n  
File \“/tmp/ansible_x7Zn20/ansible_module_kolla_docker.py\“, line 583, in recreate_or_restart_container\\n
self.start_container()\\n  File \“/tmp/ansible_x7Zn20/ansible_module_kolla_docker.py\“, line 595, in start_container\\n
self.pull_image()\\n  File \“/tmp/ansible_x7Zn20/ansible_module_kolla_docker.py\“, line 445, in pull_image\\n    
repository=image, tag=tag, stream=True\\n
File \“/usr/lib/python2.7/site-packages/docker/api/image.py\“, line 175, in pull\\n
self._raise_for_status(response)\\n  File \“/usr/lib/python2.7/site-packages/docker/client.py\“, line 173, in _raise_for_status\\n
raise errors.NotFound(e, response, explanation=explanation)\\nNotFound: 404 Client Error: Not Found (\“{\“message\“:\“manifest for opencontrailnightly/contrail-openstack-ironic-notification-manager:master-centos7-ocata-bld-33 not found\“}\“)\\n’“}
 to retry, use: --limit @/root/contrail-ansible-deployer/playbooks/install_contrail.retry
```

**Resolution:** Check CONTRAIL_VERSION. It should have a valid tag that is found here: [opencontrailnightly tags](https://hub.docker.com/r/opencontrailnightly/contrail-nodemgr/tags/)


#### 7. Seeing this error: 

```
2018-03-21 00:47:16,884 p=16999 u=root |  TASK [iscsi : Ensuring config directories exist] *********************************************************************************************************************************

2018-03-21 00:47:16,959 p=16999 u=root |  fatal: [10.0.0.4]: FAILED! => {"msg": "The conditional check 'inventory_hostname in groups['compute'] or inventory_hostname in groups['storage']' failed. The error was: error while evaluating conditional (inventory_hostname in groups['compute'] or inventory_hostname in groups['storage']): Unable to look up a name or access an attribute in template string ({% if inventory_hostname in groups['compute'] or inventory_hostname in groups['storage'] %} True {% else %} False {% endif %}).\nMake sure your variable name does not contain invalid characters like '-': argument of type 'StrictUndefined' is not iterable\n\nThe error appears to have been in '/root/contrail-kolla-ansible/ansible/roles/iscsi/tasks/config.yml': line 2, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n---\n- name: Ensuring config directories exist\n  ^ here\n"}

2018-03-21 00:47:16,961 p=16999 u=root |        to retry, use: --limit @/root/contrail-ansible-deployer/playbooks/install_contrail.retry
```

**Resolution:**: This is a result of the recent change done via [Bug #1756133](https://review.opencontrail.org/#/c/40680/) There is a use-case where vrouter needs to be provisioned without being accompanied by nova-compute. So the "openstack_compute" is not automatically inferred when "vrouter" role is specified. The "openstack_compute" role needs to be explicitly stated along with "vrouter" 


#### 8. Why do I need haproxy and virtual IP on a single openstack cluster?

By default all openstack services will listen on the IP/interface provided by kolla_internal_vip_address/network_interface variables under the "kolla_globals" section. This will in most cases correspond to the ctrl-data network. Note that this will mean even horizon will now only run on ctrl-data network only. The only way kolla provides access to horizon on the management network is by using haproxy and keepalived. Enabling keepalived in turn means that a virtual IP is required for VRRP which cannot be the interface IP itself. There is no way to enable haproxy without enabling keepalived using kolla configuration parameters. This is the reason you need to provide two virtual IP address one on management (kolla_external_vip_address) and one on ctrl-data-network (kolla_internal_vip_address). Once this is given, horizon will be accessible on the management network via the kolla_external_vip_address.


#### 9. How to use the kolla_toolbox container to run openstack CLI commands

The /etc/kolla/kolla-toolbox directory of the base host on which openstack containers are running is mounted and accessible as /var/lib/kolla/config_files from inside the kolla_toolbox container. In case the user needs other files when executing openstack commands (for example 'openstack image create' will need image file), then the user can copy the relevant files into the /etc/kolla/kolla-toolbox directory of the base host and then use them inside the container. The way to run openstack commands is as follows:

```
# ON BASE HOST OF OPENSTACK CONTROL NODE
cd /etc/kolla/kolla-toolbox
wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img

docker exec -it kolla_toolbox bash
# NOW YOU ARE INSIDE THE KOLLA_TOOLBOX CONTAINER
(kolla-toolbox)[ansible@server1 /]$ source /var/lib/kolla/config_files/admin-openrc.sh
(kolla-toolbox)[ansible@server1 /]$ cd /var/lib/kolla/config_files
(kolla-toolbox)[ansible@server1 /var/lib/kolla/config_files]$ openstack image create cirros2 --disk-format qcow2 --public --container-format bare --file cirros-0.4.0-x86_64-disk.img
+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| checksum         | 443b7623e27ecf03dc9e01ee93f67afe                     |
| container_format | bare                                                 |
| created_at       | 2018-03-29T21:37:48Z                                 |
| disk_format      | qcow2                                                |
| file             | /v2/images/e672b536-0796-47b3-83a6-df48a5d074be/file |
| id               | e672b536-0796-47b3-83a6-df48a5d074be                 |
| min_disk         | 0                                                    |
| min_ram          | 0                                                    |
| name             | cirros2                                              |
| owner            | 371bdb766278484bbabf868cf7325d4c                     |
| protected        | False                                                |
| schema           | /v2/schemas/image                                    |
| size             | 12716032                                             |
| status           | active                                               |
| tags             |                                                      |
| updated_at       | 2018-03-29T21:37:50Z                                 |
| virtual_size     | None                                                 |
| visibility       | public                                               |
+------------------+------------------------------------------------------+
(kolla-toolbox)[ansible@server1 /var/lib/kolla/config_files]$ openstack image list
+--------------------------------------+---------+--------+
| ID                                   | Name    | Status |
+--------------------------------------+---------+--------+
| e672b536-0796-47b3-83a6-df48a5d074be | cirros2 | active |
| 57e6620e-796a-40ee-ae6e-ea1daa253b6c | cirros2 | active |
+--------------------------------------+---------+--------+
```


#### 10. Failure to deploy redis with the following error:

```
The conditional check 'roles[instance_name].webui is defined or roles[instance_name].analytics is defined' failed.

}
2018-04-21 15:27:24,288 p=23225 u=root | Read vars_file '{{ hostvars['localhost'].config_file }}'
2018-04-21 15:27:24,289 p=23225 u=root | TASK [install_contrail : create /etc/contrail/redis] *******************************************************************************************************************************************************************
2018-04-21 15:27:24,289 p=23225 u=root | task path: /var/contrail-ansible-deployer/playbooks/roles/install_contrail/tasks/create_redis.yml:2
2018-04-21 15:27:24,379 p=23225 u=root | Read vars_file '{{ hostvars['localhost'].config_file }}'
2018-04-21 15:27:24,391 p=23225 u=root | fatal: [10.87.129.234]: FAILED! => {
    "msg": "The conditional check 'roles[instance_name].webui is defined or roles[instance_name].analytics is defined' failed. The error was: error while evaluating conditional (roles[instance_name].webui is defined or roles[instance_name].analytics is defined): 'dict object' has no attribute u'bms2'\n\nThe error appears to have been in '/var/contrail-ansible-deployer/playbooks/roles/install_contrail/tasks/create_redis.yml': line 2, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n---\n- name: create /etc/contrail/redis\n ^ here\n"
}
2018-04-21 15:27:24,491 p=23225 u=root | Read vars_file '{{ hostvars['localhost'].config_file }}'
2018-04-21 15:27:24,498 p=23225 u=root | fatal: [10.87.140.154]: FAILED! => {
    "msg": "The conditional check 'roles[instance_name].webui is defined or roles[instance_name].analytics is defined' failed. The error was: error while evaluating conditional (roles[instance_name].webui is defined or roles[instance_name].analytics is defined): 'dict object' has no attribute u'bms3'\n\nThe error appears to have been in '/var/contrail-ansible-deployer/playbooks/roles/install_contrail/tasks/create_redis.yml': line 2, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n---\n- name: create /etc/contrail/redis\n ^ here\n"
}
```

*Resolution*: This is caused by code incompatible with 2.5.1.0 version of Ansible. Please stick to ansible-2.4.2.0 to avoid this issue for now until we fix the code to work with the latest version of Ansible.


#### 11. Observing Cassandra's state like 'Disk for DB is too low.':

- increase disk to more than 256Gb
- set another threshold value:

```
contrail_configuration:
    CONFIG_DATABASE_NODEMGR__DEFAULTS__minimum_diskGB: "2"
    DATABASE_NODEMGR__DEFAULTS__minimum_diskGB: "2"
``` 

For 5.0.0 release you need to specify CONFIG_NODEMGR__DEFAULTS__minimum_diskGB instead of CONFIG_DTABASE_NODEMGR__DEFAULTS__minimum_diskGB


#### 12. VM for controller has 16Gb or less (demo version). Setup is not stable. All memory is consumed by several Java apps:
#### Or
#### Error response from daemon: grpc: the connection is unavailable


**Reason:** Java memory can be limited with next statement in configuration.

**Resolution:** Add the below configuration to the instances.yaml file.

```
contrail_configuration:
    JVM_EXTRA_OPTS: "-Xms1g -Xmx2g"
``` 

Also this statement can be applied only to configdb role or different memory options can be applied to configdb and analyticsdb roles in instances definition.


#### 13. libvirt container couldn't be started:

```
------------------------------------------------------------------------------
+ ./tools/deployment/common/wait-for-pods.sh openstack
containers failed to start.
NAME                                  READY     STATUS             RESTARTS   AGE       IP            NODE
...
libvirt-8dhtx                         0/1       CrashLoopBackOff   13         43m       172.17.0.1    ubuntu-2
nova-compute-default-z8qvb            0/1       CrashLoopBackOff   4          15m       172.17.0.1    ubuntu-2
...
------------------------------------------------------------------------------
```

**Reason:** Libvirt is started by default on many operating systems. Only one copy of libvirt may be running at a time.

**Resolution:** Please check if libvirtd present on the host. Remove/Disable the libvirtd if it is running on any machines that will be deployment targets. More than one instance of libvirtd is not supported.

How to disable it:
 * service libvirt-bin stop
 * update-rc.d libvirt-bin disable

On Ubuntu, apparmor will sometimes prevent libvirtd from working, with error **/usr/sbin/libvirtd: error while loading shared libraries: libvirt-admin.so.0: cannot open shared object file: Permission denied**. To fix, execute the below command.
 * sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.libvirtd 

Or just remove it with host's package manager

Reference: [link](https://bugs.launchpad.net/kolla/+bug/1687459/comments/2)

#### 14. Error due to "requests" package not found:

Reference: [Bug filed](https://bugs.launchpad.net/juniperopenstack/+bug/1803809)
Workaround (on the deployer node):

```
yum -y install python-pip                                                                                                                                
pip install requests
```

Till this is fixed as part of containerized solution/pre install