**I saw a comment from “Zuul v3 CI” user. What is it?**

The Zuul v3 CI user reports results from jobs executed on a new version of the OpenContrail CI stack. Zuul v3 is currently running unittests on the master branch for all the main projects, while the systests (integration tests) are ran on Jenkins. For a change to be fully verified, it needs a +1 vote from both CI systems - only this means that both unittests and systests completed successfully. This dual-voting setup can be considered temporary, as we plan to retire Jenkins mainline jobs entirely after finishing new Zuul v3 systest jobs.

**How do I check the status of currently running Zuulv3 jobs?**

Go to http://zuulv3.opencontrail.org/ , find your review id in the queue, click on the project name to expand the job listing. There you will see the current status (queued/running/succeeded/failed). You can click on the name of a running job to get to the console log.

**How do I check the result of a completed Zuulv3 job?**

Click on the job name, eihter in a Zuul v3 "job finished" comment or in the status table. There you can find raw job/console log ("job-output.txt.gz") and HTML-formatted step breakdown ("ara" folder). There are also other log files, depending on the job type.

**I see that my change for the master branch has a green “+1” in the “V” column in the change listing table, but it looks like it’s not verified yet. Why?**

Changes for the master branch require Verified +1 vote from both "Zuul" and "Zuul v3 CI" accounts. The green "+1" appears after the first vote, so the other one can be still missing. You can check it on the change details page. Again, this is temporary situation and Zuul (v2) will stop voting on mainline after Zuul v3 systests are implemented.

**My review has all the required labels, but it is still not merged.**

Make sure again, that the change fulfills all the requirements.

Look for the voting status area on the review page:

For master/mainline, all the votes below have to be present:
* Approved+1
* at least one Code Review +2 (and no Code Review -2)
* Verified +1 from “Zuul”
* Verified +1 from “Zuul v3 CI”

For any other branch, all the votes below have to be present:
* Approved+1
* at least one Code Review +2 (and no Code Review -2)
* Verified +1 from “Zuul”

If it is indeed the case, and the change is still not merged, ask for help on the #ci channel on Slack.

**My patchset has already passed the unittests once, but after a "recheck no bug" they are running again. Why?**

This is intended behavior, this way the code is re-tested against the current state of the target branch.
It will stay this way until we implement systests (integration testing) in Zuul v3 and enable up-to-date branch tip recheck just before the merge (gate testing).

**I have a question that is not answered here. What should I do?**

Describe your problem on the #ci channel on Slack and someone from the CI team will reach you for troubleshooting.
