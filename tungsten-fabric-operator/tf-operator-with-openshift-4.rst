TF Operator with Openshift 4.x
==============================

`Code repository <https://github.com/tungstenfabric/tf-openshift>`__

:Date: 2021-02-16


Idea and Why Openshift is different from Standard Kubernetes Cluster
--------------------------------------------------------------------

While many developers see practically no difference deploying day-to-day applications on Kubernetes and Openshift,
there are many significant differences between these two platforms.
Openshift deploys every compnent of the cluster as custom Openshift application (etcd server, API server, controller etc.).
Because these components are separately developed for Openshift purposes, its' architecture differes in details from standard Kubernetes clusters.
From Openshift version 4.x all these components are based on operators.
Openshift brings also a lot of features during installation where some of them requires CNI plugin installed from the begining of a cluster.
While Tungsten Fabric may act as CNI plugin for various orchestration platforms, it is challenging to integrate TF with Openshift platform where CNI plugin is such a vital elements of a whole platform.

Other distinctive problem of Openshift platform is usage of CoreOS nodes.
CoreOS is an operating system designed for orchestrated infrastructures which run containerized workloads.
CoreOS is a read-only filesystem which may be configured only on the boot process and afterward does not allow to change system settings in a runtime.
Ignition configs is a custom way to provide confgiuration for the boot process like what directories, files, systemd services etc. should be created.

Another problem with such a complex platform as Openshift is integration between custom resources.
While platform works only with Openshift components then integration is a natural process developed by the Openshift developers.
But in case when OpenshiftSDN CNI plugin is subsituted with Tungsten Fabric it is challenging to integrate it with other components of the platform - a bit like switching one block in a whole Jenga tower.
For example Openshift will not create network-dependent resources as long as custom resource Network will not have updated status that networking provided by CNI plugin is up and running.

Because of problems listed above in addition to `TF Operator <https://github.com/tungstenfabric/tf-operator>`__ deployment tool it is necessary to provide confgiuration files and manifests specific for Openshift dpeloyment.
`TF Openshift <https://github.com/tungstenfabric/tf-openshift>`__ repository contains all additional files that are required to sucessfully deploy Openshift platform with Tungsten Fabric as CNI plugin.

Find out more on challenges with developing operators for Openshift 4.x `here <https://codilime.com/deploying-a-kubernetes-operator-in-openshift-4-x-platform/>`__ .

