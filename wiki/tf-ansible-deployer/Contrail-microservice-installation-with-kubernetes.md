* Re-image node to centos 7.5 :
``` 
/cs-shared/server-manager/client/server-manager reimage --server_id <Server ID> centos-7.5
```

* Install required/useful tools


```
yum install -y python-pip
pip install requests
yum -y install epel-release git ansible net-tools
```

* Clone contrail-ansible-deployer repo
```
git clone https://github.com/Juniper/contrail-ansible-deployer.git
cd contrail-ansible-deployer
```

* Edit config/instances.yaml and fill in appropriate values.
  Here is a sample file for 2 node kubernetes install.

```
Sample config/instances.yaml

global_configuration:
  CONTAINER_REGISTRY: opencontrailnightly
provider_config:
  bms:
   ssh_pwd: <Password>
   ssh_user: root
   ssh_public_key: /root/.ssh/id_rsa.pub
   ssh_private_key: /root/.ssh/id_rsa
   domainsuffix: local
instances:
  <Server 1 Hostname>:
   provider: bms
   roles:            # Optional.  If roles is not defined, all below roles will be created
      config_database:         # Optional.
      config:                  # Optional.
      control:                 # Optional.
      analytics_database:      # Optional.
      analytics:               # Optional.
      webui:                   # Optional.
      k8s_master:              # Optional.
      kubemanager:             # Optional.
   ip: <BMS1 IP>
  <Server 2 Hostname>:
   provider: bms
   roles:            # Optional.  If roles is not defined, all below roles will be created
     vrouter:        # Optional.
     k8s_node:       # Optional.
   ip: <BMS2 IP>
contrail_configuration:
  CONTAINER_REGISTRY: opencontrailnightly
  CONTRAIL_VERSION: latest
  KUBERNETES_CLUSTER_PROJECT: {}
```

* Run Configure
```
ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/configure_instances.yml
```

* Run Install
```
ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/install_k8s.yml
ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/install_contrail.yml
```