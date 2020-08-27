Below you can find some notes about Zuul that are not included in the official documentation.

## Job statuses
The only job status that gives a "Verified +1" vote from Zuul is the **SUCCESS** status. All other results are considered failure.

|Status name| Source of failure | Where to look for information |
|-----------|------------------|--------------------------------|
|**SKIPPED**| dependent job has failed earlier | logs of other jobs in the same buildset |
|**FAILURE**| there was an error during the main job execution. The tests failed | regular job logs on the webserver |
|**POST_FAILURE**| there was an error during additional steps after the job finished (log upload, container push etc.) | regular job logs on the webserver, or if the failure occurred during log upload: zuul-executor logs (`ze01-jnpr.o.o:/var/log/zuul/executor-debug.log`) |
|**RETRY_LIMIT**| there was an error during the job preparation phase (so-called pre-playbooks). Zuul tried to re-run the job, but if failed multiple times | regular job logs on the webserver |
|**TIMED_OUT**| the job was killed by Zuul, because it exceeded the run-time limit | regular job logs on the webserver |
|**MERGER_FAILURE**| there was an error during the source code preparation | zuul-merger logs `zuulv3.o.o:/var/log/zuul/merger-debug.log` |
|**NODE_FAILURE**| there was a problem with spawning builder VM | nodepool-launcher logs `nl02-jnpr.o.o:/var/log/nodepool/launcher-debug.log`|

## Changes not merging
Sometimes, Zuul will refuse to merge changes even if all the required votes are present. Below are 
All the information that is required to troubleshoot problems with merging resides in the zuul-scheduler logs (`zuulv3.opencontrail.org:/var/logs/zuul/debug.log`)
* there is a merge conflict
* the change depends on another change that is not yet merged
  * the dependency can be specified explicitly (by a `Depends-On:` tag in the commit message)
  * the dependency can be introduced by git tree structure - if a change is based on a parent commit that is not yet merged, the two changes will be dependent
* the project is not added to the `gate` pipeline in Zuul, so it will never begin the merging procedure
* the change has a dependent change in another project that is not a member of the same Zuul `ChangeQueue` (see https://docs.openstack.org/infra/zuul/user/config.html#attr-project.<pipeline>.queue)