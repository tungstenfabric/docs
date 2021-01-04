# Installing Contrail with Kubernetes by Using Juju Charms

 

<div id="intro">

<div class="mini-toc-intro">

You can deploy Contrail Networking using Juju Charms. Juju helps you
deploy, configure, and efficiently manage applications on private clouds
and public clouds. Juju accesses the cloud with the help of a Juju
controller. A Charm is a module containing a collection of scripts and
metadata and is used with Juju to deploy Contrail.

A Juju Charm helps you deploy Docker containers to the cloud. For more
information on containerized Contrail, see [Understanding Contrail
Containers](../concept/summary-of-container-design.html). Juju Charms
simplifies Contrail deployment by providing a simple way to deploy,
configure, scale, and manage Contrail operations.

</div>

</div>

## Understanding Juju Charms with Kubernetes

Contrail supports the following charms:

-   contrail-agent

-   contrail-analytics

-   contrail-analyticsdb

-   contrail-controller

-   contrail-kubernetes-master

-   contrail-kubernetes-node

## Preparing to Deploy Contrail with Kubernetes by Using Juju Charms

You can deploy Contrail Networking by using Juju bundle.

Follow these steps to prepare for deployment:

1.  <span id="jd0e64">Install Juju.</span>
    <div id="jd0e67" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        apt install bridge-utils -y 
        apt install snapd -y 
        snap install juju --classic

    </div>

    </div>

