Installing Contrail with Kubernetes by Using Juju Charms
========================================================

 

You can deploy Tungsten Fabric using Juju Charms. Juju helps you
deploy, configure, and efficiently manage applications on private clouds
and public clouds. Juju accesses the cloud with the help of a Juju
controller. A Charm is a module containing a collection of scripts and
metadata and is used with Juju to deploy TF.

A Juju Charm helps you deploy Docker containers to the cloud. For more
information on containerized TF, see `Understanding Contrail
Containers <../concept/summary-of-container-design.html>`__. Juju Charms
simplifies TF deployment by providing a simple way to deploy,
configure, scale, and manage TF operations.

Understanding Juju Charms with Kubernetes
-----------------------------------------

TF supports the following charms:

-  contrail-agent

-  contrail-analytics

-  contrail-analyticsdb

-  contrail-controller

-  contrail-kubernetes-master

-  contrail-kubernetes-node

Preparing to Deploy TF with Kubernetes by Using Juju Charms
-----------------------------------------------------------

You can deploy Tungsten Fabric by using Juju bundle.

Follow these steps to prepare for deployment:

1. Install Juju.

   ::

      apt install bridge-utils -y 
      apt install snapd -y 
      snap install juju --classic

2. Configure Juju.

   You can add a cloud to Juju, identify clouds supported by Juju, and
   manage clouds already added to Juju.

   Adding a cloud

   Juju already has knowledge of the AWS cloud, which means adding your
   AWS account to Juju is quick and easy.

   ::

      juju show-cloud --local aws

   .. note::

      In versions prior to Juju v.2.6.0 the ``show-cloud`` command only
      operates locally. There is no ``--local`` option.

   You must ensure that Juju’s information is up to date (e.g. new
   region support). Run the following command to update Juju’s public
   cloud data:

   ::

      juju update-public-clouds

   Juju recognizes a wide range of cloud types. You can use any one of
   the following methods to add a cloud credentials to Juju:

   -  Adding a Cloud Credentials by Using Interactive Command

      *Example: Adding AWS cloud credentials to Juju*

      ::

         juju add-credential aws

         Enter credential name: jlaurin

         Using auth-type "access-key".

         Enter access-key: AKIAIFII5EH5FOCYZJMA

         Enter secret-key: ******************************

         Credential "jlaurin" added locally for cloud "aws".

   -  Adding a Cloud Credentials Manually
      You can use a YAML configuration file to add AWS cloud
      credentials. Run the following command:
      ::

         juju add-credential aws -f <mycreds.yaml>

      For details, refer to `Juju Adding Credentials from a
      File <https://discourse.jujucharms.com/t/credentials/1112#heading--adding-credentials-from-a-file>`__.

   Identifying a supported cloud

   Use the ``juju clouds`` command to list cloud types that are
   supported by Juju.

   ::

      $ juju clouds
      Cloud        Regions  Default          Type        Description
      aws               15  us-east-1        ec2         Amazon Web Services
      aws-china          1  cn-north-1       ec2         Amazon China
      aws-gov            1  us-gov-west-1    ec2         Amazon (USA Government)
      azure             26  centralus        azure       Microsoft Azure
      azure-china        2  chinaeast        azure       Microsoft Azure China
      cloudsigma         5  hnl              cloudsigma  CloudSigma Cloud
      google            13  us-east1         gce         Google Cloud Platform
      joyent             6  eu-ams-1         joyent      Joyent Cloud
      oracle             5  uscom-central-1  oracle      Oracle Cloud
      rackspace          6  dfw              rackspace   Rackspace Cloud
      localhost          1  localhost        lxd         LXD Container Hypervisor

3. Create a Juju controller.

   ::

      juju bootstrap --bootstrap-series=xenial <cloud name> <controller name>

   A Juju controller manages and keeps track of applications in the Juju
   cloud environment.

4. Download the Contrail bundle from `JAAS - TF Kubernetes <https://jaas.ai/u/juniper-os-software/contrail-k8s>`__.

Deploying TF Charms with Kubernetes
-----------------------------------------
Juju Charms simplifies TF deployment by providing a simple way to
deploy, configure, scale, and manage TF operations.

You can deploy TF Charms in a bundle or manually.
Deploying TF Charms in a Bundle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to deploy TF Charms in a bundle.

