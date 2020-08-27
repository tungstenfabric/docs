Contrail-ansible can be used to provision Contrail-Kubernetes cluster.

This repo exposes a site.yml playbook that has the requisite roles and tasks to provision a fully functional Contrail-kubernetest cluster.

The inventory files in this repo expose all required knobs and levers required by the playbook to provision the cluster. We recommend directory based inventory file mechanism for provisioning.

NOTE: The scope of contrail-ansible will only be to provision contrail part of our Kubernetes solution. The Kubernetes cluster itself should be provisioned indepedently, as per guidelines laid out by the kubernetes project.

# __Contrail-Kubernetes cluster - Supported Modes__

There are two modes in which Contrail-Kubernetes solution can be provisioned:

*  **Bare-Metal Contrail-Kubernetes cluster**
   In this mode, Contrail provides networking to bare-metal Kubernetes cluster. Contrail components are provisioned and dedicated to the management of this cluster.

*  **Nested Contrail-Kubernetes cluster**
  In this mode, Contrail provides networking for a Kubernetes cluster that is provisioned on an Contail-Openstack cluster.
Contrail components are shared between the two clusters. Ansible will only provision Contrail components that directly interface with Kubernetes api server. All other Contrail components are shared between Openstack and Kubernetes clusters.
# __Prerequisites__

Please ensure that the following prerequisites are met, for a successful provisioning of Contrail-Kubernetes cluster.

1.   Installed and running Kubernetes cluster.

    A kubernetes cluster should be installed and available. 
    User is free to follow any installation method of their choice. 

2.   Kubernetes cluster should have atleast one worker Node.

    The Kubernetes cluster should consist of a Kubernetes master node and
    atleast one Kubernetes worker node. We do not support a tainted Kubernetes
    master i.e a mode where worker pods can be scheduled on kubernetes master node.
 
3.   Kubelet running on the Kubernetes master should NOT be configured with
    network plugin.
    
    Ensure that Kubelet running on the kubernetes master node is not run with
    network plugin options. If kubelet is running with network plugin option,
    then:

    a. disable/comment out the KUBELET_NETWORK_ARGS option in the configuration file:

       /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

    b. Restart kubelet service:

       systemctl daemon-reload; systemctl restart kubelet.service       

4.   Get a service account token that has cluster-admin cluster role.

    This token needs be configured in contrail-ansible during provisioning
    of the Contrail-Kubernetes cluster. Please refer to "kubernetes_access_token"
    variable in the all.yml in contrail-ansible.
    

    4.a Create a service account and bind it to "cluster-admin" cluster role using the command:
       kubectl create clusterrolebinding < role-binding-name > --clusterrole=cluster-admin --serviceaccount=< service-account-name >

       Optionally you could provide the cluster-admin role to an existing
       service account with the command.
```
       Example:
          Give an cluster-admin role to Service-account "default":

          kubectl create clusterrolebinding contrail-kube-manager --clusterrole=cluster-admin --serviceaccount=default:default
```

     4.b Get the secret associated with the service account using the command:
       kubectl describe sa < service-account-name >
```
       Example:
       > kubectl describe sa default
         Name:		default
         Namespace:	default
         Labels:	<none>
         Annotations:	<none>
         Tokens:            	default-token-r353k  <-----
         Image pull secrets:	<none>
         Mountable secrets: 	default-token-r353k
```      
    4.c Get the token associated with the secret, using the command:

        kubectl describe secret < name >
