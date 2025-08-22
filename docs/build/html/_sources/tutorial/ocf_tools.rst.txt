Open Channel Tools (:mod:`ocf_tools.ocf_tools`)
===============================================

.. currentmodule:: ocf_tools.ocf_tools

.. contents::

The OCF Tools package includes modules to perform several different types of
analysis associated with open channel hydraulics:

* The ``ocf_tools`` module is the main module for defining channel cross
  sections and computing water depths.

* The ``culvert_tools`` module is an experimental module for computing
  controls and water levels in culverts.

* The ``weir_tools`` module provides functions for standard weir equations to
  compute flow rate from head over the weir.

* The ``storage_routing`` module allows for computing the storage equation
  and outflow from detention basins.

The following sections document the main steps involved in using each of
these modules. At the present time, only the ``ocf_tools`` and ``weir_tools``
modules are included. You may read the source code for the other modules or
check back later when more of the documentation is complete.


.. _tutorial_ocf:

Using the ``ocf_tools`` Module
==============================

The ``ocf_tools`` module includes two main classes for handling open channel
hydraulics calculations: cross-section classes and an ``OpenChannel`` class.
Calculations usually involve creating a cross-section object, passing that
object to the ``OpenChannel`` class, and then using the various object
methods to make standard calculations. The following example is for a
trapezoidal cross-section, which uses the ``TrapSection`` class. Other
section types have there own classes, with the input data required to create
those objects described in the ref:`API Reference ./reference/index`.

Creating a Cross-Section Object
-------------------------------

We will create a trapezoidal section with side slopes of 3 units horizontal
to 1 unit vertical, a bottom width of 15 m, Manning's *n* value of 0.015 in
the main channel, and an optional different Manning's *n* value ov 0.025 for
the side slopes. The unit system should be specified as `0` for U.S.
Customary Units or `1` for SI units::

    from ocf_tools import ocf_tools
    trap_sec = ocf_tools.TrapSection(3., 15. 0.015, ns=0.025, units=1)

We can use this new `trap_sec` object to do most calculations that depend on
a known water depth and discharge. Consider a case of a flow of 2.5 cubic
meters per second and water depth of 1.2 m. Then, we can compute several
relevant quantities as follows.

To compute the flow velocity and Froude number::

    y = 1.2
    Q = 2.5
    v = trap_sec.velocity(y, Q)
    Fr = trap_sec.froude_number(y, Q)

Notice that we do not need to enter the unit system or any of the channel
geometry with these calculations. Those data are stored in the object itself.
We can also calculate the specific energy and momentum function as follows::

    E = trap_sec.specific_energy(y, Q)
    M = trap_sec.momentum_function(y, Q)

We could also directly compute the flow cross-sectional area or centroid
depth with::

    A = trap_sec.area(y)
    y_centroid = trap_sec.centroid_depth(y)
    
Or, the wetted perimeter and top width as::

    P = trap_sec.wetted_perimeter(y)
    B = trap_sec.top_width(y)

You can find documentation for all available ``Section`` methods in the
ref:`API Reference ./reference/index`

Using the ``OpenChannel`` Class
-------------------------------

Often times in open channel hydraulics problems, we know the discharge, but not the water depth.  In those cases, there normally needs to be some kind of iteration, either to solve the implicit Manning's equation, or to find a water depth that matches a given specific energy or momentum function.  These calculations, along with computation of backwater profiles, are handled by the ``OpenChannel`` class.  

We can create an ``OpenChannel`` object by passing a ``Section`` object as input.  Note that this will tell the ``OpenChannel`` object what unit system you are using, so do not try to change unit systems. 

We will start by creating a `canal` object using our trapezoidal section created above::

    canal = ocf_tools.OpenChannel(trap_sec)

You can pass any ``Section`` object as input; this module assumes the channel is prismatic, with the same cross-section geometry along the whole length of the channel.

We can find the critical depth, which involves interating to set the Froude number to 1.  We pass the discharge and an initial guess for the critical depth.  The method returns the correct value::

    yc = canal.critical_depth(Q, 0.5)

We can check the result, by calling the Froude number method of the cross-section object::

    Fr = trap_sec.Froude_number(yc, Q)

We can also compute the normal depth given the discharge.  Unlike for the critical depth, we now need to include the channel slope.  The calculations are as follows::

    S = 0.0005
    yn = canal.normal_depth(Q, S, 1.0)
    
Here, `S` is the channel slope and `1.0` is an initial guess for the normal depth.  If either of these methods (critical depth or normal depth) return the initial guess as the answer, the most likely outcome is that the iteration search did not find a solution.  Always check the output from these functions to ensure the results are the correct answers.  We can check the normal depth by computing the discharge by Manning's equation and comparing it to the given discharge::

   Qn = canal.manning_flow(yn, S)
   
If the calculation found the correct normal depth `yn`, then the normal flow `Qn` should match our design discharge `Q`.