1. Deploy TF Charms.

   To deploy TF Charms in a bundle, use the
   ``juju deploy <bundle_yaml_file>`` command.
   The following example shows you how to use a bundle YAML file to
   deploy Contrail on Amazon Web Services (AWS) Cloud.
   ::

      series: "bionic"

      machines:

        # kubernetes pods
        0:
          series: "bionic"
          constraints: mem=8G cores=2 root-disk=60G

        # kubernetes master
        2:
          series: "bionic"
          constraints: mem=8G cores=2 root-disk=60G

        # TF components
        5:
          series: "bionic"
          constraints: mem=16G cores=4 root-disk=60G

      services:

        # kubernetes

        easyrsa:
          series: "bionic"
          charm: cs:~containers/easyrsa
          num_units: 1
          annotations:
            gui-x: '1168.1039428710938'
            gui-y: '-59.11077045466004'
          to:
          - lxd:2

        etcd:
          series: "bionic"
          charm: cs:~containers/etcd
          annotations:
            gui-x: '1157.2041015625'
            gui-y: '719.1614406201691'
          num_units: 1
          options:
            channel: 3.2/stable
          to: [2]

        kubernetes-master:
          series: "bionic"
          charm: cs:~containers/kubernetes-master-696
          annotations:
            gui-x: '877.1133422851562'
            gui-y: '325.6035540382413'
          expose: true
          num_units: 1
          options:
            channel: '1.14/stable'
            service-cidr: '10.96.0.0/12'
            docker_runtime: 'custom'
            docker_runtime_repo: 'deb [arch={ARCH}] https://download.docker.com/linux/ubuntu {CODE} stable'
            docker_runtime_key_url: 'https://download.docker.com/linux/ubuntu/gpg'
            docker_runtime_package: 'docker-ce'
          to: [2]

        kubernetes-worker:
          series: "bionic"
          charm: cs:~containers/kubernetes-worker-550
          annotations:
            gui-x: '745.8510131835938'
            gui-y: '-57.369691124215706'
          num_units: 1
          options:
            channel: '1.14/stable'
            docker_runtime: 'custom'
            docker_runtime_repo: 'deb [arch={ARCH}] https://download.docker.com/linux/ubuntu {CODE} stable'
            docker_runtime_key_url: 'https://download.docker.com/linux/ubuntu/gpg'
            docker_runtime_package: 'docker-ce'
          to: [0]

        # contrail-kubernetes

        contrail-kubernetes-master:
          series: "bionic"
          charm: cs:~juniper-os-software/contrail-kubernetes-master
          annotations:
            gui-x: '586.8027801513672'
            gui-y: '753.914497641757'
          options:
            log-level: 'SYS_DEBUG'
            service_subnets: '10.96.0.0/12'
            docker-registry: "opencontrailnightly"
            image-tag: "master-latest"

        contrail-kubernetes-node:
          series: "bionic"
          charm: cs:~juniper-os-software/contrail-kubernetes-node
          annotations:
            gui-x: '429.1971130371094'
            gui-y: '216.05209087397168'
          options:
            log-level: 'SYS_DEBUG'
            docker-registry: "opencontrailnightly"
            image-tag: "master-latest"

        # contrail

        contrail-agent:
          series: "bionic"
          charm: cs:~juniper-os-software/contrail-agent
          annotations:
            gui-x: '307.5467224121094'
            gui-y: '-24.150856522753656'
          options:
            log-level: 'SYS_DEBUG'
            docker-registry: "opencontrailnightly"
            image-tag: "master-latest"

        contrail-analytics:
          series: "bionic"
          charm: cs:~juniper-os-software/contrail-analytics
          annotations:
            gui-x: '15.948270797729492'
            gui-y: '705.2326686475128'
          expose: true
          num_units: 1
          options:
            log-level: 'SYS_DEBUG'
            docker-registry: "opencontrailnightly"
            image-tag: "master-latest"
          to: [5]

        contrail-analyticsdb:
          series: "bionic"
          charm: cs:~juniper-os-software/contrail-analyticsdb
          annotations:
            gui-x: '24.427139282226562'
            gui-y: '283.9550754931123'
          num_units: 1
          options:
            cassandra-minimum-diskgb: '4'
            cassandra-jvm-extra-opts: '-Xms1g -Xmx2g'
            log-level: 'SYS_DEBUG'
            docker-registry: "opencontrailnightly"
            image-tag: "master-latest"
          to: [5]

        contrail-controller:
          series: "bionic"
          charm: cs:~juniper-os-software/contrail-controller
          annotations:
            gui-x: '212.01282501220703'
            gui-y: '480.69961284662793'
          expose: true
          num_units: 1
          options:
            auth-mode: 'no-auth'
            cassandra-minimum-diskgb: '4'
            cassandra-jvm-extra-opts: '-Xms1g -Xmx2g'
            log-level: 'SYS_DEBUG'
            docker-registry: "opencontrailnightly"
            image-tag: "master-latest"
          to: [5]

        # misc

        ntp:
          charm: "cs:bionic/ntp"
          annotations:
            gui-x: '678.6017761230469'
            gui-y: '415.27124759750086'

      relations:


      - [ kubernetes-master:kube-api-endpoint, kubernetes-worker:kube-api-endpoint ]
      - [ kubernetes-master:kube-control, kubernetes-worker:kube-control ]
      - [ kubernetes-master:certificates, easyrsa:client ]
      - [ kubernetes-master:etcd, etcd:db ]
      - [ kubernetes-worker:certificates,  easyrsa:client ]
      - [ etcd:certificates, easyrsa:client ]

      # contrail
      - [ kubernetes-master, ntp ]
      - [ kubernetes-worker, ntp ]
      - [ contrail-controller, ntp ]

      - [ contrail-controller, contrail-analytics ]
      - [ contrail-controller, contrail-analyticsdb ]
      - [ contrail-analytics, contrail-analyticsdb ]
      - [ contrail-agent, contrail-controller ]

      # contrail-kubernetes
      - [ contrail-kubernetes-node:cni, kubernetes-master:cni ]
      - [ contrail-kubernetes-node:cni, kubernetes-worker:cni ]
      - [ contrail-kubernetes-master:contrail-controller, contrail-controller:contrail-controller ]
      - [ contrail-kubernetes-master:kube-api-endpoint, kubernetes-master:kube-api-endpoint ]
      - [ contrail-agent:juju-info, kubernetes-worker:juju-info ]
      - [ contrail-agent:juju-info, kubernetes-master:juju-info ]
      - [ contrail-kubernetes-master:contrail-kubernetes-config, contrail-kubernetes-node:contrail-kubernetes-config ]

   You can create or modify the TF Charm deployment bundle YAML
   file to:

   -  Point to machines or instances where the TF Charms must be
      deployed.

   -  Include the options you need.

      Each TF Charm has a specific set of options. The options you
      choose depend on the charms you select. For more information on
      the options that are available, see ``config.yaml`` file for each
      charm located at `TF Charms <https://github.com/tungstenfabric/tf-charms>`__.

