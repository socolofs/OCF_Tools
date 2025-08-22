==================================================
Storage Routing (:mod:`ocf_tools.storage_routing`)
==================================================

.. currentmodule:: ocf_tools.storage_routing

Reservoir Class
===============

.. autosummary::
   :toctree: generated/
   
   ResRouter - A simple reservoir-routing tool

Function Tools
==============

.. autosummary::
   :toctree: generated/
   
   get_stage_discharge - Read the stage-discharge data from Excel
   get_inflow_hydrograph - Read the inflow hydrograph from Excel

ResRouter Methods
=================

.. autosummary::
   :toctree: generated/
   
   ResRouter.get_res_values - Get reservoir properties at interpolated levels
   ResRouter.route - Route the hydrograph through the reservoir
   ResRouter.check_sim - Check if the simulation data exist
   ResRouter.plot_inflow - Plot the inflow hydrograph
   ResRouter.plot_sim - Plot the inflow and outflow hydrographs
   ResRouter.plot_sim_params - Plot the full simulation state space