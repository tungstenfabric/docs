# Provisioning of Kubernetes Clusters

 

<div id="intro">

<div class="mini-toc-intro">

Contrail Networking supports the following ways of provisioning
Kubernetes clusters:

</div>

</div>

## Provisioning of a Standalone Kubernetes Cluster

You can provision a standalone Kubernetes cluster using
contrail-ansible-deployer.

Perform the following steps to install one Kubernetes cluster and one
Contrail cluster and integrate them together.

1.  <span id="jd0e25">See [Supported Platforms Contrail
    Release](/documentation/en_US/contrail19/information-products/topic-collections/release-notes/topic-143725.html#jd0e140)
    for a list of supported platforms.</span>

2.  <span id="jd0e31">Install the necessary tools.</span>

    `yum -y install epel-release git ansible net-tools`

3.  <span id="jd0e37">Download the
    `contrail-ansible-deployer-19<xx>.<NN>.tgz` Ansible Deployer
    application tool package onto your provisioning host from [Contrail
    Downloads](https://www.juniper.net/support/downloads/?p=contrail#sw)
    page and extract the package.</span>

    `- tar xvf contrail-ansible-deployer-19<xx>.<NN>.tgz`

4.  <span id="jd0e49">Navigate to the `contrail-ansible-deployer`
    directory.</span>

    `cd contrail-ansible-deployer`

5.  <span id="jd0e58">Edit the `config/instances.yaml` and enter the
    necessary values. See [Understanding contrail-ansible-deployer used
    in Contrail
    Command](../../concept/install-contrail-overview-ansible-50.html)
    for a sample `config/instances.yaml` file.</span>

6.  <span id="jd0e69">Turn off the <span class="cli"
    v-pre="">swap</span> functionality on all nodes.</span>

    `swapoff -a`

7.  <span id="jd0e78">Configure the nodes.</span>

    `ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/configure_instances.yml`

8.  <span id="jd0e84">Install Kubernetes and Contrail.</span>

    `ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/install_k8s.yml`

    `ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/install_contrail.yml `

9.  <span id="jd0e93">Turn on the <span class="cli" v-pre="">swap</span>
    functionality on all nodes.</span>

    `swapon -a`

## Provisioning of Nested Contrail Kubernetes Clusters

When Contrail provides networking for a Kubernetes cluster that is
provisioned on the workloads of a Contrail-OpenStack cluster, it is
called a nested Kubernetes cluster. Contrail components are shared
between the two clusters.

<span class="kbd user-typing" v-pre="">Prerequisites</span>

Ensure that the following prerequisites are met before provisioning a
nested Kubernetes cluster:

1.  <span id="jd0e117">Ensure that you have an operational
    Contrail-OpenStack cluster based on Contrail Networking Release
    19&lt;xx&gt;..</span>

2.  <span id="jd0e120">Ensure that you have an operational Kubernetes
    v1.12.9 cluster on virtual machines created on an Contrail-OpenStack
    cluster.</span>

3.  <span id="jd0e123">Update the `/etc/hosts` file on the Kubernetes
    primary node with entries for each node of the cluster.</span>

    For example, if the Kubernetes cluster is made up of three nodes
    such as master1 (IP: x.x.x.x), minion1 (IP: y.y.y.y), and minion2
    (IP: z.z.z.z). The `/etc/hosts` on the Kubernetes primary node must
    have the following entries:

    <div id="jd0e134" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        x.x.x.x master1
        y.y.y.y minion1
        z.z.z.z minion2

    </div>

    </div>

4.  <span id="prerequisites-step4">If Contrail container images are
    stored in a secure docker registry, a Kubernetes secret must be
    created and referenced during [Generate a single yaml file to create
    a Contrail-k8s
    cluster](provisioning-k8s-cluster.html#id-generate-a-single-yaml-file-to-create-a-contrailk8s-cluster),
    with credentials of the private docker registry.</span>

    <div id="jd0e142" class="sample" dir="ltr">

    <div id="jd0e143" dir="ltr">

    `kubectl create secret docker-registry name --docker-server=registry --docker-username=username --docker-password=password --docker-email=email -n namespace`

    </div>

    </div>

    Command options:

    -   `name`—Name of the secret.

    -   `registry`—Name of the registry. Example:
        hub.juniper.net/contrail.

    -   `username`—Username to log in to the registry.

    -   `password`—Password to log in to the registry.

    -   `email`—Registered email of the registry account.

    -   `namespace`—Kubernetes namespace where the secret must be
        created. This should be the namespace where you intend to create
        the Contrail pods.

The following steps describe how to provision a nested Contrail
Kubernetes cluster.

1.  [Configure network connectivity to Contrail configuration and data
    plane
    functions.](provisioning-k8s-cluster.html#id-create-linklocal-services-in-the-contrailopenstack-cluster)

2.  [Generate a single yaml file to create a Contrail-k8s
    cluster](provisioning-k8s-cluster.html#id-generate-a-single-yaml-file-to-create-a-contrailk8s-cluster)

3.  [Instantiate the Contrail-k8s
    cluster](provisioning-k8s-cluster.html#id-instantiate-the-contrailk8s-cluster)

### Configure network connectivity to Contrail configuration and data plane functions.

A nested Kubernetes cluster is managed by the same Contrail control
processes that manage the underlying OpenStack cluster.

The kube-manager is essentially a part of the Contrail Config function.
In a nested deployment, one kube-manager instance will is provisioned in
each overlay cluster. This necessitates the need The kube-manager
running in the overlay must have network reachability to Contrail config
functions of the underlay OpenStack cluster.

Network connectivity for the following Contrail config functions are
required:

-   Contrail Config

-   Contrail Analytics

-   Contrail Msg Queue

-   Contrail VNC DB

-   Keystone

In addition to config connectivity, the CNI for the Kubernetes cluster
needs network reachability to the vRouter on its Compute node. Network
connectivity for the vRouter data plane function is also required.

You can use the link local service feature or a combination of link
local service with fabric Source Network Address Translation (SNAT)
feature of Contrail to provide IP reachability to and from the overlay
Kubernetes cluster config and data components to corresponding config
and data compoenents of the underlay OpenStack cluster.

To provide IP reachability to and from the Kubernetes cluster using the
fabric SNAT with link local service, perform the following steps.

1.  <span id="jd0e235">Enable fabric SNAT on the virtual network of the
    VMs.</span>

    The fabric SNAT feature must be enabled on the virtual network of
    the virtual machines on which the Kubernetes primary and minions are
    running.

2.  <span id="jd0e240">Create a link local service for the Container
    Network Interface (CNI) to communicate with its vRouter Agent. This
    link local service should be configured using the Contrail GUI, in
    the following example:</span>

|                  |                                  |              |           |             |
|:-----------------|:---------------------------------|:-------------|:----------|:------------|
| Contrail Process | Service IP                       | Service Port | Fabric IP | Fabric Port |
| vRouter          | `Service-IP for the active node` | 9091         | 127.0.0.1 | 9091        |

**Note**

Fabric IP address is 127.0.0.1 since you must make the CNI communicate
with the vRouter on its underlay node.

For example, the following link local services must be created:

|                         |            |              |           |             |
|:------------------------|:-----------|:-------------|:----------|:------------|
| Link Local Service Name | Service IP | Service Port | Fabric IP | Fabric Port |
| K8s-cni-to-agent        | 10.10.10.5 | 9091         | 127.0.0.1 | 9091        |

**Note**

Here 10.10.10.5 is the Service IP address that you chose. This can be
any unused IP in the cluster. This IP address is primarily used to
identify link local traffic and has no other significance.

### Generate a single yaml file to create a Contrail-k8s cluster

Contrail components are installed on the Kubernetes cluster as pods. The
configuration to create these pods in Kubernetes is encoded in a yaml
file.

This file can be generated as follows:

1.  <span id="jd0e343">Download the
    `contrail-ansible-deployer-19<xx>.<NN>.tgz` Ansible Deployer
    application tool package onto your provisioning host from [Juniper
    Networks](https://www.juniper.net/support/downloads/?p=contrail#sw)
    and extract the package.</span>

    `- tar xvf contrail-ansible-deployer-19<xx>.<NN>.tgz`

2.  <span id="jd0e355">Navigate to the `contrail-container-builder`
    directory.</span>

    `cd contrail-container-builder`

3.  <span id="jd0e364">Populate the `common.env` file located in the top
    directory of the cloned contrail-container-builder repo with
    information corresponding to your cluster and environment.</span>

    For a sample `common.env` file with the required bare minimum
    configurations, see the
    [common.env.sample.nested\_mode](https://github.com/tungstenfabric/tf-container-builder/blob/master/kubernetes/sample_config_files/common.env.sample.nested_mode)
    sample configuration file.

    **Note**

    If Contrail container images are stored in a secure docker registry,
    a Kubernetes secret must be created and referenced as documented in
    [4](provisioning-k8s-cluster.html#prerequisites-step4) of
    Prerequisites. Populate the variable
    KUBERNETES\_SECRET\_CONTRAIL\_REPO=&lt;`secret-name`&gt; with the
    name of the generated Kubernetes secret, in the `common.env` file.

4.  <span id="yaml-step3">Generate the yaml file as following in your
    shell:</span>
    <div id="jd0e392" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        cd contrail-container-build-repo/kubernetes/manifests

        ./resolve-manifest.sh contrail-kubernetes-nested.yaml  > nested-contrail.yml

    </div>

    </div>

5.  <span id="jd0e398">Copy the output (or file) generated from
    [4](provisioning-k8s-cluster.html#yaml-step3) to the primary node in
    your Kubernetes cluster.</span>

### Instantiate the Contrail-k8s cluster

Create contrail components as pods on the Kubernetes cluster.

<div id="jd0e410" class="sample" dir="ltr">

<div class="output" dir="ltr">

    root@k8s:~# kubectl get pods -n kube-system
    NAME                                  READY     STATUS    RESTARTS   AGE
    contrail-kube-manager-lcjbc           1/1       Running   0          3d
    contrail-kubernetes-cni-agent-w8shc   1/1       Running   0          3d

</div>

</div>

You will see the following pods running in the kube-system namespace:

contrail-kube-manager-xxxxxx—This is the manager that acts as conduit
between Kubernetes and OpenStack clusters

contrail-kubernetes-cni-agent-xxxxx—This installs and configures
Contrail CNI on Kubernetes nodes

## Provisioning of Non-Nested Contrail Kubernetes Clusters

In non-nested mode, a Kubernetes cluster is provisioned side by side
with an OpenStack cluster with networking provided by the same Contrail
components of the OpenStack cluster.

<span class="kbd user-typing" v-pre="">Prerequisites</span>

Ensure that the following prerequisites are met before provisioning a
non-nested Kubernetes cluster:

1.  <span id="jd0e434">You must have an installed and operational
    Contrail OpenStack cluster based on the Contrail Networking Release
    19`xx` release.</span>

2.  <span id="jd0e440">You must have an installed and operational
    Kubernetes cluster on the server where you want to install the
    non-nested Contrail Kubernetes cluster.</span>

3.  <span id="jd0e443">Label the Kubernetes primary node with the
    Contrail controller label:</span>
    <div id="jd0e446" class="sample" dir="ltr">

    <div id="jd0e447" dir="ltr">

    `kubectl label node node node-role.opencontrail.org/config=true`

    </div>

    </div>

4.  <span id="jd0e452">Ensure that the Kubelet running on the Kubernetes
    primary node is not run with network plugin options. If kubelet is
    running with network plugin option, then disable or comment out the
    KUBELET\_NETWORK\_ARGS option in the
    `/etc/systemd/system/kubelet.service.d/10-kubeadm.conf`
    configuration file.**Note**</span>

    It is recommended that the Kubernetes primary should not be
    configured with a network plugin, so as to not install vRouter
    kernel module on the control node. However, this is optional.

5.  <span id="jd0e461">Restart the kubelet service:</span>
    <div id="jd0e464" class="sample" dir="ltr">

    <div id="jd0e465" dir="ltr">

    `systemctl daemon-reload; `

    </div>

    <div id="jd0e467" dir="ltr">

    `systemctl restart kubelet.service`

    </div>

    </div>

<span class="kbd user-typing" v-pre="">Provisioning a Contrail
Kubernetes Cluster</span>

Follow these steps to provision Contrail Kubernetes cluster.

1.  <span id="jd0e476">Download the
    `contrail-ansible-deployer-19<xx>.<NN>.tgz` Ansible Deployer
    application tool package onto your provisioning host from [Juniper
    Networks](https://www.juniper.net/support/downloads/?p=contrail#sw)
    and extract the package.</span>

    `- tar xvf contrail-ansible-deployer-19<xx>.<NN>.tgz`

2.  <span id="jd0e491">Navigate to the `contrail-container-builder`
    directory.</span>

    `cd contrail-container-builder`

3.  <span id="jd0e500">Populate the `common.env` file located in the top
    directory of the cloned contrail-container-builder repo with
    information corresponding to your cluster and environment.</span>

    For a sample `common.env` file with required bare minimum
    configurations, see the
    [common.env.sample.non\_nested\_mode](https://github.com/tungstenfabric/tf-container-builder/blob/master/kubernetes/sample_config_files/common.env.sample.non_nested_mode)
    sample configuration file.

    **Note**

    If Config API is not secured by keystone, ensure that `AUTH_MODE`
    and `KEYSTONE_*` variables are not configured or present while
    populating the `common.env` file.

4.  <span id="non-nested-step3">Generate the yaml file as shown
    below:</span>
    <div id="jd0e529" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        cd contrail-container-build-repo/kubernetes/manifests

        ./resolve-manifest.sh contrail-kubernetes-nested.yaml  > non-nested-contrail.yml

    </div>

    </div>

5.  <span id="jd0e535">Copy the file generated from
    [4](provisioning-k8s-cluster.html#non-nested-step3) to the primary
    node in your Kubernetes cluster.</span>

6.  <span id="jd0e540">Create contrail components as pods on the
    Kubernetes cluster as follows:</span>
    <div id="jd0e543" class="sample" dir="ltr">

    <div id="jd0e544" dir="ltr">

    `kubectl apply -f non-nested-contrail.yml`

    </div>

    </div>

7.  <span id="jd0e546">Create the following Contrail pods on the
    Kubernetes cluster. Ensure that contrail-agent pod is created only
    on the worker node.</span>
    <div id="jd0e549" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        [root@b4s403 manifests]# kubectl get pods --all-namespaces -o wide
               NAMESPACE     NAME                             READY     STATUS    RESTARTS   AGE       IP            NODE
               kube-system   contrail-agent-mxkcq             2/2       Running   0          1m        <x.x.x.x>     b4s402
               kube-system   contrail-kube-manager-glw5m      1/1       Running   0          1m        <x.x.x.x>     b4s403

    </div>

    </div>

 
