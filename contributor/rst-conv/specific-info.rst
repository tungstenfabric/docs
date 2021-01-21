Specific information blocks
===========================

Use special markups to emphasize specific information within your document.
Depending on specific semantic meaning of the message, you can use:

* **note** - for a message of generic meaning.

* **warning** or **important** - includes details that can be easily missed,
  but should not be ignored by a user and are valuable before proceeding.

* **caution** - delivers information that prevents a user from mistakes
  and undesirable consequences when following the procedures.

* **tip** or **seealso** - wraps extra but helpful information.

**Input**

.. code-block:: none

   .. note::

      This is the text of a note admonition.
      This line is the continuation of the first line.

      A note may contain bulleted or enumerated lists,
      as well as code blocks:

      * First option,
      * ...

**Output**

.. note::

   This is the text of a note admonition.
   This line is the continuation of the first line.

   A note may contain bulleted or enumerated lists,
   as well as code blocks:

   * First option,
   * ...

|

**Input**

.. code-block:: none

   .. warning::

      This is the text of a warning admonition.
      This line is the continuation of the first line.


**Output**

.. warning::

   This is the text of a warning admonition.
   This line is the continuation of the first line.

|

**Input**

.. code-block:: none

   .. important::

      This is the text of a important admonition.
      This line is the continuation of the first line.


**Output**

.. important::

   This is the text of a important admonition.
   This line is the continuation of the first line.

|

**Input**

.. code-block:: none

   .. caution::

      This is the text of a caution admonition.
      This line is the continuation of the first line.

**Output**

.. caution::

   This is the text of a caution admonition.
   This line is the continuation of the first line.

|

**Input**

.. code-block:: none

   .. tip::

      This is the text of a tip admonition.
      This line is the continuation of the first line.


**Output**

.. tip::

   This is the text of a tip admonition.
   This line is the continuation of the first line.

|

**Input**

.. code-block:: none

   .. seealso::

      This is the text of a seealso admonition.
      This line is the continuation of the first line.


**Output**

.. seealso::

   This is the text of a seealso admonition.
   This line is the continuation of the first line.


|

This documentation, is a derivative of `RST conventions <https://docs.openstack.org/doc-contrib-guide/rst-conv.html>`_ by OpenStack, used under CC BY. 
