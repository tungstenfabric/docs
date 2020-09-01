### SUCCESS
Patchset went through CI and passed the tests.
### FAILURE
Job run was unsuccessful due to a bug in the patchset.
### NODE_FAILURE
It means spawning slave node failed and job will not run.
### SKIPPED
When you see `SKIPPED` next to the job name, it means one of the previous jobs failed and was a dependency. For job dependencies, see [jobs.yaml](https://github.com/Juniper/contrail-project-config/blob/master/zuul.d/jobs.yaml).
### TIMED_OUT
It means job exceeded run time of 8 hours.
### POST_FAILURE
After a job run, our post-run tasks failed - e.g. log collection at the end of the job.
### RETRY_LIMIT
Whenever the pre-run steps fail to run three times (pre-run steps are automatically retried), Zuul 'gives up' and reports this result to Gerrit.