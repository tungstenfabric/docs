Manual CLA Administration
=========================

At the time of the writing of this document, Tungsten Fabric is using two different Contributor License Agreement (CLA) processes depending upon the origin of the repository you're contributing to:

#. **Sign/Return a PDF**: For all repositories in the review.opencontrail.org Gerrit
#. **Online automated system**: For all repositories in the gerrit.tungsten.io Gerrit

These instructions are for how to process signed CLAs that arrive via the first process. At some point in the (hopefully near) future, these instructions will be deprecated since all of the repositories will have moved to the Gerrit hosted at gerrit.tungsten.io.

However, since the repository transition is a work in progress, we still need the procedure for processing these "manual" CLAs.

Types of CLA Administrators
---------------------------

There are two types of CLA Administrators:

#. CCLA Administrators: People who are authorized by a company to approve new contributors under their Corporate CLA.
#. ICLA Administrators: People who process any Individual CLAs that arrive. This is a superset of the CCLA Administrators plus any independent authorized individuals. The Linux Foundation staff are this type of CLA Administrator.

As implied above, CCLA admins may process ICLAs, but ICLA admins may **not** process CCLAs without express written permission by the appropriate CCLA admin. 

Which is to say: Please don't approve someone to contribute on behalf of a company you don't work for.

The cla@lists.tungsten.io Mailing List
--------------------------------

All manual CLAs arrive as messages sent to the cla@lists.tungsten.io mailing list. Because CLAs contain identifying information, membership to the mailing list is restricted to CLA Administrators.

If you are a CLA admin, please pay attention to the cla@lists.tungsten.io mailing list and help to process new CLAs as they arrive.

**We strive to process all CLAs within two work days of their arrival on the cla@lists.tungsten.io mailing list.**

Accessing the review.opencontrail.org Gerrit
--------------------------------------------

All manual CLAs are managed through the soon-to-be-deprecated Gerrit that's hosted at https://review.opencontrail.org (r.o.o).

Access to this Gerrit requires a Launchpad_ ID. If you're an admin, you already have one of these. If you're going to be a new admin, make sure you create one of these even though you'll only need it for a few months.

.. _Launchpad: http://launchpad.net

Adding Someone to a CCLA
------------------------

- Confirm the new addition has a Launchpad ID and has logged into the r.o.o Gerrit at least once.
- If the new addition has sent over a CLA document, confirm that it's complete (including an actual signature).
- Log into Gerrit at review.opencontrail.org using your Launchpad ID.
- Click 'Browse' at the top
- Click 'Groups' at the top below 'People'
- Select the CCLA-$company group for your company.
- Click 'Members'.
- Search for the new addition's email address in the search field titled `Members` and click `Add`  when they're located.
    - If you can't locate them, re-confirm that they have a Launchpad ID and have logged into Gerrit at least once.
    - Gerrit auto-saves the addition. There's no `Save` button to push.
- If the addition request was accompanied by a document of a signed CLA, save that CLA document to the `Signed CLAs`_ wiki page.
- Notify the new addition that you have finished processing their addition and that they can now commit code to review.opencontrail.org.
- If the signed CLA arrived via the cla@lists.tungsten.io mailing list, reply to the mailing list to let people know that you've processed the CLA.

.. _Signed CLAs: https://wiki.tungsten.io/display/TUN/Signed+CLAs

Removing Someone from a CCLA
----------------------------

- Log into Gerrit at review.opencontrail.org using your Launchpad ID.
- Click 'People'  at the top.
- Click 'List Groups' at the top below 'People'.
- Select the CCLA-$company group for your company.
- Click the checkmark next to the name of the person you wish to remove from your company's CCLA.
- Click `Delete`. Gerrit auto-saves the deletion. There are no more buttons to push and you're done.

Adding a New Company to the CCLA Groups
---------------------------------------

- Verify that you have a document of a CCLA in hand and that it is complete including a signature. If you don't, **DO NOT CONTINUE**.
- Log into Gerrit at review.opencontrail.org using your Launchpad ID.
- Click 'People' at the  top.
- Create an Admin group for the company.
    - Click 'Create New Group' at the top below 'People'.
    - Enter a name for the group. The name should follow the pattern `CCLA-$companyname-Admin`. If the company name contains spaces, replace them with underscores.
    - Follow the steps for "Adding Someone to a CCLA", adding the person who will be the CCLA administrator for that company.
    - If there are multiple administrators for the company, repeat the addition process as many times as necessary.
- Create a CCLA group for the company.
    - Click 'Create New Group' at the top below 'People'.
    - Enter a name for the group. The name should follow the pattern `CCLA-$companyname`. The `$companyname` used here must match the `$companyname` used to create the Admin group.
    - Search for the Admin group in the search field titled `Included Groups` and click `Add`  when its located.
    - If there are any other individuals to add to the CCLA, follow the steps for "Adding Someone to a CCLA", repeating the addition process as many times as necessary for all of the individuals who need to be added.
- Add the CCLA group to the 'CLA Accepted' group
    - Click 'List Groups' at the top below 'People'
    - Find the 'CLA Accepted' group and click on it
    - Scroll down past the Members to the 'Included Groups' 
    - Search for the new CCLA-$company group in the search field titled `Included Groups` and click `Add` when its located.
- Create a Jira Task ticket to have the new CCLA Manager(s) authorized to add documents to the `Signed CLAs wiki page`_. Assign the ticket to Casey Cain.
- Save the document to the Signed CLAs wiki page.
- Notify everyone involved that you have finished processing the CLA and that they can now commit code to review.opencontrail.org

.. _Signed CLAs wiki page: https://wiki.tungsten.io/display/TUN/Signed+CLAs

Processing an ICLA
------------------
- Follow the steps for "Adding Someone to a CCLA" but instead of CCLA-$companyname, the new addition should be added to the `ICLA-Accepted` group.
