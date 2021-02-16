Development of TF Operator
==========================

:Date: 2021-02-16

Prerequisities
--------------

To develop TF Operator you will need:

* Go (minimal 1.14.1)
* `Docker <https://github.com/operator-framework/operator-sdk/>`_
* `Operator-SDK <https://github.com/operator-framework/operator-sdk/>`_ (version 0.18)

Building Operator Image
-----------------------

Using Operator-SDK binary in version 0.18, operator may be built from CLI with :command:`operator-sdk build <container name>`.

Afterward, the operator image should be available in the local registry of container images.
Depending on the Kubernetes cluster type, it may be necessary to push the image to an external registry like Docker Hub.
Manually built operator image may be run using kustomize manifests located under ``deploy/kustomize/operator/templates`` directory
by switching ``newName`` and ``newTag`` parameters to values of the custom built image.

Changing Operator API
---------------------

Any change of operator API (files under `pkg/apis/` directory) requires to run 2 commands:

#. ``operator-sdk generate k8s`` - which re-generates Go code for API handling
#. ``operator-sdk generate crds`` - which updates Custom Resource Definition (CRD) files for Tungsten Fabric resources

Writing Kubernetes Operators Best Practises
-------------------------------------------

Here are some best practices in writing Kubernetes operators:

* Operator API should have major changes and maintain legacy deployments with every new change. Any major changes should result in bumping up API version.
* Operator API code should not contain functions, only API structure definitions.
* Operator should manage a single type of application.
* If there is a sequencing or orchestration process, a separate operator should be written to cover the process with delegation to other operators managing smaller sub-deployments.
* Single CRD should be managed with a single controller.
* Operators should be platform-agnostic and dynamically adapt to every deployment environment. No information should be assumed (e.g. deployment namespace)
* No information should be hardcoded. Any necessary information should be obtained via Kubernetes API based on the current deployment environment.
* API should minimize human error by hardening API with OpenAPI spec.

More best practises on developing Kubernetes operators may be found here:

* `Operator Framework Best Practises <https://github.com/operator-framework/community-operators/blob/master/docs/best-practices.md>`_
* `7 Best Practises for Writing Kubernetes Operators: An SRE Perspective <https://www.openshift.com/blog/7-best-practices-for-writing-kubernetes-operators-an-sre-perspective>`_
* `Kubernetes Operators Best Practises <https://www.openshift.com/blog/kubernetes-operators-best-practices>`_
* `How to create a custom resource with Kubernetes Operator <https://codilime.com/how-to-create-a-custom-resource-with-kubernetes-operator/>`_
