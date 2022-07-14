Processes before submitting a blueprint
=======================================

1. The TSC is deciding on high level what is the use case and hardware
      or software features that will go into a specific release. Any
      blueprint that is targeting that specific release but doesn’t fit
      under the prioritized use case and features will be either
      rejected or marked as “For future release”

2. Provided the blueprint matches the release, or is submitted for TSC’s
   future consideration the BP submitter will have to consult the
   guidelines below and submit the required documentation in the 
   launchpad.

3. There will be two buckets:

   a. One for the current (say N) release

   b. A backlog which is the bucket for future releases. The TSC is
         advised to review this bucket when planning for an upcoming
         release (say release N+1).

4. There will also be a deadline, announced at the beginning of a
      release cycle (N) by which BPs targeting this release will be
      accepted. Anything submitted past that deadline will automatically
      be moved to the backlog for the upcoming releases unless the
      author appeals by email to ARB. If the ARB accepts their
      submission it will be included for this release.

5. For the accepted BPs, the ARB will have a regular meeting (bi-weekly)
      and assign reviewers to BPs. When the reviewers have read offline
      the BP they will need to invite the submitter to the ARB regular
      meeting and ask them to briefly justify their submission and
      answer any questions the ARB member will have. The reviewer who is
      assigned to that particular BP will be leading the ARB discussion
      and has power to give a +2 or -2, but it is appropriate to have
      support from the rest of the ARB members in order to do so.

Blueprint Submission
====================

Blueprint submission is a two step process.

1. Submit a blueprint providing high level overview of the feature (or
      enhancement) proposed. The blueprint is submitted
      at\ https://github.com/tungstenfabric/tf-specs/ . This
      blueprint must have a link to the full specifications of the
      feature (or enhancement).

At a minimum, the blueprint must have the following fields filled:

-  Assignee

-  Milestone Targeted

2. Submit full specification of the feature (or enhancement) in details.
      This specification must be submitted at https://github.com/tungstenfabric/tf-specs/ . 
      This specification must be submitted in Markdown format (file with .md
      extension).

EULA is necessary for submitting a spec file.

   An MD file is a text file which is created using dialects of Markdown
   language. All specification files reside
   at\ https://github.com/tungstenfabric/tf-specs/ . Full details of the feature
   must be provided in order for the feature to be considered by ARB.
   Take a look at any of the specs present at the above mentioned github
   repo and ensure that you fill in all of the fields of the spec to be
   considered. Here is an example of specification using MD file
   -\ https://github.com/tungstenfabric/tf-specs/blob/master/ironic_contrail.md

Launchpad
---------

   Please go to\ https://blueprints.launchpad.net/opencontrail\ and
   register a blueprint. The fields on the page are explained here:

   Status: This field is auto-updated

   Priority: Default for all TSC reviewed blueprints will be Medium
   until further notice

   Direction: “Approved” = TSC approved the blueprint after discussion
   on one of the weekly calls

   Definition: “Approved” = spec file merged in Gerrit, “Pending
   Approval” = at least one +1 but not merged yet, “Review” = a spec
   file exists in Gerrit

   Milestone target: Currently “5.0-featurefreeze” for all TSC approved
   blueprints. Need further discussion of whether we need additional
   milestones such as codefreeze.

   Approver: The designated member of the ARB who is responsible for
   merging the spec in Gerrit after appropriate review time

   Drafter: The author of the spec in Gerrit

   Assignee: The developer who is writing the code, probably should be
   the same as Drafter in most cases

   Series goal: Currently 5.0. This will probably always be the next
   upcoming release unless it is determined that a blueprint will miss
   the release and needs to be bumped out.

   Implementation: The assignee’s subjective opinion on how far along
   they are on writing the code (not the spec or blueprint, but the
   actual implementation code)

   Related bugs: Should be linked to a Launchpad bug because Gerrit
   automatically updates Launchpad bugs but does not automatically
   update Launchpad blueprints

Spec
----

   Specs must be submitted
   into\ https://github.com/tungstenfabric/tf-specs/ . Make sure first
   you have a Gerrit account. Once the account is in place here is the
   command line needed to do push your spec file for review:

   git clone https://github.com/tungstenfabric/tf-specs/

   cd contrail-specs/5.0

   Create the spec file here (spec filename should have a .md extension)

   Edit your spec in a text editor. Please hard wrap lines to somewhere
   around 80 characters for ease of reviewing on the Gerrit side-by-side
   diff view. Consult a markdown cheatsheet such as
   https://daringfireball.net/projects/markdown/syntax\ or similar.
   After finishing your editing, run:

   ::

     git checkout -b <your spec short name> (optional, but this will show up
     in Gerrit as "Topic" and is not a bad idea to do)

     git add <insert your spec filename here>

     git commit (write a good commit message and make sure to include a
     line "Partial-bug: #<your Launchpad bug ID>"

     git remote add gerrit ssh://<your gerrit
     username>@review.opencontrail.org:29418/Juniper/contrail-specs.git
     (this is needed once)

     git review

   If all goes well, the git review command should output a URL to
   https://review.opencontrail.org\ for your newly created spec.

Code Submission
===============

1. Initially any submitter will need to sign the appropriate CLA.

2. Submission of code patch(set) needs to be done into
      review.opencontrail.org.

   a. Patch(set) must compile cleanly. By “cleanly” we mean depending on
         which repo the patch(set) targets, some repos allow warnings
         some don’t.

   b. Unitests for that patch(set) need to have been ran successfully.

3. Together with patch(set) submission unitest code needs to be
      submitted as well with guidelines how CI can invoke those unitests
      provided the submission is about a feature.

4. For bug fixes unitests are highly desired but is not a hard
      requirement when this unitest is a complicated test (such as race
      conditions).

Test plan Submission
====================

1. Possibly for CI test plan submission we \*must\* have code +
      documentation.

2. For “individual tests” just documentation is ok although we prefer
      code to come with it.