2. (Optional) Check the status of deployment.

   You can check the status of the deployment by using the
   ``juju status`` command.

3. Enable configuration statements.

   Based on your deployment requirements, you can enable the following
   configuration statements:

   -  ``contrail-agent``

      For more information, see
      https://github.com/tungstenfabric/tf-charms/blob/master/contrail-agent/README.md.

   -  ``contrail-analytics``

      For more information, see
      https://github.com/tungstenfabric/tf-charms/blob/master/contrail-analytics/README.md.

   -  ``contrail-analyticsdb``

      For more information, see
      https://github.com/tungstenfabric/tf-charms/blob/master/contrail-analyticsdb/README.md.

   -  ``contrail-controller``

      For more information, see
      https://github.com/tungstenfabric/tf-charms/blob/master/contrail-controller/README.md.

   -  ``contrail-kubernetes-master``

      For more information, see
      https://github.com/tungstenfabric/tf-charms/blob/master/contrail-kubernetes-master/README.md.

   -  ``contrail-kubernetes-node``

      For more information, see
      https://github.com/tungstenfabric/tf-charms/blob/master/contrail-kubernetes-node/README.md.

Deploying Juju Charms with Kubernetes Manually
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you begin deployment, ensure that you have:

-  Installed and configured Juju

-  Created a Juju controller

-  Installed Ubuntu 16.04 or Ubuntu 18.04

Follow these steps to deploy Juju Charms with Kubernetes manually:

1. Create machine instances for Kubernetes master, Kubernetes workers,
   and TF.

   ::

      juju add-machine ssh:<sshusername>@<IP> --constraints mem=8G cores=2 root-disk=32G --series=xenial  #for Kubernetes worker machine

   ::

      juju add-machine ssh:<sshusername>@<IP> --constraints mem=18G cores=2 root-disk=32G --series=xenial #for Kubernetes master machine

   ::

      juju add-machine ssh:<sshusername>@<IP> --constraints mem=16G cores=4 root-disk=32G --series=xenial #for TF machine

2. Deploy the Kubernetes services.

   Some of the applications may need an additional configuration.

   You can deploy Kubernetes services using any one of the following
   methods:

   -  By specifying the Kubernetes parameters in a YAML file

   -  By using CLI

   -  By using a combination of YAML-formatted file and CLI

   .. note::

      You must use the same docker version for TF and Kubernetes.

   For more details, refer to `Juju Application Configuration <https://old-docs.jujucharms.com/2.4/en/charms-config>`__.