```
        Example:
        > kubectl describe secret default-token-r353k
        Name:		default-token-r353k
        Namespace:	default
        Labels:		<none>
        Annotations:	kubernetes.io/service-account.name=default
         		kubernetes.io/service-account.uid=4fbcc5cf-3fed-11e7-acf4-0271c93f63d6
        Type:	kubernetes.io/service-account-token
        Data
        ====
        ca.crt:		1025 bytes
        namespace:	7 bytes
        token:		          eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tcjM1M2siLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjRmYmNjNWNmLTNmZWQtMTFlNy1hY2Y0LTAyNzFjOTNmNjNkNiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.n_yp4ScFYNT7yvITtDYiHqGOSa3mm5xXxQWzojb_or-v7XrxpcMTU1zOIbLEOPBhOMc_iEOXO7TbVJCuCu8NwupUDeYtcCLimz8cjS0t3vKDGTcwU-G7_o7LWISqgdRPd_XFrFW0vXICVxUQJ2YsdDFat5N1bKxvs-u9eVFa1iwU-4vT5TPJXtpbeMggRdt3KRrkSJ9bC-sYRQt7y3x_9hbz4_SlpeS5PZHO9rqJ7ZPFmS7xK2xsO7TChPp5W2KocLo9QX5YgtfcuF9c58TsMhAmjcM-v5WcL5VbRWzoc3QNz2AnB_tpzmKX9MmacR3RclXZLZ1Mt6IpbfBuNb3yZg         
```

# __Provision a Contrail - Kubernetes cluster__

  The following ansible play will install Contrail-Kubernetes cluster.
  
  **ansible-playbook -i inventory/my-inventory site.yml**
   
  where:
*   inventory/my-inventory  is where the inventory files are located.

*   site.yml is the ansible play

# __Inventory Files__

  There are two inventory files in a directory based provisioning:
*   inventory/my-inventory/hosts

*   inventory/my-inventory/group_vars/all.yml

## __inventory/my-inventory/hosts__

Following are the knobs of interest:

```
Cluster-Mode: Both   --> Applicable to Bare-Metal and Nested clusters.
              Bare-Metal --> Applicable only to a Bare-Metal cluster.
              Nested --> Applicable only to Nested cluster.
```
| Knob | Cluster-Mode | Description |
| --- | --- | --- |
| contrail-repo | <sub>Nested</sub> | <sub> List of hosts where contrail apt or yum repo container will be started.This repo will be used by other nodes on installing any packages in the node. Setting up contrail-cni need this repo enabled</sub> |
| contrail-controllers | <sub>Bare-metal</sub> | <sub>List of hosts where contrail-controller container/processes are to be provisioned.</sub> |
| contrail-analyticsdb| <sub>Bare-metal</sub> | <sub>List of hosts where contrail-analyticsdb container/process is to be provisioned.</sub> |
| contrail-analytics| <sub>Bare-metal</sub> | <sub>List of hosts where contrail-analytics container/process is to be provisioned.</sub> |
| contrail-kubernetes| <sub>Both</sub> | <sub>Node where contrail-kube-manager container/process is to be run.</sub> |
| contrail-compute| <sub>Both</sub> | <sub>List of hosts which are to be provisioned as kubernetes compute/minion nodes. Contrail vrouter/vrouter-agent/CNI will be provisioned on these nodes.</sub> |
| kubernetes-contrail-controllers| <sub>Nested</sub> | <sub>List of nodes with pre-existing contrail-controller container/processes to which contrail-kube-manager should connect to.</sub> |
| kubernetes-contrail-analytics| <sub>Nested</sub> | <sub>List of nodes with pre-existing contrail-analytics container/processes to which contrail-kube-manager should connect to.</sub> |

### __Example inventory/my-inventory/hosts__

#### __Bare-Metal Contrail-Kubernetes cluster__
```
[contrail-controllers]
10.84.27.16

[contrail-analyticsdb]
10.84.27.16

[contrail-analytics]
10.84.27.16

[contrail-kubernetes]
10.84.27.16

[contrail-compute]
10.84.23.37

```
#### __Nested Contrail-Kubernetes cluster__

```
[contrail-repo]
10.84.31.71

[contrail-kubernetes]
10.84.31.71

[contrail-compute]
10.84.31.72

[kubernetes-contrail-controllers]
10.84.29.27

[kubernetes-contrail-analytics]
10.84.29.27

```

## __inventory/my-inventory/group_vars/all.yml__

In addition to other config and knobs in this file, the following are of interest for Contrail-kubernetes provisioning:

```
Cluster-Mode: Both        --> Applicable to Bare-metal and Nested cluster.
              Bare-Metal --> Applicable only to a  cluster.
              Nested      --> Applicable only to Nested cluster.
```
| Knob | Value | Default | Cluster-Mode | Description |
| --- | --- | --- | --- | --- |
| cloud_orchestrator | <sub>Kubernetes</sub> | <sub>None</sub> | <sub>Both</sub> | <sub>Specifies orchestrator type.</sub> |
| contrail_compute_mode | <sub>container/bare_metal</sub> | <sub>bare_metal</sub> | <sub>Both</sub> | <sub>Specifies if the contrail components should be run as containers or as processes on a bare metal server </sub>|
| keystone_config | <sub>{ip: < ip >, admin_password: < passwd >, admin_user: < username >, admin_tenant: < tenant-name >}</sub> | <sub>None</sub> | <sub>Nested</sub> |  <sub>Keystone authentication info.</sub> |
| nested_cluster_private_network | <sub>"< cluster-private-CIDR >"</sub> | <sub>None</sub> | <sub>Nested</sub> | <sub>The IP subnet reserved for use by kubernetes for internal cluster management and housekeeping. The user of ansible is responsible to make sure this CIDR does not collide with existing CIDR's in the virtual-network.</sub>|
| kubernetes_cluster_name | < cluster-name > | <sub>k8s-default</sub> | <sub>Both</sub> | <sub>Name of the kubernetes cluster being provisioned.</sub>|
| nested_cluster_network | <sub>{domain: < name >, project: < name >, name: < name >}</sub> | <sub>None</sub> | <sub>Nested</sub> | <sub>Virtual Network in which the Kubernetes cluster should be provisioned. This network SHOULD be the network to which the virtual machines's, that hosts the kubernetes cluster, belong to.</sub>|
| kubernetes_access_token | <sub>< token ></sub> | <sub> None </sub> | <sub> Both </sub> | <sub> RBAC token to connect to Kuberenetes API server. </sub>|
| nested_mode | <sub>true</sub> | <sub>None</sub> | <sub>Nested</sub> | <sub> Knob to enable nested provisioning of a kubernetes cluster. </sub>|
| kubernetes_public_fip_pool | <sub>{domain: <>, project: <>, network: <>, name: <>}</sub> | <sub>None</sub> | <sub>Both</sub> | <sub>Kubernetes FloatingIpPool to be used for service/ingress.</sub>|
| kubernetes_cluster_project | <sub>{domain: <>, project: <>}</sub>|<sub>{domain: default-domain, project: default}</sub>| <sub>Both</sub> | <sub>Fq-name of Contrail project within with this kubernetes cluster should be provisioned.</sub>|
| kubernetes_pod_subnet | <sub>< CIDR ></sub> | <sub> 10.32.0.0/12 </sub> | <sub>Both</sub> | <sub>Pod subnet to be used by kubernetes cluster.</sub>|
| kubernetes_service_subnet | <sub>< CIDR ></sub> | <sub> 10.96.0.0/12 </sub> | <sub>Both</sub> | <sub>Service subnet to be used by kubernetes cluster.</sub>|
| kubernetes_api_server | <sub>< IP ></sub> | <sub> Contrail Control Node IP </sub> | <sub>Both</sub> | <sub>Node where kubernetes-api server is running.</sub>|

### __Example inventory/my-inventory/group_vars/all.yml__