2.  <span id="jd0e70">Configure Juju.</span>

    You can add a cloud to Juju, identify clouds supported by Juju, and
    manage clouds already added to Juju.

    <span class="kbd user-typing" v-pre="">Adding a cloud</span>

    Juju already has knowledge of the AWS cloud, which means adding your
    AWS account to Juju is quick and easy.

    <div id="jd0e80" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju show-cloud --local aws

    </div>

    </div>

    **Note**

    In versions prior to Juju v.2.6.0 the `show-cloud` command only
    operates locally. There is no `--local` option.

    You must ensure that Juju’s information is up to date (e.g. new
    region support). Run the following command to update Juju’s public
    cloud data:

    <div id="jd0e94" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju update-public-clouds

    </div>

    </div>

    Juju recognizes a wide range of cloud types. You can use any one of
    the following methods to add a cloud credentials to Juju:

    -   <span class="kbd user-typing" v-pre="">Adding a Cloud
        Credentials by Using Interactive Command</span>

        *Example: Adding AWS cloud credentials to Juju*

        <div id="jd0e108" class="sample" dir="ltr">

        <div class="output" dir="ltr">

            juju add-credential aws

            Enter credential name: jlaurin

            Using auth-type "access-key".

            Enter access-key: AKIAIFII5EH5FOCYZJMA

            Enter secret-key: ******************************

            Credential "jlaurin" added locally for cloud "aws".

        </div>

        </div>

    -   <span class="kbd user-typing" v-pre="">Adding a Cloud
        Credentials Manually</span>

        <div id="jd0e117" class="sample" dir="ltr">

        You can use a YAML configuration file to add AWS cloud
        credentials. Run the following command:

        <div class="output" dir="ltr">

            juju add-credential aws -f <mycreds.yaml>

        </div>

        </div>

        For details, refer to [Juju Adding Credentials from a
        File](https://discourse.jujucharms.com/t/credentials/1112#heading--adding-credentials-from-a-file).

    <span class="kbd user-typing" v-pre="">Identifying a supported
    cloud</span>

    Use the `juju clouds` command to list cloud types that are supported
    by Juju.

    <div id="jd0e135" class="sample" dir="ltr">

    <div class="output" dir="ltr">

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

    </div>

    </div>

3.  <span id="jd0e138">Create a Juju controller.</span>

    <div id="jd0e141" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju bootstrap --bootstrap-series=xenial <cloud name> <controller name>

    </div>

    </div>

    A Juju controller manages and keeps track of applications in the
    Juju cloud environment.

4.  <span id="jd0e148">Download the Contrail bundle from [JAAS -
    Contrail
    Kubernetes](https://jaas.ai/u/juniper-os-software/contrail-k8s).</span>

## Deploying Contrail Charms with Kubernetes

<div class="mini-toc-intro">

Juju Charms simplifies Contrail deployment by providing a simple way to
deploy, configure, scale, and manage Contrail operations.

You can deploy Contrail Charms in a bundle or manually.

</div>

-   [Deploying Contrail Charms in a
    Bundle](deploying-contrail-using-juju-charms-kubernetes.html#DeployingContrailCharmsInABundlek8s)

-   [Deploying Juju Charms with Kubernetes
    Manually](deploying-contrail-using-juju-charms-kubernetes.html#id-deploying-juju-charmsk8s)

### Deploying Contrail Charms in a Bundle

Follow these steps to deploy Contrail Charms in a bundle.

1.  <span id="jd0e181">Deploy Contrail Charms.</span>

    To deploy Contrail Charms in a bundle, use the
    `juju deploy <bundle_yaml_file>` command.

    <div id="jd0e189" class="sample" dir="ltr">

    The following example shows you how to use a bundle YAML file to
    deploy Contrail on Amazon Web Services (AWS) Cloud.

    <div class="output" dir="ltr">

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

          # contrail components
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

    </div>

    </div>

    You can create or modify the Contrail Charm deployment bundle YAML
    file to:

    -   Point to machines or instances where the Contrail Charms must be
        deployed.

    -   Include the options you need.

        Each Contrail Charm has a specific set of options. The options
        you choose depend on the charms you select. For more information
        on the options that are available, see `config.yaml ` file for
        each charm located at [Contrail
        Charms](https://github.com/tungstenfabric/tf-charms).

2.  <span id="jd0e212">(Optional) Check the status of deployment.</span>

    You can check the status of the deployment by using the
    `juju status` command.

3.  <span id="jd0e220">Enable configuration statements.</span>

    Based on your deployment requirements, you can enable the following
    configuration statements:

    -   `contrail-agent`

        For more information, see
        <https://github.com/tungstenfabric/tf-charms/blob/master/contrail-agent/README.md>.

    -   `contrail-analytics`

        For more information, see
        <https://github.com/tungstenfabric/tf-charms/blob/master/contrail-analytics/README.md>.

    -   `contrail-analyticsdb`

        For more information, see
        <https://github.com/tungstenfabric/tf-charms/blob/master/contrail-analyticsdb/README.md>.

    -   `contrail-controller`

        For more information, see
        <https://github.com/tungstenfabric/tf-charms/blob/master/contrail-controller/README.md>.

    -   `contrail-kubernetes-master`

        For more information, see
        <https://github.com/tungstenfabric/tf-charms/blob/master/contrail-kubernetes-master/README.md>.

    -   `contrail-kubernetes-node`

        For more information, see
        <https://github.com/tungstenfabric/tf-charms/blob/master/contrail-kubernetes-node/README.md>.

### Deploying Juju Charms with Kubernetes Manually

Before you begin deployment, ensure that you have:

-   Installed and configured Juju

-   Created a Juju controller

-   Installed Ubuntu 16.04 or Ubuntu 18.04

Follow these steps to deploy Juju Charms with Kubernetes manually:

1.  <span id="jd0e308">Create machine instances for Kubernetes master,
    Kubernetes workers, and Contrail.</span>
    <div id="jd0e311" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju add-machine ssh:<sshusername>@<IP> --constraints mem=8G cores=2 root-disk=32G --series=xenial  #for Kubernetes worker machine

    </div>

    <div class="output" dir="ltr">

        juju add-machine ssh:<sshusername>@<IP> --constraints mem=18G cores=2 root-disk=32G --series=xenial #for Kubernetes master machine

    </div>

    <div class="output" dir="ltr">

        juju add-machine ssh:<sshusername>@<IP> --constraints mem=16G cores=4 root-disk=32G --series=xenial #for Contrail machine

    </div>

    </div>

2.  <span id="jd0e318">Deploy the Kubernetes services.</span>

    Some of the applications may need an additional configuration.

    You can deploy Kubernetes services using any one of the following
    methods:

    -   By specifying the Kubernetes parameters in a YAML file

    -   By using CLI

    -   By using a combination of YAML-formatted file and CLI

    **Note**

    You must use the same docker version for Contrail and Kubernetes.

    For more details, refer to [Juju Application
    Configuration](https://old-docs.jujucharms.com/2.4/en/charms-config).

3.  <span id="jd0e343">Deploy and configure <span class="cli"
    v-pre="">ntp, easyrsa, etcd, kubernetes-master,
    kubernetes-worker</span>.</span>
    <div id="jd0e349" class="sample" dir="ltr">

    <div class="output" dir="ltr">

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

    </div>

    </div>

4.  <span id="jd0e352">Deploy and configure Contrail services.</span>

    Deploy <span class="cli" v-pre="">contrail-analyticsdb,
    contrail-analytics, contrail-controller, contrail-kubernetes-master,
    contrail-kubernetes-node, contrail-agent</span> from the directory
    where you have downloaded the charms.

    **Note**

    You must set the `auth-mode` parameter of the contrail-controller
    charm to <span class="kbd user-typing" v-pre="">no-auth</span> if
    Contrail is deployed without a keystone.

    <div id="jd0e369" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju deploy contrail-analytics contrail-analytics

        juju deploy contrail-analyticsdb contrail-analyticsdb
        juju set contrail-analyticsdb cassandra-minimum-diskgb="4" cassandra-jvm-extra-opts="-Xms1g -Xmx2g"

        juju deploy contrail-controller contrail-controller
        juju set contrail-controller cassandra-minimum-diskgb="4" cassandra-jvm-extra-opts="-Xms1g -Xmx2g" auth-mode="no-auth"

        juju deploy contrail-kubernetes-master contrail-kubernetes-master

        juju deploy contrail-kubernetes-node contrail-kubernetes-node

        juju deploy contrail-agent contrail-agent

    </div>

    </div>

5.  <span id="jd0e372">Enable applications to be available to external
    traffic:</span>
    <div id="jd0e375" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju expose kubernetes-master
        juju expose kubernetes-worker

    </div>

    </div>

6.  <span id="enable-contrail-controller-analytics">Enable
    contrail-controller and contrail-analytics services to be available
    to external traffic if you do not use HAProxy.</span>
    <div id="jd0e381" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju expose contrail-controller
        juju expose contrail-analytics

    </div>

    </div>

7.  <span id="jd0e384">Apply SSL.</span>

    You can apply SSL if needed. To use SSL with Contrail services,
    deploy easy-rsa service and `add-relation` command to create
    relations to contrail-controller service and contrail-agent
    services.

    <div id="jd0e392" class="sample" dir="ltr">

    <div class="output" dir="ltr">

        juju add-relation easyrsa contrail-controller
        juju add-relation easyrsa contrail-analytics
        juju add-relation easyrsa contrail-analyticsdb
        juju add-relation easyrsa contrail-kubernetes-master
        juju add-relation easyrsa contrail-agent

    </div>

    </div>

8.  <span id="jd0e395">Add other necessary relations.</span>
    <div id="jd0e398" class="sample" dir="ltr">

    <div class="output" dir="ltr">

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

    </div>

    </div>

 
