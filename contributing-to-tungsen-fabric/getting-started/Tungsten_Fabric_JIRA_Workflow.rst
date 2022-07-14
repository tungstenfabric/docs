Tungsten Fabric JIRA workflow
=============================

This Document provides guidance for the current  JIRA workflow for Tungsten
Fabric utilizing various constructs available as part of Jira.

Basic definitions:

JIRA Projects:

-  TF Blueprints - captures details on blueprints for all new features
      that needs to be added to Tungsten Fabric

-  TF Bugs - captures all workflow other than blueprints

JIRA Issue Type:

-  Epic - Capture large user stories which can be broken down into
      smaller user stories and used to bundle/group new features
      (BluePrints) together in one place.

-  Story (Not available for TF Bugs) - Capture user stories

-  New Feature - introduction of new feature into Tungsten fabric

-  Bug - default bucket for any issue that does not fall into the
      category of improvement or a new feature

-  Improvement - ticket to track an improvement on already available
      functionality

-  Task - a work unit defined to carry out an activity

Affects Version:

-  Blueprint :- represents which version this blueprint is proposed for

-  Issue :- represents which version have this issue reported for

Fix Versions:

Version for which this Blueprint or fix for issue will be part of

*Current Workflow:*

While proposing a new feature

-  File a User Story under TF-Blueprint project for review, assignee
      will be submitting a blueprint/spec using this User Story for
      community review

   -  For larger activities an Epic needs to be created, which will be
         broken down into separate user stories for Blueprint

-  As part of the approval of a Blueprint, a milestone version will be
      attached to it to represent the targeted Release version

-  Upon approval, the assignee will create (new feature / improvement) issue
      under TF Bugs project to submit the changes to code repositories

-  Link these new feature / improvement issues to the approved blueprint
      user story

-  Follow the individual issue work flow on individual issues.

.. image:: images/jira_workflow.png