#### __Bare-Metal Contrail-Kubernetes cluster__
```
docker_registry: 10.84.34.155:5000
docker_registry_insecure: True
docker_install_method: package
docker_py_pkg_install_method: pip

# ansible connection details
ansible_user: root
ansible_become: true
ansible_ssh_private_key_file: ~/.ssh/id_rsa

contrail_compute_mode: container

os_release: ubuntu14.04

# contrail version
contrail_version: 4.0.0.0-3058

cloud_orchestrator: kubernetes

# vrouter physical interface
vrouter_physical_interface: enp6s0f0

# global_config:

# To configure custom webui http port
webui_config: {http_listen_port: 8085}

# Name of the kubernetes cluster being provisioned.
kubernetes_cluster_name: k8s5

# Access token to connect to Kuberenetes API server.
kubernetes_access_token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tcTUzYmYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImVhNzE1YjJkLTJhYWUtMTFlNy1iZmJmLTAyMWQwOTNhMzRkMSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.Kj0-NYBopRc8rMsX4NnKpJa570k2iamPOgCTdj3d93MW20girt4IgdAmR4v4kifQO-h5eYGVlfA3ftkPuWb5GbHDz9x7BoYc7b759i2cuX3AmtbCl5kNcbGY7_7JPIDkMHwwRj7FK7Y57eEFTstCxcpR4itqxzsRi7jc0nrrcbDkvlOkDhA93ID4ChPwE2PcsAf_LV9ds-gSzuyPIQt0qdxnQvI262AjgeNowbQhkYguoqZWJIE--AwpgSE0NiNpjcxiUx1HC2uaRSP3g9mMr2g4YQHRjxJwuz3fUkaSRNZyQEpyE5G5WKXTefc7h52R5Kphn2nT9gg6x175mrrnNQ

# Kubernetes API server IP.
kubernetes_api_server: 10.84.27.16

```
#### __Nested Contrail-Kubernetes cluster__

```
docker_registry: 10.84.34.155:5000
docker_registry_insecure: True
docker_install_method: package
docker_py_pkg_install_method: pip

# ansible connection details
ansible_user: root
ansible_become: true
ansible_ssh_private_key_file: ~/.ssh/id_rsa

contrail_compute_mode: container

os_release: ubuntu14.04

# contrail version
contrail_version: 4.0.0.0-3058

cloud_orchestrator: kubernetes

# vrouter physical interface
vrouter_physical_interface: enp6s0f0

# global_config:

# To configure custom webui http port
webui_config: {http_listen_port: 8085}

keystone_config: {ip: 10.84.29.27, admin_password: c0ntrail123, admin_user: admin, admin_tenant: admin}

###################################################
# Kubernetes cluster configuration
##

# The IP subnet reserved for use by kubernetes for internal cluster management
# and housekeeping.
nested_cluster_private_network: "10.10.10.0/24"

# Name of the kubernetes cluster being provisioned.
kubernetes_cluster_name: k8s5

# Virtual Network in which the Kubernetes cluster should be provisioned.
nested_cluster_network: {domain: default-domain, project: admin, name: 5-k8s-VM-network}

# Access token to connect to Kuberenetes API server.
kubernetes_access_token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tcTUzYmYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImVhNzE1YjJkLTJhYWUtMTFlNy1iZmJmLTAyMWQwOTNhMzRkMSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.Kj0-NYBopRc8rMsX4NnKpJa570k2iamPOgCTdj3d93MW20girt4IgdAmR4v4kifQO-h5eYGVlfA3ftkPuWb5GbHDz9x7BoYc7b759i2cuX3AmtbCl5kNcbGY7_7JPIDkMHwwRj7FK7Y57eEFTstCxcpR4itqxzsRi7jc0nrrcbDkvlOkDhA93ID4ChPwE2PcsAf_LV9ds-gSzuyPIQt0qdxnQvI262AjgeNowbQhkYguoqZWJIE--AwpgSE0NiNpjcxiUx1HC2uaRSP3g9mMr2g4YQHRjxJwuz3fUkaSRNZyQEpyE5G5WKXTefc7h52R5Kphn2nT9gg6x175mrrnNQ

# Kubernetes cluster is nested within an Openstack cluster.
nested_mode: true

# Kubernetes API server IP.
kubernetes_api_server: 10.84.27.16

```

# __FAQ's__

* **Can Contrail Kubernetes manager connect to Kubernetes master running on another node ?**

  **Should Contrail kubernetes manager run in the same node as the Kubernetes master ?**

  NO. Contrail Kubernetes manager can connect to Kubernertes master running on any node, locally or remote.
  IP address of the Kubernetes master node should be configured in inventory/myinvetory/groups/all.yml file using the variable/knob: **kubernetes_api_server**.
  If this knob is not configured, then by default, Kubernetes master is assumed to run in the same node as Contrail Kubernetes manager.
  ```
  Example
  File: inventory/myinvetory/groups/all.yml
  
  kubernetes_api_server: 192.168.0.22
  ```
  
