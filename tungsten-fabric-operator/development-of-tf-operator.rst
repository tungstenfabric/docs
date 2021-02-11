Development of TF Operator
==========================

Prerequisities
--------------

In order to develop TF Operator you will need:

* Go (minimal 1.14.1)
* `Docker <https://github.com/operator-framework/operator-sdk/>`_
* `Operator-SDK <https://github.com/operator-framework/operator-sdk/>`_ (version 0.18)

Building Operator Image
-----------------------

Using Operator-SDK binary in version 0.18 operator may be build from CLI with :command:`operator-sdk build <container name>`.

Afterwards, operator image should be available in local registry of container images.
Depending on Kubernetes cluster type it may be necessary to push image to external registry like Docker Hub.
Manually built operator image may be run using kustomize manifests located under ``deploy/kustomize/operator/templates`` directory
by switching ``newName`` and ``newTag`` parameters to values of custom built image.


