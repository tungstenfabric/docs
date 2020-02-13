================================
How to review a patch in Gerrit
================================

Patch review is an essential process of any contribution workflow.

Any patch must undergo review by others before it gets committed.

**Who can review:**  After creating a developer account in Gerrit, anyone can comment and express their opinions and approvals. But only a small group of people in Gerrit will be given the authority to approve code and merge it into Gerrit repository. 

1. Basic Terminologies 
======================

* **Change:** A unit of review. Every git commit has a change-Id associated with it.

* **Patch set:** A revision of a change. The first revision is patch set 1.

* **Label:** A rating category that allows or blocks progress of a change

* **Score:** The rating given to a label. For some labels, its range is +1/-1 that allows or blocks. Code review spans +2 to -2.
           
* **Abandon:** Archives a change that can be restored later.

* **Project:** A Git repository

2. Fundamental Steps to review
==============================

#. Use Linux Foundation user credentials to login.
   Gerrit UI login: https://gerrit.tungsten.io/r/login/%2F%2Fq%2Fstatus%3Aopen
#. Under **Your**-> **Changes** :

   **Incoming reviews:** Someone made a change and they want you to review.
   
   **Outgoing reviews:**  You made a change and submitted for review to someone.
#. By clicking on **ADD REVIEWER** under Reviewers section on the left side panel, 
   you can add reviewers for a particular patch. Reviewer immediately gets email notifications. 
   We can have multiple reviewers assigned. For example, if reviewer 1 gave +1 score and the 
   second reviewer gave +1 score, it does not mean +2. In order to get merged, +2 is needed.
   
   Scoring system has these values: **-2,-1,0,+1,+2**
   ::   

    -2 This shall not be merged

    -1 I would prefer this is not merged as it is

    0  No score

    +1 Looks good to me, but someone else must approve

    +2 Looks good to me, approved
   
    Note: +2/-2 scores are only for "core" contributors, but anyone with a login can review and give +1/-1 to any patch.
#. Go to **File** section at the bottom, click on the file name and add comments. You can add comment line by line or to the entire file.

2.1 Inline Comments 
--------------------

Inline comments are displayed directly in the patch file under the code that is commented. 
Inline comments can be placed on lines or on code blocks.
If an inline comment relates to a code block, this code block is highlighted by a yellow background.

Follow the following steps to leave your review comments inline: 

a. You can set the **Diff view** on the right hand side to either **Side-by-side diff** or **Unified-diff** view. The side-by-side diff screen shows a single patch; the old file version is displayed on the left side of the screen; the new file version is displayed on the right side of the screen. This screen allows to review a patch and to comment on it.
b. To add a new inline comment, select a code block or a line and press **c** from keyboard. Alternatively, you can also click on the line number for adding comments.
c. For typing your comments inline, a new comment box is displayed under the code block or the line that you selected.
d. Type your comment in the comment box.
e. Clicking on the **Save** button saves the new comment as a draft. To make it visible to other users it must be published from the change screen by replying (click on the **Reply** button) to the change.
f. Clicking on the **Discard** button deletes the new comment.
g. If you have selected **side-by-side diff** view, file-level comments can also be applied by clicking on the File button displayed in the header.

2.2. Adding Review Score
-------------------------

a. Click on the **Reply** button in the main page. For example: https://gerrit.tungsten.io/r/c/tungstenfabric/docs/+/351.
b. Add your score. In order to pass, the final reviewer must give +2 score.

2.3 Submitting the Patch
--------------------------

a. Click Submit button if ready to merge.
b. Criteria to submit: The final score must be +2. History is displayed under Change log. Comment threads display reviewer comments.

3 Searching for changes with pending edits
==========================================

To find changes with pending edits: Select **Your** < **Changes** from the Gerrit dashboard.

All the changes are listed here, according to works in progress, outgoing reviews, incoming reviews, and so on.