# __Provision a Contrail - Kubernetes cluster Using Kubernetes Single YAML file__

## __Nested Mode__

### Step 1

Start required number of Virtual Machines running Centos 7.x/Ubuntu 16.04.2 OS. These virtual machines are the nodes of your kubernetes cluster.

### Step 2

Install Kubernetes cluster on the virtual machines. 
NOTE: Remember to disable CNI on the Kubernetes master node.

At the end of installation, you will have a setup where the kubernetes master is in Ready state and all kubernetes compute nodes are in NotReady state.

```
[root@k8s-5-c-1 ~]# kubectl get nodes
NAME        STATUS     AGE       VERSION
k8s-5-c-1   Ready      1m        v1.7.3
k8s-5-c-2   NotReady   1s        v1.7.3
```

### Step 3
Load and tag contrail-kube-manager-ubuntu.xxxx.tar.gz image onto the docker repo on the master kubernetes node.
#### Step 3.1 Load contrail-kube-manager image using command:  docker load -i < image-file-name >
```
 docker load -i contrail-kube-manager-ubuntu14.04-4.0.0.0-20.tar.gz 
```
#### Step 3.2 Tag contrail-kube-manager image using command:  docker tag < image-id > < tag-name >
```
docker tag 0d6e917c6634 10.84.5.71:5000/contrail-kube-manager-ubuntu14.04:4.0.0.0-20

0d6e917c6634 <-- Docker image id
10.84.5.71:5000/contrail-kube-manager-ubuntu14.04:4.0.0.0-20 <-- Preferred tag for the docker image.
```
### Step 4
Load and tag contrail-kubernetes-agent-xxxx.tar.gz image onto the docker repo on ALL kubernetes compute nodes.
#### Step 3.1 Load contrail-kubernetes-agent image using command:  docker load -i < image-file-name >
```
 docker load -i contrail-kubernetes-agent-ubuntu14.04-4.0.0.0-20.tar.gz 
```
#### Step 3.2 Tag contrail-kubernetes-agent image using command:  docker tag < image-id > < tag-name >
```
docker tag 3c2cdfe92c60 10.84.5.71:5000/contrail-kubernetes-agent-ubuntu14.04:4.0.0.0-20

3c2cdfe92c60 <-- Docker image id
10.84.5.71:5000/contrail-kubernetes-agent-ubuntu14.04:4.0.0.0-20 <-- Preferred tag for the docker image.
```
### Step 5
Configure Link-local services for Contrail Services.

A nested kubernetes cluster is managed by the same contrail control processes that manage the underlying openstack cluster. Towards this goal, the nested kubernetes cluster needs ip reachability to the contrail control processes. Since the kubernetes cluster is actually an overlay on the openstack cluster, we use Link Local Service feature of Contrail to provide ip reachability to/from the overly kubernetes cluster and openstack cluster.

To configure a Link Local Service, we need a Service IP and Fabric IP. Fabric IP is the node IP on which the contrail processes are running on. Service IP(along with port number) is used by data plane to identify the fabric ip/node. Service IP is required to be a unique and unused IP in the entire openstack cluster. **For each node of the openstack cluster, one service IP should be identified.**

NOTE: The user is responsible to configure these Link Local Services via Contrail GUI.

The following are the Link Local Services are required:

| Contrail Process | Service IP  | Service Port | Fabric IP | Fabric Port |
| --- | --- | --- | --- | --- |
| Contrail Config     | < Service IP for the running node > | 8082 | < Node IP of running node > | 8082 |
| Contrail Analytics  | < Service IP for the running node > | 8086 | < Node IP of running node > | 8086 |
| Contrail Msg Queue  | < Service IP for the running node > | 5672 | < Node IP of running node > | 5672 |
| Contrail VNC DB     | < Service IP for the running node > | 9161 | < Node IP of running node > | 9161 |
| Keystone            | < Service IP for the running node > | 35357 | < Node IP of running node > | 35357 |
| VRouter             | < Service IP for the running node > | 9091 | 127.0.0.1 | 9091 |

