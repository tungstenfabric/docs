Provisioning of Kubernetes Clusters
===================================

:date: 2020-10-21

Tungsten Fabric supports the following ways of provisioning
Kubernetes clusters:

Provisioning of a Standalone Kubernetes Cluster
-----------------------------------------------

You can provision a standalone Kubernetes cluster using
contrail-ansible-deployer.

Perform the following steps to install one Kubernetes cluster and one
TF cluster and integrate them together.

1. See :ref:`Supported Platforms for Tungsten Fabric
   Release <ServerReqAndPlatform>`
   for a list of supported platforms.

2. Install the necessary tools.

   ``yum -y install epel-release git ansible net-tools``

3. Download the ``contrail-ansible-deployer-19<xx>.<NN>.tgz`` Ansible
   Deployer application tool package onto your provisioning host from
   `Contrail
   Downloads <https://www.juniper.net/support/downloads/?p=contrail#sw>`__
   page and extract the package.

   ``- tar xvf contrail-ansible-deployer-19<xx>.<NN>.tgz``

4. Navigate to the ``contrail-ansible-deployer`` directory.

   ``cd contrail-ansible-deployer``

5. Edit the ``config/instances.yaml`` and enter the necessary values.


6. Turn off the swap functionality on all nodes.

   ``swapoff -a``

7. Configure the nodes.

   ``ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/configure_instances.yml``

8. Install Kubernetes and TF.

   ``ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/install_k8s.yml``

   ``ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/install_contrail.yml``

9. Turn on the swap functionality on all nodes.

   ``swapon -a``

Provisioning of Nested TF Kubernetes Clusters
---------------------------------------------------

When TF provides networking for a Kubernetes cluster that is
provisioned on the workloads of a TF-OpenStack cluster, it is
called a nested Kubernetes cluster. TF components are shared
between the two clusters.

Prerequisites

Ensure that the following prerequisites are met before provisioning a
nested Kubernetes cluster:

1. Ensure that you have an operational TF-OpenStack cluster based
   on Tungsten Fabric Release 19<xx>..

2. Ensure that you have an operational Kubernetes v1.12.9 cluster on
   virtual machines created on an TF-OpenStack cluster.

3. Update the ``/etc/hosts`` file on the Kubernetes primary node with
   entries for each node of the cluster.

   For example, if the Kubernetes cluster is made up of three nodes such
   as master1 (IP: x.x.x.x), minion1 (IP: y.y.y.y), and minion2 (IP:
   z.z.z.z). The ``/etc/hosts`` on the Kubernetes primary node must have
   the following entries:

   ::

      x.x.x.x master1
      y.y.y.y minion1
      z.z.z.z minion2

4. If TF container images are stored in a secure docker registry,
   a Kubernetes secret must be created and referenced during `generate a singleyaml`_,
   with credentials of the private docker registry.

   ``kubectl create secret docker-registry name --docker-server=registry --docker-username=username --docker-password=password --docker-email=email -n namespace``

   Command options:

   -  ``name``—Name of the secret.

   -  ``registry``—Name of the registry. Example:
      hub.juniper.net/contrail.

   -  ``username``—Username to log in to the registry.

   -  ``password``—Password to log in to the registry.

   -  ``email``—Registered email of the registry account.

   -  ``namespace``—Kubernetes namespace where the secret must be
      created. This should be the namespace where you intend to create
      the Contrail pods.

The following steps describe how to provision a nested Contrail
Kubernetes cluster.

.. _configure-network-connectivity-to-contrail-configuration-and-data-plane-functions:

Configure network connectivity to TF configuration and data plane functions.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A nested Kubernetes cluster is managed by the same TF control
processes that manage the underlying OpenStack cluster.

The kube-manager is essentially a part of the Tungsten Fabric Config function.
In a nested deployment, one kube-manager instance will is provisioned in
each overlay cluster. This necessitates the need The kube-manager
running in the overlay must have network reachability to Contrail config
functions of the underlay OpenStack cluster.

Network connectivity for the following Contrail config functions are
required:

