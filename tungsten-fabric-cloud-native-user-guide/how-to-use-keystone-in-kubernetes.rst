How to Enable Keystone Authentication in a Juju Cluster within a Kubernetes Environment
=======================================================================================

:date: 2020-12-08

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

Starting in Contrail Networking Release 2011, Kubernetes can use the
Keystone authentication service in Openstack for authentication in
environments that contain cloud networks using Openstack and Kubernetes
orchestrators when the Kubernetes environment is using Juju. This
capability is available when the cloud networks are both using Contrail
Networking and when the Kubernetes cluster was created in an environment
using Juju.

This document discusses how to enable keystone authentication in
Kubernetes environments and contains the following sections:

.. raw:: html

   </div>

.. raw:: html

   </div>

Overview: Keystone Authentication in Kubernetes Environments with a Juju Cluster
--------------------------------------------------------------------------------

A cloud environment that includes Contrail clusters in
Kubernetes-orchestrated environments and OpenStack-orchestrated
environments can simplify authentication processes by having a single
authentication service in place of each orchestrator authenticating
separately. The ability for a Kubernetes-orchestrated environment to
authenticate using the Keystone service from Openstack can provide this
capability when the Kubernetes environment is using Juju.

Kubernetes is able to authenticate users using Keystone when the
contrail-controller charm in Juju has relations with both an Openstack
orchestrator and the Kubernetes orchestrator. The contrail-controller
charm—when the Keystone service in Kubernetes is enabled—passes the
credentials from Keystone to the contrail-kubernetes-master charm. The
contrail-kubernetes-master charm then passes the Keystone parameters to
kubemanager.

Both orchestrators use their native authentication processes by default.
The ability for Kubernetes to use Keystone authentication in an
environment using Juju was introduced in Contrail Networking Release
2011 and must be user-enabled.

How to Enable Keystone Authentication in a Kubernetes Environment
-----------------------------------------------------------------

To enable Keystone authentication for Kubernetes:

1. In Juju running in the Kubernetes cluster, add a relation between the
   kubernetes-master and Keystone and configure the Kubernetes master to
   use Keystone authorization:

   .. raw:: html

      <div id="jd0e38" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju add-relation kubernetes-master keystone
      juju config kubernetes-master authorization-mode="Node,RBAC" enable-keystone-authorization=true

   .. raw:: html

      </div>

   .. raw:: html

      </div>

2. Ensure that IP Fabric Forwarding for the pod network in the default
   kube-system project is disabled and that SNAT is enabled. SNAT
   enablement is required to reach the Keystone service from the
   keystone-auth pod in Kubernetes.

   You can disable IP Fabric Forwarding and enable SNAT from the kubectl
   CLI or from the Tungsten Fabric GUI.

   -  *Kubectl*:

      Navigate to kubectl edit ns default and add the following
      configuration:

      .. raw:: html

         <div id="jd0e57" class="sample" dir="ltr">

      .. raw:: html

         <div class="output" dir="ltr">

      ::

         metadata:
           annotations:
             opencontrail.org/ip_fabric_snat: "true"

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   -  *Tungsten Fabric Graphical User Interface*

      Change the appropriate settings in the Configure > Networking >
      Networks > default-domain > k8s-kube-system workflow.

3. In Juju, apply the policy.json configuration:

   .. raw:: html

      <div id="jd0e72" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      juju config kubernetes-master keystone-policy="$(cat policy.json)"

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   The JSON configuration varies by environment and the JSON
   configuration option descriptions are beyond the scope of this
   document.

   A sample JSON configuration file is provided for reference:

   .. raw:: html

      <div id="jd0e79" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: k8s-auth-policy
        namespace: kube-system
        labels:
          k8s-app: k8s-keystone-auth
      data:
        policies: |
          [
            {
             "resource": {
                "verbs": ["get", "list", "watch"],
                "resources": ["*"],
                "version": "*",
                "namespace": "*"
              },
              "match": [
                {
                  "type": "role",
                  "values": ["*"]
                },
                {
                  "type": "project",
                  "values": ["k8s"]
                }
              ]
            },
            {
             "resource": {
                "verbs": ["*"],
                "resources": ["*"],
                "version": "*",
                "namespace": "myproject"
              },
              "match": [
                {
                  "type": "role",
                  "values": ["*"]
                },
                {
                  "type": "project",
                  "values": ["k8s-myproject"]
                }
              ]
            }
          ]

   .. raw:: html

      </div>

   .. raw:: html

      </div>

4. Install client tools on the jumphost or an another node outside of
   the cluster.

   .. raw:: html

      <div id="jd0e85" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      sudo snap install kubectl --classic
      sudo snap install client-keystone-auth --edge

   .. raw:: html

      </div>

   .. raw:: html

      </div>

5. In Kubernetes, configure the Keystone context and set credentials:

   .. raw:: html

      <div id="jd0e91" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      kubectl config set-context keystone --user=keystone-user
      kubectl config use-context keystone
      kubectl config set-credentials keystone-user --exec-command=/snap/bin/client-keystone-auth
      kubectl config set-credentials keystone-user --exec-api-version=client.authentication.k8s.io/v1beta1

   .. raw:: html

      </div>

   .. raw:: html

      </div>

6. Apply the required settings to the environment:

   .. raw:: html

      <div id="jd0e97" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      export OS_IDENTITY_API_VERSION=3
      export OS_USER_DOMAIN_NAME=admin_domain
      export OS_USERNAME=admin
      export OS_PROJECT_DOMAIN_NAME=admin_domain
      export OS_PROJECT_NAME=admin
      export OS_DOMAIN_NAME=admin_domain
      export OS_PASSWORD=password
      export OS_AUTH_URL=http://192.168.30.78:5000/v3

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   If preferred, you can also perform this step from stackrc.

7. From kubectl, use the configuration to create a namespace from
   keystone authentication.

   .. raw:: html

      <div id="jd0e105" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      root@noden18:[~]$ kubectl -v=5 --insecure-skip-tls-verify=true -s https://192.168.30.29:6443 get pods --all-namespaces
      NAMESPACE     NAME                                READY   STATUS    RESTARTS   AGE
      default       cirros                              1/1     Running   0          30h
      kube-system   coredns-6b59b8bd9f-2nb4x            1/1     Running   3          33h
      kube-system   k8s-keystone-auth-db47ff559-sh59p   1/1     Running   0          33h
      kube-system   k8s-keystone-auth-db47ff559-vrfwd   1/1     Running   0          33h

   .. raw:: html

      </div>

   .. raw:: html

      </div>

 
