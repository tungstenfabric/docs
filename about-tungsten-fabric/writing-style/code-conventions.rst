.. _code_conventions:

Code conventions
================

Follow these guidelines:

* **Use "--option ARGUMENT"**

  In technical publications, use ``--option ARGUMENT`` even if the CLI
  supports both ``--option ARGUMENT`` and ``--option=ARGUMENT``. 

* **Use capital letters with underscores for parameters**

  When you write parameters in an example command,
  use capital letters for the parameters, with underscore as a delimiter.
  For example:

  .. code-block:: console

     $ openstack user create --project PROJECT_A --password PASSWORD USERNAME

  If necessary, describe the parameters immediately after the example
  command block. For example, for the ``PASSWORD`` parameter:

  .. code-block:: none

     Replace ``PASSWORD`` with a suitable password.

|

This documentation, is a derivative of `Writing style <https://docs.openstack.org/doc-contrib-guide/writing-style.html>`_ by OpenStack, used under CC BY. 