-  Tungsten Fabric Config

-  Tungsten Fabric Analytics

-  Tungsten Fabric Msg Queue

-  Tungsten Fabric VNC DB

-  Keystone

In addition to config connectivity, the CNI for the Kubernetes cluster
needs network reachability to the vRouter on its Compute node. Network
connectivity for the vRouter data plane function is also required.

You can use the link local service feature or a combination of link
local service with fabric Source Network Address Translation (SNAT)
feature of TF to provide IP reachability to and from the overlay
Kubernetes cluster config and data components to corresponding config
and data compoenents of the underlay OpenStack cluster.

To provide IP reachability to and from the Kubernetes cluster using the
fabric SNAT with link local service, perform the following steps.

1. Enable fabric SNAT on the virtual network of the VMs.

   The fabric SNAT feature must be enabled on the virtual network of the
   virtual machines on which the Kubernetes primary and minions are
   running.

2. Create a link local service for the Container Network Interface (CNI)
   to communicate with its vRouter Agent. This link local service should
   be configured using the Contrail GUI, in the following example:

+-------------+------------------------------------+-------------+-----------+-------------+
| Contrail    | Service IP                         | Service     | Fabric IP | Fabric Port |
| Process     |                                    | Port        |           |             |
+-------------+------------------------------------+-------------+-----------+-------------+
| vRouter     | ``Service-IP for the active node`` | 9091        | 127.0.0.1 | 9091        |
+-------------+------------------------------------+-------------+-----------+-------------+

.. note::

   Fabric IP address is 127.0.0.1 since you must make the CNI communicate
   with the vRouter on its underlay node.

For example, the following link local services must be created:

======================= ========== ============ ========= ===========
Link Local Service Name Service IP Service Port Fabric IP Fabric Port
K8s-cni-to-agent        10.10.10.5 9091         127.0.0.1 9091
======================= ========== ============ ========= ===========

.. note::

   Here 10.10.10.5 is the Service IP address that you chose. This can be
   any unused IP in the cluster. This IP address is primarily used to
   identify link local traffic and has no other significance.

.. _generate a singleyaml:

Generate a single yaml file to create a TF-k8s cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Contrail components are installed on the Kubernetes cluster as pods. The
configuration to create these pods in Kubernetes is encoded in a yaml
file.

This file can be generated as follows:

1. Download the ``contrail-ansible-deployer-19<xx>.<NN>.tgz`` Ansible
   Deployer application tool package onto your provisioning host from
   `Juniper
   Networks <https://www.juniper.net/support/downloads/?p=contrail#sw>`__
   and extract the package.

   ``- tar xvf contrail-ansible-deployer-19<xx>.<NN>.tgz``

2. Navigate to the ``contrail-container-builder`` directory.

   ``cd contrail-container-builder``

3. Populate the ``common.env`` file located in the top directory of the
   cloned contrail-container-builder repo with information corresponding
   to your cluster and environment.

   For a sample ``common.env`` file with the required bare minimum
   configurations, see the
   `common.env.sample.nested_mode <https://github.com/tungstenfabric/tf-container-builder/blob/master/kubernetes/sample_config_files/common.env.sample.nested_mode>`__
   sample configuration file.

   .. note::

      If Contrail container images are stored in a secure docker registry,
      a Kubernetes secret must be created and referenced as documented in
      `4 <provisioning-k8s-cluster.html#prerequisites-step4>`__ of
      Prerequisites. Populate the variable
      KUBERNETES_SECRET_CONTRAIL_REPO=<``secret-name``> with the name of
      the generated Kubernetes secret, in the ``common.env`` file.

4. Generate the yaml file as following in your shell:

   ::

      cd contrail-container-build-repo/kubernetes/manifests

      ./resolve-manifest.sh contrail-kubernetes-nested.yaml  > nested-contrail.yml

5. Copy the output (or file) generated from 4 to the primary node
   in your Kubernetes cluster.

Instantiate the Contrail-k8s cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create TF components as pods on the Kubernetes cluster.

