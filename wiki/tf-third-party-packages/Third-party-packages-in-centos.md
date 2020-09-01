# Introduction
This wiki goes over creating or updating rpm third party packages required for contrail

## Overview
The third party packages that are being built fall under 2 categories.
* packages which had to be modified(eg., ifmap-server)
* packages for which rpms were not available (eg., pycassa)

When performing updates, decision to update a package or not is made based on the version information mentioned in the spec file.

This is the convention we follow when creating versions:

1. If we don't modify the third party package in any way, then append the string "0contrail0" to the tag "Release" in the spec file 
2. If we are modifying the third party packages then , append the string "contrail" to the tag "Release" in the spec file. [eg., if we added new patches to a third party package for the current release 3.0 then append string "3contrail" to the version tag in spec file].

[Try issuing rpm upgrade with the new package to make sure that the new package is recognized as the higher version]

## Packages

Currently the following packages are maintained in this repo: 
* ifmap-server 
* python-bitarray 
* python-bottle 
* python-django-horizon 
* python-geventhttpclient 
* python-heatclient 
* python-lxml 
* python-pycassa 
* python-pycrypto 
* python-simplejson 
* python-thrift 
* python-zope-interface 
* redis 
* redis-py 
* supervisor 
* xmltodict 


## Repo Information

This repo contains patches and specs for all the third party packages we are building. Along with that a Makefile is provided by which can build individual packages.
                  The files have been arranged such that when we choose to upstream a new package eg., ifmap-server, we can go to the upstream/rpm/ and copy the ifmap-folder contents to the cloned git@github.com:Juniper/rpms.git and raise a pull request.

1. How to rebuild a thirdparty package?

 Have a build-VM ready. Additionally install git,spectool(to get the source targz given a spec file) and mock-1.1.41 ( to build the rpms given the source and spec file)in the VM. Checkout this repo. Go to $(SB_TOP)/upstream/rpm. Issue make . It should place the rpms(source and binary) in BUILD directory outisde the SandBox.

2. How to setup mock ?

Mock is provided by epel. For centos 6.4 it can be installed the following way:

` wget http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm`</br>
 `rpm -ivh epel-release-6-8.noarch.rpm`</br>
After installing mock, create user and grant sudo access useradd makerpm -G mock su - makerpm rpmdev-setuptree

3. How to debug if the build fails?

 The BUILD directory that gets created outside the sandbox should have a build.log file which contains the error messages.

4. How to add a new package?

 If you have a spec file and/or diffs that you apply to an existing upstream package put that inside the $(SB_TOP)/upstream/rpm/specs/. Change the Make file in $(SB_TOP)/upstream/rpm and add a new target for the package added. The Make should have instructions to start the mock with the spec file and source file location. Use question 2 to debug the make failures.

5. How to upstream a package?

 clone git@github.com:Juniper/rpms.git Copy the folder $(SB_TOP)/upstream/rpm/specs/ to $(SB_TOP_newly_cloned)/specs/ Raise a pull request.

6. Build fails because build dependency packages cannot be fetched

 Identify the repo that hosts the build dependecy package. Add this repo to the config file, upstream/rpm/utils/ and issue rebuild.

7. How to create a spec file for a python library

 Inside the python package issue python setup.py bdist_rpm --spec-only to get the spec file

8. How to add new patches and upstream to existing third party package?

 Add the patch to the package folder located in $(SB_TOP)/upstream/rpm/specs//. Include the patch in spec file as well.then follow the steps in question 1.