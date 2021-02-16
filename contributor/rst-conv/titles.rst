.. _cg_titles:

Titles
======

Each RST source file has the tree structure. Define up to three heading
levels within one file using the following non-alphanumeric characters:

* **Heading 1** - underline with equal signs;

  * **Heading 2** - underline with dashes;

    * **Heading 3** - underline with tildes.

When it's a first Heading in a file it should be folowed by a `:Date:` directive with a date of last major update (or creation). 
The date should be also updated when an old document is positively verified for being up-to-date.

**Input**

.. code::

   Heading 1
   =========

   :Date: 2020-01-01

   Body of the first level section that includes general overview
   of the subject to be covered by the whole section.
   Can include several focused Heading-2-sections.
   When it's a first Heading in a file it should be folowed by a :Date: directive with a date of last major update (or creation). 
   The date should be also updated when an old document is positively verified for being up-to-date.

   Heading 2
   ---------

   Body of the second level section that gives detailed explanation of one
   of the aspects of the subject. Can include several Heading-3-sections.

   Within user guides, it is mostly used to entitle a procedure with a set
   of actions targeted at a single task performance.
   For example, "Associate floating IP addresses".

   Heading 3
   ~~~~~~~~~

   Body of the third level section.
   It includes very specific content, and occurs mainly in guides containing
   technical information for advanced users.

.. note::

   Underlines should be of the same length
   as that of the heading text.

   Avoid using lower heading levels by rewriting and reorganizing the
   information.


|

This documentation, is a derivative of `RST conventions <https://docs.openstack.org/doc-contrib-guide/rst-conv.html>`_ by OpenStack, used under CC BY. 