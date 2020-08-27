A pipeline is a set of jobs that are run upon trigger-event (e.g. added patch or comment).
### check
All newly uploaded patchsets enter this pipeline to receive initial `Verified +1/-1` vote.
### experimental and experimental-provision
On-demand pipelines for development purposes.
### gate
This pipeline fires when the review got all the required votes, this means:
* `Code-Review +2` (and no `Code-Review -2`)
* `Approved +1`
* `Verified +1`

When the change successfully passes this pipeline, it is automatically merged by Zuul.
