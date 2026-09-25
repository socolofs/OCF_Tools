.. _ocf_tools-api:

OCF_Tools API
=============

OCF_Tools contains several different modules, each designed for a slightly different purpose.  In general, these modules are normally used by importing them separately.  For example, if you wanted to use the `ocf_tools` module, which defines channel cross-sections, computes channel flow properties, and plots backwater curves, you would use::

   >>> from ocf_tools import ocf_tools

If you wanted to use the `storage_routing` package to compute the behavior of a detension basin, you may begin your code with::

   >>> from ocf_tools import storage_routing

Each of the classes, methods, and functions defined in these modules are documented in the following sections.

API Definition
--------------

The modules currently available in OCF_Tools include the following.

* :doc:`culvert_tools`

* :doc:`ocf_tools`

* :doc:`storage_routing`

.. toctree::
   :maxdepth: 1
   :hidden:
   :titlesonly:
   
   culvert_tools <culvert_tools>
   ocf_tools <ocf_tools>
   storage_routing <storage_routing>

OCF_Tools Structure
-------------------

Each OCF_Tools module should follow the following conventions:

* Each module should be self-contained, having minimal dependencies on other
  modules within the package.

* Each module is normally organized to first present the module classes
  followed by optional functions that may be used by the classes. It is not
  normally expected that users would need to call module functions directly.
  Instead, they should create objects for the classes and interact with the
  tool through those objects.

* Occassionally, a module may call functions from an another module. This may
  be the case, for example, when heavy numerics required by the module are
  self-contained in a separate module. These external modules would normally
  be considered private, and the user should only make use of the classes
  defined in the main modules listed above.