3. Deploy and configure ntp, easyrsa, etcd, kubernetes-master,
   kubernetes-worker.

   ::

      juju deploy cs:xenial/ntp ntp

      juju deploy cs:~containers/easyrsa easyrsa --to lxd:0

      juju deploy cs:~containers/etcd etcd \
          --resource etcd=3 \
          --resource snapshot=0
      juju set etcd channel="3.2/stable"

      juju deploy cs:~containers/kubernetes-master kubernetes-master \
          --resource cdk-addons=0 \
          --resource kube-apiserver=0 \
          --resource kube-controller-manager=0 \
          --resource kube-proxy=0 \
          --resource kube-scheduler=0 \
          --resource kubectl=0
      juju set kubernetes-master channel="1.14/stable" \
          enable-dashboard-addons="false" \
          enable-metrics="false" \
          dns-provider="none" \
          docker_runtime="custom" \
          docker_runtime_repo="deb [arch={ARCH}] https://download.docker.com/linux/ubuntu {CODE} stable" \
          docker_runtime_key_url="https://download.docker.com/linux/ubuntu/gpg" \
          docker_runtime_package="docker-ce"

      juju deploy cs:~containers/kubernetes-worker kubernetes-worker \
          --resource kube-proxy="0" \
          --resource kubectl="0" \
          --resource kubelet="0"
      juju set kubernetes-worker channel="1.14/stable" \
          ingress="false" \
          docker_runtime="custom" \
          docker_runtime_repo="deb [arch={ARCH}] https://download.docker.com/linux/ubuntu {CODE} stable" \
          docker_runtime_key_url="https://download.docker.com/linux/ubuntu/gpg" \
          docker_runtime_package="docker-ce"

4. Deploy and configure TF services.

   Deploy contrail-analyticsdb, contrail-analytics, contrail-controller,
   contrail-kubernetes-master, contrail-kubernetes-node, contrail-agent
   from the directory where you have downloaded the charms.

   .. note::

      You must set the ``auth-mode`` parameter of the contrail-controller
      charm to no-auth if TF is deployed without a keystone.

   ::

      juju deploy contrail-analytics contrail-analytics

      juju deploy contrail-analyticsdb contrail-analyticsdb
      juju set contrail-analyticsdb cassandra-minimum-diskgb="4" cassandra-jvm-extra-opts="-Xms1g -Xmx2g"

      juju deploy contrail-controller contrail-controller
      juju set contrail-controller cassandra-minimum-diskgb="4" cassandra-jvm-extra-opts="-Xms1g -Xmx2g" auth-mode="no-auth"

      juju deploy contrail-kubernetes-master contrail-kubernetes-master

      juju deploy contrail-kubernetes-node contrail-kubernetes-node

      juju deploy contrail-agent contrail-agent

5. Enable applications to be available to external traffic:

   ::

      juju expose kubernetes-master
      juju expose kubernetes-worker

6. Enable contrail-controller and contrail-analytics services to be
   available to external traffic if you do not use HAProxy.

   ::

      juju expose contrail-controller
      juju expose contrail-analytics

7. Apply SSL.

   You can apply SSL if needed. To use SSL with TF services,
   deploy easy-rsa service and ``add-relation`` command to create
   relations to contrail-controller service and contrail-agent services.

   ::

      juju add-relation easyrsa contrail-controller
      juju add-relation easyrsa contrail-analytics
      juju add-relation easyrsa contrail-analyticsdb
      juju add-relation easyrsa contrail-kubernetes-master
      juju add-relation easyrsa contrail-agent

8. Add other necessary relations.

   ::

      juju add-relation "contrail-controller" "contrail-analytics"
      juju add-relation "contrail-controller" "contrail-analyticsdb"
      juju add-relation "contrail-analytics" "contrail-analyticsdb"
      juju add-relation "contrail-agent" "contrail-controller"
      juju add-relation "contrail-controller" "ntp"
      juju add-relation “kubernetes-worker”, “ntp”
      juju add-relation “kubernetes-master”, “ntp”

      juju add-relation "kubernetes-master:kube-api-endpoint" "kubernetes-worker:kube-api-endpoint"
      juju add-relation "kubernetes-master:kube-control" "kubernetes-worker:kube-control"
      juju add-relation "kubernetes-master:certificates" "easyrsa:client"
      juju add-relation "kubernetes-master:etcd" "etcd:db"
      juju add-relation "kubernetes-worker:certificates" "easyrsa:client"
      juju add-relation "etcd:certificates" "easyrsa:client"

      juju add-relation contrail-agent:juju-info, kubernetes-master:juju-info

      juju add-relation "contrail-kubernetes-node:cni" "kubernetes-master:cni"
      juju add-relation "contrail-kubernetes-node:cni" "kubernetes-worker:cni"
      juju add-relation "contrail-kubernetes-master:contrail-controller" "contrail-controller:contrail-controller"
      juju add-relation "contrail-kubernetes-master:kube-api-endpoint" "kubernetes-master:kube-api-endpoint"
      juju add-relation "contrail-agent:juju-info" "kubernetes-worker:juju-info"
      juju add-relation "contrail-agent:juju-info" "kubernetes-master:juju-info"
      juju add-relation "contrail-kubernetes-master:contrail-kubernetes-config" "contrail-kubernetes-node:contrail-kubernetes-config"

 
