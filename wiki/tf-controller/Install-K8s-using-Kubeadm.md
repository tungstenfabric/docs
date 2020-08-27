# Installing Kubernetes on Master node

**(Centos 7.4 - 3.10.0-862.3.2 kernel)**

1. Prepare the node by running the following pre-requisites
```
sudo setenforce 0
swapoff -a
```
2. Install Docker
```
sudo yum install -y docker
systemctl enable docker.service;service docker start

```
3. Add Kubernetes repo 
```
cat << EOF >> /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
        https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

```
4. Install Kubernetes components
```
yum update -y; yum install -y kubelet kubeadm
```
5. Disable networking on Master
```
sudo vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

Comment out "#Environment="KUBELET_NETWORK_ARGS=--network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin"
sudo systemctl daemon-reload;sudo service kubelet restart
```
6. Restart kubelet service
```
systemctl enable kubelet && systemctl start kubelet
```
7. Disable firewalld
```
sysctl -w net.bridge.bridge-nf-call-iptables=1
systemctl stop firewalld; systemctl disable firewalld
```
8. Create K8s cluster
```
kubeadm init
```
9. Once "kubeadm init" completes, save the "join" command that will be printed on the shell, to a file of your choice. This will be needed to add new nodes to your cluster.

```
example:
"kubeadm join 192.168.1.3:6443 --token 0smq4g.7pmg2jqc8arl1uz7 --discovery-token-ca-cert-hash sha256:d92ac0785b1435666d726f4bc54fde58693f87cf91371d9fd553da4a40813650"
```
10. Run the following commands to initially kubernetes command line
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

# Installing Kubernetes on all your Compute node/s
**(Centos 7.4 - 3.10.0-862.3.2 kernel)**

1. Prepare the node by running the following pre-requisites
```
sudo setenforce 0
swapoff -a
```
2. Install Docker
```
sudo yum install -y docker
systemctl enable docker.service;service docker start

```
3. Add Kubernetes repo 
```
cat << EOF >> /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
        https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

```
4. Install Kubernetes components
```
yum update -y; yum install -y kubelet kubeadm
```
5. Disable firewalld
```
sysctl -w net.bridge.bridge-nf-call-iptables=1
systemctl stop firewalld; systemctl disable firewalld
```
6. Join the Master node
Copy paste the "join" command you saved from Step-9 of instructions for installation of K8s on master.
```
"kubeadm join 192.168.1.3:6443 --token 0smq4g.7pmg2jqc8arl1uz7 --discovery-token-ca-cert-hash sha256:d92ac0785b1435666d726f4bc54fde58693f87cf91371d9fd553da4a40813650"

```