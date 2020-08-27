A pipeline is a set of jobs that are run upon trigger-event (e.g. added patch or comment).
### check
All newly uploaded patchsets enter this pipeline to receive initial +1/-1 vote.
### experimental and experimental-provision
On-demand pipelines for development purposes.


Right now, we're working on splitting pipeline `check` into two pipelines - `check` and `gate`. `check` will retain its current function and purpose, while `gate` will be run after a patchset receives `Code-Review +2` and `Approved +1` votes.