####Example:

Lets assume the following hypothetical Openstack Cluster where:
```
Contrail Config : 192.168.1.100
Contrail Analytics : 192.168.1.100, 192.168.1.101
Contrail Msg Queue : 192.168.1.100
Contrail VNC DB : 192.168.1.100, 192.168.1.101, 192.168.1.102
Keystone: 192.168.1.200
Vrouter: 192.168.1.300, 192.168.1.400, 192.168.1.500
```
This cluster is made of 7 node. We will allocate 7 unused IP's for these nodes:
```
192.168.1.100  --> 10.10.10.1
192.168.1.101  --> 10.10.10.2
192.168.1.102  --> 10.10.10.3
192.168.1.200  --> 10.10.10.4
192.168.1.300  --> 10.10.10.5
192.168.1.400  --> 10.10.10.6
192.168.1.500  --> 10.10.10.7
```
The following link-local services will be created:

| LL Service Name | Service IP  | Service Port | Fabric IP | Fabric Port |
| --- | --- | --- | --- | --- |
| Contrail Config      | 10.10.10.1 | 8082 | 192.168.1.100 | 8082 |
| Contrail Analytics 1 | 10.10.10.1 | 8086 | 192.168.1.100 | 8086 |
| Contrail Analytics 2 | 10.10.10.2 | 8086 | 192.168.1.101 | 8086 |
| Contrail Msg Queue   | 10.10.10.1 | 5672 | 192.168.1.100 | 5672 |
| Contrail VNC DB 1    | 10.10.10.1 | 9161 | 192.168.1.100 | 9161 |
| Contrail VNC DB 2    | 10.10.10.2 | 9161 | 192.168.1.101 | 9161 |
| Contrail VNC DB 3    | 10.10.10.3 | 9161 | 192.168.1.102 | 9161 |
| Keystone             | 10.10.10.4 | 35357 | 192.168.1.200| 35357 |
| VRouter-192.168.1.300 | 10.10.10.5 | 9091 | 127.0.0.1 | 9091 |
| VRouter-192.168.1.400 | 10.10.10.6 | 9091 | 127.0.0.1 | 9091 |
| VRouter-192.168.1.500 | 10.10.10.7 | 9091 | 127.0.0.1 | 9091 |

### Step 6
Create the Contrail-Kubernetes cluster.

Copy over the yaml file to the kubernetes master node and invoke "kubectl create" on it.

The yaml files can be downloaded here:
https://github.com/Juniper/contrail-docker/tree/master/kubernetes/manifests

There are two flavors of yaml files:
```
contrail-host-cantos-nested.yml  <--- If the Kubernetes cluster is running on Centos
contrail-host-ubuntu-nested.yml  <--- If the Kubernetes cluster is running on Ubuntu
```
Modify the image name of contrail-kube-manager and contrail-kubernetes-agent containers in the yml file to the reflect the respective tags specified in Step 3 and Step 4.

### Step 7
Instantiate the Contrail-kubernetes cluster with the following command:
```
kubectl create -f < xxx.yaml >

Example: kubectl create -f contrail-host-centos-nested.yml 
```

When contrail-kube-manager and contrail-kubernetes-agent pods transition to "Running" state, the cluster is ready.
```
[root@k8s-5-c-1 ~]# kubectl get pods -n kube-system
NAME                                READY     STATUS    RESTARTS   AGE
contrail-kube-manager-pghh9         1/1       Running   0          23s
contrail-kubernetes-agent-c7zrv     1/1       Running   0          23s
etcd-k8s-5-c-1                      1/1       Running   2          13m
kube-apiserver-k8s-5-c-1            1/1       Running   0          13m
kube-controller-manager-k8s-5-c-1   1/1       Running   3          13m
kube-dns-2425271678-lkd9n           3/3       Running   0          14m
kube-proxy-bbsc4                    1/1       Running   0          14m
kube-proxy-n7pcs                    1/1       Running   0          13m
kube-scheduler-k8s-5-c-1            1/1       Running   3          13m
```
