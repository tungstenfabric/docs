See [[Frequently Asked Questions|OpenContrail CI FAQ]].

***

December 1st, 2017 update: the Zuul v3 CI system became voting. And the unittest jobs got moved to it from Zuul v2. All changes for the master branches of all projects require "Verified +1" vote from both Zuul v2 and Zuul v3. Projects that do not run unittest jobs get an instant "Verified +1" from Zuul v3.

***

Starting November 6th, 2017, a new "Zuul v3 CI" (zuulv3) user account is adding comments on changes at the OpenContrail Gerrit site.
This new account is reporting jobs executed on a new CI stack that is going to replace the current Zuul v2 + Jenkins setup.

Currently the v3 jobs are in testing stage and are non-voting, so failures will not affect the development workflow. However, you are welcome to test out the links to job reports to get a glimpse of how it will look in the future. The CI team will gradually move CI jobs to the new v3 services, starting with master branches and the Ubuntu platform variants. All important changes in the review system will be announced on the mailing lists and Slack channels.

To learn more about the new v3 version of the Zuul CI stack, see:
- https://docs.openstack.org/infra/zuul/feature/zuulv3/
- http://inaugust.com/posts/whats-coming-zuulv3.html