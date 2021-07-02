Contrail Project Overview
-------------------------

OpenContrail is community supported Apache project to provide network virtualization functionality on Openstack and other orchestration systems. Currently, this is primarily supported on Openstack. The code is available publically on GitHub and project is hosted on launchpad.
This document is meant to be the overview of the project to developers and users new to the community.

This document covers following topics:

* Launchpad projects: OpenContrail vs Contrail Cloud (previously called JuniperOpenstack)
* Project Management
* Developer resources.
* FAQs

- - -

#### OpenContrail vs Contrail Cloud/Contrail Networking ####

OpenContrail provides virtual network functionality based on open protocols and Rest APIs. OpenContrail and Contrail Networking is identical in feature set. OpenContrail is freely available on Launchpad. Contrail Networking and Contrail Cloud is commercial supported product from Juniper. Contrail Networking consists of following major components (aka roles): 

* Virtual Network Controller (VNC): SDN controller based on BGP/L3VPN.
* Configuration Node: Manages contrail configuration and exposes north bound REST APIs (VNC API). Neutron v2 APIs are also supported.
* vRouter: Implements dataplane forwarding LKM and user space 'Agent' to manage forwarding.
* Analytics: Collects logs, statistics, flow data from all nodes. These data can be queried via REST APIs.
* UI: Contrail UI implements configuration and monitoring system based on standard APIs supported by Configuration and Analytics node.

OpenContrail can be integrated with Openstack and other orchestration systems. Currently this is actively maintained for Openstack. Beta level support is available for Cloudstack.

Contrail Cloud is a distribution of OpenStack by Juniper that is used by Juniper Private Cloud, Juniper's NFV Solution for Service Provider Market. In addition to Contrail networking this includes following components:

* Block and Object storage.
* Installation, provisioning and monitoring of cluster.
* Contrail extension to openstack componenets such as Horizon, Neutron Client etc.
* High availability for Openstack.
* Other features to ease the deployment and operation of cloud.

Contrail Cloud is based on Ubuntu cloud archive openstack packages with fixes/extension as needed. Its bundled with all the dependent packages and installation scripts. Note that Ubuntu Cloud archive has additonal openstack packages which may not be qualified for Contrail Cloud and so will not be part of the release. That does not mean those package cannot be installed on top of Juniper's distribution.

At this time, CentOS and its variant are not distributed as part of Contrail Cloud. These are available as Contrail networking product, with the expectation that it will be integrated with third party openstack distributions. More specifically, components that are part of Contrail Cloud (eg. storage, Openstack HA, and Server Manager) are not supported for CentOS target. Having said that we maintain exact feature and performance parity on CentOS wrt Contrail networking features.

