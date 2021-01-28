References
==========

Cross-references
~~~~~~~~~~~~~~~~

To cross-reference to arbitrary locations within one document,
use the ``ref`` role.
Reference target names need to start with an underscore.
For example, ``.. _example:``. However, the reference itself should not
have the underscore preceding the reference. For example, ``example``.
For more information on referencing, see `Internal Hyperlink Targets
<http://docutils.sourceforge.net/docs/user/rst/quickref.html#internal-hyperlink-targets>`_.


**Input**

.. code-block:: none

   .. _cg_titles:

   Titles
   ~~~~~~

   This is the section we want to reference to.

   ...

   The following - :ref:`cg_titles` - generates a link to the section with
   the defined label using this section heading as a link title.

   A link label and a reference can be defined in separate source files,
   but within one directory. Otherwise, use the external linking.

**Output**

...

The following - :ref:`cg_titles` - generates a link to the section with
the defined label using this section heading as a link title.

A link label and a reference can be defined in separate source files,
but within one directory. Otherwise, use the external linking.

Reference works only if it points to heading or section. For making link to
any location you must give your reference an explicit title, using this syntax: ``:ref:`Link title <label-name>`.``

**Input**

.. code-block:: none

  .. _label used in referencing file:

  **Input**

  This is the section we want to reference to.

  ...

  Here is a link to :ref:`that label located in another file 
  <label used in referencing file>`.  

**Output**

Here is a link to :ref:`that label located in another file 
<label used in referencing file>`.  


External references
~~~~~~~~~~~~~~~~~~~

To link to some external locations, format the RST source as follows:

* Do not apply any markups to specify a web link.

* If you need a specific link title to appear in the output,
  format a web link as ``Link text <http://web-link.com>``
  wrapping it in backticks.

* Do not separate the link name from the link itself by defining the link in
  another place in your document. It prevents translated documents from using
  different links, for example, corresponding links to translated versions.

**Input**

.. code-block:: none

   Here is a link to the Linux Foundation home page: https://www.linuxfoundation.org.

   Here is an external web link with a link title:
  `Linux Foundation <https://www.linuxfoundation.org>`_.

**Output**

Here is a link to the Linux Foundation home page: https://www.linuxfoundation.org.

Here is an external web link with a link title:
`Linux Foundation <https://www.linuxfoundation.org>`_.

Links
~~~~~

In some cases same locations might be mentioned many times in the same document. 
Instead of embeding URI inline each time use links. All hyperlink target should be put at the end of the file.

**Input**

.. code-block:: none

  Here is a link to `Signed CLAs wiki page`_.
  And here is another paragraph with a link to the same `Signed CLAs wiki page`_.

  .. _Signed CLAs wiki page: https://wiki.tungsten.io/display/TUN/Signed+CLAs

**Output**

Here is a link to `Signed CLAs wiki page`_.
And here is another paragraph with a link to the same `Signed CLAs wiki page`_.

.. _Signed CLAs wiki page: https://wiki.tungsten.io/display/TUN/Signed+CLAs

|

This documentation, is a derivative of `RST conventions <https://docs.openstack.org/doc-contrib-guide/rst-conv.html>`_ by OpenStack, used under CC BY. 