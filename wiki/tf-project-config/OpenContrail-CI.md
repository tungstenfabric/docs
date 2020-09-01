This document is a guide to the OpenContrail CI infrastructure. It describes the CI system for branches R5.0 upwards (R5.0, R5.1, master etc.), driven by Zuul version 3. Older branches are serviced by Zuul 2.5 as the job manager and Jenkins as the build executor.

When you create new change request on OpenContrail Gerrit (https://review.opencontrail.org), Zuul will start executing jobs. The first sign of this is a "Starting jobs" comment from the "Zuul v3 CI" account.

The status of the **currently running** jobs can be seen on the Zuul dashboard: http://zuulv3.opencontrail.org/ . Search for your change ID and click on the title to expand the list of the running jobs. Finished jobs will show their result on the list. When all the jobs from a buildset finish, it disappears from the dashboard and the results can be found in the review comments.

After the jobs finish, you will get a "Verified" comment from Zuul. It will be a "+1" if all the voting jobs succeeded or a "-1" if there was a failure. Getting a "Verified +1" vote from Zuul is one of the requirements for merging your change.

If your change got a "-1" vote, you need to inspect the logs to determine the failure. The link to the logs can be found in the "Build finished" comment or in a job table on the review page.

Log structure:
* `ara/` directory - here you can find a HTML-formatted report of the job phases. Failed phases are marked with a red X mark.
* `job-output.txt.gz` - this the full, raw output of the job. It will be automatically uncompressed and displayed in your browser. Please note, that the timestamps in front of every log line are hyperlinks - you can use them to point other people to specific places in the log.
* `zuul-info` - this directory contains various information about the job execution environment: ansible variables, dmesg log, git logs for repositories used in the build etc.
* there are also other directories, specific for particular job types (`unittest-logs`, `sanity-logs`, etc.)
 
If you believe that the job failure is not related to your change (e.g. there was some hardware glitch), you can re-run the test pipeline by placing a "recheck" comment. Every recheck will rebuild all the code from scratch, and also use the latest current target branch state.

Job-to-project assignment is defined in Zuul configuration here:
https://github.com/Juniper/contrail-project-config/blob/master/zuul.d/projects.yaml

## Job types (selected)
### Unittests
Runs Python and C++ unittests using SCons.

[Example success logs](http://logs.opencontrail.org/36/38836/3/check/contrail-vnc-build-unittest-ubuntu-trusty/6d0aa04/)

[Example failure logs](http://logs.opencontrail.org/03/39103/1/check/contrail-vnc-build-unittest-ubuntu-trusty/b5a9e8c/)

### Systests / sanity
This job stands up a Contrail cluster connected to an OpenStack installation prepared by Kolla.
It uses the microservice-based Docker deployment and is entirely CentOS 7 based.

[Example success logs](http://logs.opencontrail.org/28/39028/2/check/contrail-systest-centos74-kolla-ocata/f02d546/ara/)

[Example failure logs](http://logs.opencontrail.org/67/38967/1/check/contrail-systest-centos74-kolla-ocata/5183a60/)

### WebUI unittests

Run unittests for the `contrail-web*` projects.

[Example success logs](http://logs.opencontrail.org/09/38609/4/check/contrail-vnc-unittest-webui/1e7d733/) 

[Example failure logs](http://logs.opencontrail.org/60/38860/3/check/contrail-vnc-unittest-webui/4713975/ara/)

## CI pipelines
### Check pipeline
This is the main testing pipeline used to verify changes. It is triggered on every change/patchset submission and it also runs when you send a "recheck" comment.

### Gate pipeline
This pipeline fires when the review got all the required votes, this means:
* `Code-Review +2` (and no `Code-Review -2`)
* `Approved +1`
* `Verified +1`

When the change successfully passes this pipeline, it is automatically merged by Zuul.