More details on the release content of Contrail Cloud can be found at [http://techwiki.juniper.net](http://techwiki.juniper.net/Documentation/Contrail).

- - -

#### Developer Resources ####

###### Code Repositories: ######
Entire Contrail code, test scripts and features available as part of Contrail Cloud are available in public at [GitHub](https://github.com/Juniper?query=). The developers are recommended to use android repo tool to create the development environment. The manifest files for OpenContrail is published at https://github.com/Juniper/contrail-vnc. For more information on building the OpenContrail packages refer to this [document](http://juniper.github.io/contrail-vnc/README.html).

Note: All the code is distributed with Apache 2.0 license.

###### Submitting patches ######

Developers can upstream their patches via OpenContrail CI process. The tools and workflow is similar to that in Openstack project. To get started:

1. Sign the [contributor agreement](https://na2.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=cf81ffe2-5694-4ad8-9d92-334fc57a8a7c)
2. Create a Launchpad ID

After that one can submit the patch to [review.opencontrail.org](https://review.opencontrail.org) by following the [CI document](https://github.com/Juniper/contrail-controller/wiki/OpenContrail-Continuous-Integration-(CI)). The CI tool enables code review and runs test script. After passing these steps code will be merged automatically to mainline.

For any new feature commit, a blueprint must be submitted and reviewed for the same. These blueprints must be committed into 'specs' directory of the respective repo. Most of the blueprints of the project will reside [here](https://github.com/Juniper/contrail-controller/tree/master/specs) in contrail-controller repo. Blueprint must follow this [template](https://github.com/Juniper/contrail-controller/blob/master/specs/blueprint_template.md).


###### Guidelines for Commit Logs ######

These are based on [Gerrit commit guidelines](https://wiki.openstack.org/wiki/Gerrit_Workflow#Committing_Changes)

1. Start commit message with a short (~50 characters) 1-line summary paragraph i.e. a single very brief line (no period at end) followed by a blank line. Rest of the commit log can be zero or more paragraphs. Each line within a paragraph should be <= 72 characters.

2. Include a launchpad bug number by adding a Closes-Bug: #NNNNNN line somewhere in the commit message, typically just before/after the Change-Id line.  Other useful keywords are Partial-Bug and Related-Bug.  Using these keywords provides really nice integration between launchpad and github.  The review contains a link to the bug and the bug activity log is automatically updated with detailed review information.  Further, the status of the bug gets updated to "Fix committed" when Closes-Bug is used.

* Closes-Bug: #1234567 -- use 'Closes-Bug' if the commit is intended to fully fix and close the bug being referenced
* Partial-Bug: #1234567 -- use 'Partial-Bug' if the commit is only a partial fix and more work is needed
* Related-Bug: #1234567 -- use 'Related-Bug' if the commit is merely related to the referenced bug

The # is optional but be sure to add a space after the colon - the integration doesn't work otherwise.
A single commit should not normally be used to fix unrelated bugs.  In cases where a single commit does address multiple (related) bugs, one of the above keywords must be used for each bug.

Note that when you mention Partial-Bug/Closes-Bug in the review request for a series, only that particular series which the bug is fixed for will get updated to "In Progress"/"Fix committed". If the bug doesn't have the series in question, it doesn't get updated.


###### Documentation ######

Here are the pointers to Contrail documents:
* Contrail architecture document is at [http://opencontrail.org/ebook/](http://opencontrail.org/ebook/)
* Contrail Cloud / Contrail Networking user guide & release notes are hosted on [techwiki](http://techwiki.juniper.net/Documentation/Contrail)
* Developer contributed wiki on Contrail internals, installations etc are hosted on [GitHub](https://github.com/Juniper/contrail-controller/wiki)
* Community contributed blogs on Contrail features & capabilities are at [http://opencontrail.org/blog/](http://opencontrail.org/blog/)
* Blueprints are contributed in GitHub in .md format in spec dir of respective code repos as indicated above. Follow this [template](https://github.com/Juniper/contrail-controller/blob/master/specs/blueprint_template.md).

###### Support ######
To get support on Contrail, join the mailing list as indicated in [http://www.opencontrail.org/developer-resources/](http://www.opencontrail.org/developer-resources/)

- - -

#### Project Management ####

###### Official releases: ######
Contrail Cloud follows continuous integration development model. The project schedules a major and minor release every 2-4 months. The schedule and branch information for the project are maintained on [launchpad](https://launchpad.net/juniperopenstack). The top level branch diagram shows the current 'milestone' and 'series' active on the project. 

Contrail releases are done via internal build process. Official releases are done from the public throttle branches after the internal test cycle is done. All the development is in public but the Juniper's release is done after internal test process to harden the end product. We do not tag the exact version publicly on git on which a release was cut, as Juniper's product decisions are managed independent of OpenContrail. Release numbering follows 4 digit scheme, **a.b.c.d**. 'a' corresponds to yearly LTS release. 'b' represents the major release done 3-4 times in a year. Minor releases are represented by 'c' where small enhancements are done as needed. In some cases patch release (denoted by digit 'd') could be done for critical blocker issues on any minor or major releases. All LTS and major releases are done on its own throttle branch. Minor releases are done on the corresponding throttle branches. (Note that before 3.0 release, the numbering scheme did not have the period between 'b' and 'c', e.g., 2.21.1. From 3.0 onwards the 4 tuple will be separated by a period. e.g., 3.1.1.0)

Contrail packages are available on OpenContrail launchpad PPA as stable opencontrail packages [here](https://launchpad.net/~opencontrail/+archive/ubuntu/ppa).  Periodically a working version is uploaded from mainline at snapshot area [here](https://launchpad.net/~opencontrail/+archive/ubuntu/snapshots). The installation instruction for OpenContrail packages can be found on this [wiki](https://github.com/Juniper/contrail-controller/wiki/OpenContrail-bring-up-and-provisioning). These packages are community supoprted via mailing lists as indicated above. 

###### Bug tracking: ######
Bug tracking on this project is done publicly on Launchpad. Two Launchpad IDs (aka projects) are maintained for this project, [Contrail Cloud](https://launchpad.net/juniperopenstack) and [OpenContrail](https://launchpad.net/opencontrail). Bugs found during internal testing of Contrail Cloud/Contrail Network, are tracked at JuniperOpenstack project. All the bugs are made public, unless they have proprietary customer information. By default only Juniper Engineering team can create issues on this project. Anyone can add his/her ID to track a particular bug(s). Launchpad will generate email update for any change on these bugs.

'OpenContrail' project account is meant to track community reported bugs. By default these bugs are public. No special privilege is needed to create a bug on this project. Optionally user can cross link these public bugs to make it dependent on JuniperOpenstack project and vice versa.

There is no restriction w.r.t code commit against bugs on any of these 2 launchpad projects.

Details for bug management is described [here](https://github.com/Juniper/contrail-controller/wiki/Bug-management).

- - -

#### FAQs ####

1. Do we have all code distributed as part of Contrail Cloud available in public?

	Yes, including test suites. Juniper developers also develop on the opensource repos like any other developer in the community.
    
2. What tests do you run before code gets merged via Contrail CI?

   Contrail CI is evolving continuously. Currently it does build for CentOS, Ubuntu 12.04 & 14.04. It runs Unit tests on those builds. Then it installs Contrail Cloud and runs few basic tests covering basic functionality around Virtual network, policies and packet forwarding. For more detail refer to this [document](https://github.com/Juniper/contrail-controller/wiki/OpenContrail-Continuous-Integration-(CI)).

3. I am an application developer. Where can I find documentation on Contrail APIs?

   Contrail API documentation is maintained with the code. They can be found after installation of Contrail at http://<config-node-ip>:8082/documentation/index.html. Analytics API are at http://<analytics-node-ip>:8083/documentation/index.html.
   
4. Why is 'xyz' feature supported on Ubuntu but not on CentOS?

   In general all contrail networking feature are supported on both platforms. Some of features specific to Contrail Cloud distribution are only qualified on Ubuntu. This is mainly to reduce the test matrix. The missing features can be integrated on CentOS as well starting from Open Source code. An example of such feature is 'Openstack HA'.
   
5. Why did Juniper chose Ubuntu as opposed to CentOS for Contrail Cloud?

   This is mainly because CentOS kernel version for long time was quite old. After CentOS 7.0 is out this concern is no longer there. So, depending on interest, Contrail Cloud could be productized on CentOS as well. 
   
6. Why does Juniper distribute OpenStack packages with Contrail Cloud on CentOS too?

	For CentOS we distribute minimal working openstack pakcages so CentOS version of Contrail could be deployed for POCs. CentOS customers should deploy only the 'Contrail' packages from the bundle. 

6. What are high level content of Contrail Cloud distribution. How can I get those?

	Contrail Cloud distribution is available from Juniper. If you are interested in evaluation, pl get in touch with the support team. The bundle includes provisioning scripts, contrail and openstack packages qualified by Juniper. Also, all the dependent package to install these on base OS version (CentOS or Ubuntu) is included. For more details on installation please refer to [http://techwiki.juniper.net](http://techwiki.juniper.net/Documentation/Contrail).
    
7. Can I only deploy Contrail packages from Contrail cloud bundle?

     Yes, abosoltely. Many of our customer have live deployment on Contrail packages. Customers are free to chose alternate solutions/sources for non networking features included in Contrail Cloud.

8. Do you support devstack?

      Yes. To install devstack follow the guide [here](https://github.com/Juniper/contrail-installer/blob/master/README.md).

9. How closely do you track Upstream Openstack?

      We support upstream Openstack on Contrail Cloud release within 6 weeks of upstream release. Contrail networking support is released earlier as beta for customers who want to integrate Contrail with latest openstack sooner.
