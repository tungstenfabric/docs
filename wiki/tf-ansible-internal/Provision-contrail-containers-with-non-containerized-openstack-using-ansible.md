Notes:
* Ansible code to deploy openstack follows https://github.com/Juniper/contrail-ansible/wiki/Provision-contrail-with-existing-open-stack-using-ansible,fab,manual-steps

## Step 1: Setup requisites and inventory for contrail

Follow [Quickstart guide](https://github.com/Juniper/contrail-ansible/wiki/Quickstart-Guide-with-ini-file-based-inventory) to setup inventory 
Follow all steps until "Step 6: Run ansible" in above quickstart guide

## Step 2: Setup inventory file for openstack (inventory/my-inventory.ini)
* Uncomment and update [openstack-controllers]
```
##
# Only enable if you setup with openstack (when cloud_orchestrator is openstack)
##
;[openstack-controllers]
;192.168.0.23 ansible_user=root
```

* Uncomment and update openstack specific vars 
```

###################################################
# Openstack specific configuration
##
;contrail_install_packages_url=http://10.84.5.120/github-build/mainline/3023/ubuntu-14-04/mitaka/contrail-install-packages_4.0.0.0-3023~mitaka_all.deb
;keystone_config = {'ip': '192.168.0.23', 'admin_password': 'contrail123'}

```

## Step 3: Run ansible

```
$ cd contrail-ansible/playbooks
$ ansible-playbook -i inventory/my-inventory.ini site-openstack.yml
```