::

   root@k8s:~# kubectl get pods -n kube-system
   NAME                                  READY     STATUS    RESTARTS   AGE
   contrail-kube-manager-lcjbc           1/1       Running   0          3d
   contrail-kubernetes-cni-agent-w8shc   1/1       Running   0          3d

You will see the following pods running in the kube-system namespace:

contrail-kube-manager-xxxxxx—This is the manager that acts as conduit
between Kubernetes and OpenStack clusters

contrail-kubernetes-cni-agent-xxxxx—This installs and configures
TF CNI on Kubernetes nodes

Provisioning of Non-Nested TF Kubernetes Clusters
-------------------------------------------------

In non-nested mode, a Kubernetes cluster is provisioned side by side
with an OpenStack cluster with networking provided by the same Contrail
components of the OpenStack cluster.

Prerequisites

Ensure that the following prerequisites are met before provisioning a
non-nested Kubernetes cluster:

1. You must have an installed and operational TF OpenStack cluster
   based on the Tungsten Fabric Release 19\ ``xx`` release.

2. You must have an installed and operational Kubernetes cluster on the
   server where you want to install the non-nested TF Kubernetes
   cluster.

3. Label the Kubernetes primary node with the TF controller label:

   ``kubectl label node node node-role.opencontrail.org/config=true``

4. Ensure that the Kubelet running on the Kubernetes primary node is not
   run with network plugin options. If kubelet is running with network
   plugin option, then disable or comment out the KUBELET_NETWORK_ARGS
   option in the
   ``/etc/systemd/system/kubelet.service.d/10-kubeadm.conf``
   configuration file.
   
   .. note:: 

      It is recommended that the Kubernetes primary should not be
      configured with a network plugin, so as to not install vRouter kernel
      module on the control node. However, this is optional.

5. Restart the kubelet service:

   ``systemctl daemon-reload;``

   ``systemctl restart kubelet.service``

Provisioning a TF Kubernetes Cluster

Follow these steps to provision TF Kubernetes cluster.

1. Download the ``contrail-ansible-deployer-19<xx>.<NN>.tgz`` Ansible
   Deployer application tool package onto your provisioning host from
   `Juniper
   Networks <https://www.juniper.net/support/downloads/?p=contrail#sw>`__
   and extract the package.

   ``- tar xvf contrail-ansible-deployer-19<xx>.<NN>.tgz``

2. Navigate to the ``contrail-container-builder`` directory.

   ``cd contrail-container-builder``

3. Populate the ``common.env`` file located in the top directory of the
   cloned contrail-container-builder repo with information corresponding
   to your cluster and environment.

   For a sample ``common.env`` file with required bare minimum
   configurations, see the
   `common.env.sample.non_nested_mode <https://github.com/tungstenfabric/tf-container-builder/blob/master/kubernetes/sample_config_files/common.env.sample.non_nested_mode>`__
   sample configuration file.

   .. note::

      If Config API is not secured by keystone, ensure that ``AUTH_MODE``
      and ``KEYSTONE_*`` variables are not configured or present while
      populating the ``common.env`` file.

4. Generate the yaml file as shown below:

   ::

      cd contrail-container-build-repo/kubernetes/manifests

      ./resolve-manifest.sh contrail-kubernetes-nested.yaml  > non-nested-contrail.yml

5. Copy the file generated from 4 to the primary
   node in your Kubernetes cluster.

6. Create TF components as pods on the Kubernetes cluster as
   follows:

   ``kubectl apply -f non-nested-contrail.yml``

7. Create the following TF pods on the Kubernetes cluster. Ensure
   that TF-agent pod is created only on the worker node.

   ::

      [root@b4s403 manifests]# kubectl get pods --all-namespaces -o wide
             NAMESPACE     NAME                             READY     STATUS    RESTARTS   AGE       IP            NODE
             kube-system   contrail-agent-mxkcq             2/2       Running   0          1m        <x.x.x.x>     b4s402
             kube-system   contrail-kube-manager-glw5m      1/1       Running   0          1m        <x.x.x.x>     b4s403

 