In the case of a hydraulic jump, the momentum function remains constant through the jump.  The sequent depth is the depth on the other side of the hydraulic jump.  Because the Froude number goes through 1.0 in the jump, the `sequent_depth` method is able to compute either upstream or downstream sequent depths by first interrogating the Froude number of the given input depth.  For example, if we had a hydraulic jump in this channel with a downstream depth of 2.3 m, the upstream sequent depth of the super-critical inflow would be computed as follows::

    y1 = canal.sequent_depth(Q, 2.3)
    
These are the main methods that compute local channel properties.

Computing Gradually Varied Flow Profiles
----------------------------------------

``OpenChannel`` objects can also compute gradually-varied flow profiles.  Several methods are involved in the calculation:

* The `profile` method is normally called first to compute a gradually varied flow profile.  This stores the numerical table of data for use by subsequent methods.

* The `plot_profile` method will plot the currently stored gradually varied flow profile.

* To see the computed values, you may use the `get_profile_table` method to obtain a string header describing the data and a Numpy array of corresponding computed values.

* You may save the computed values directly to a space-delimited file, using the `save_profile_table` method.

* The `profile_type` method is used by the `profile` method to decide what type of profile to plot.  This method is not usually called directly by the user.

We can compute an example as follows.  Let us assume the flow in our trapezoidal channel is sub-critical, with a downstream control that sets the water depth to 3.3 m.  We will compute the water depths at locations upstream of this downstream control.  To do that, we need to specify the following values:

* `x0`:  The numerical value for the x-coordinate at the downstream control.  This could be zero or a known survey station value.

* `y0`:  The water depth at the control, here 3.3 m.

* `Q`:  The design discharge, here 2.5 cubic meters per second.

* `S`:  The channel slope, assumed constant throughout the profile.  Here, we will use 0.0005

* `control_section`:  a flag indicating where the control is located.  Use `1` for a downstream control or `0` for an upstream control.  Be sure to use upstream control on any steep slope.

* `delta_x`:  This is the maximum step size the solver will be allowed to take between computed values along the profile.  The solver is an adaptive step-size solver, so it may take smaller steps when needed.  Use this to produce smooth output when plotting the profile.

* `max_x`:  Use this optional parameter to specify how far away from the control the profile should be computed.  If set to `None`, the solver will solve until the profile is within 0.1 percent of normal depth.

The return values from the `profile` method are the *x* and *y* coordinates of each point along the profile water surface elevation.  

We can solve for the profile in our canal and plot the result as follows::

    x0 = 0.
    y0 = 3.3
    x, y = canal.profile(x0, y0, Q, S, control_section=1, delta_x=100.)
    canal.plot_profile(fig=1, label='Canal Profile')

We can save the results of the profile calculation using::

    fname = 'canal_profile.txt'
    canal.save_profile_table(fname)
    
These are the main steps in using `ocf_tools` to compute flow profiles.

Using the ``weir_tools`` Module
===============================

The weir-tools module contains two functions:  one for sharp-crested weirs and the other for broad-crested weirs.  These functions take a minimized array of inputs (e.g., height on the weir, weir height, and unit system) and return the discharge over the weir.  

Sharp-crested Weirs
-------------------

The sharp-crested weir function computes equation (2.39) from Sturm [Sturm]_ with updated values for the *C_d* coefficient based on the paper by [Pugh]_.  The input parameters are:

* `H`: The height of the water above the weir crest.

* `P`: The height of the weir, from the channel bottom to the weir crest.

* `L`: The length of the weir.  This function only considers supressed weirs, so this length should always match the channel top width.

* `units`:  A flag indicating the unit system:  use `0` for U.S. Customary Units or `1` for SI units.

We can compute an example as follows::

    from ocf_tools import weir_tools
    H = 1.2     # head on weir in feet
    P = 6.
    L = 18.
    units=0
    Q = weir_tools.sharp_crested_weir(H, P, L, units=units)

Broad-crested Weirs
-------------------

This function computes equation (2.47) in [Sturm]_ for a broad-crested weir.  This function only implements *C_d* = 0.848, which is the truly broad-crested weir case.  The function checks to make sure the broad-crested weir criteria are met and returns an error message when one of the dimensions is wrong.  The input parameters are:

* `H`: The height of the water above the weir crest.

* `P`: The height of the weir, from the channel bottom to the weir crest.

* `L`: The length of the weir.  This function only considers supressed weirs, so this length should always match the channel top width.

* `l`: The length of the weir in the flow direction.

* `units`:  A flag indicating the unit system:  use `0` for U.S. Customary Units or `1` for SI units.

We can compute the same example as above, just changing to a broad-crested weir, as follows::

    l = 10.
    Q = weir_tools.broad_crested_weir(H, P, L, l, units=units)

Note that the broad-crested weir function does iterate to find the correct value of the energy loss coefficient *C_v*.


References
==========

.. include:: ../_references
