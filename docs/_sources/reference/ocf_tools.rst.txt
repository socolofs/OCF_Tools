====================================================
Open Channel Flow Tools (:mod:`ocf_tools.ocf_tools`)
====================================================

.. currentmodule:: ocf_tools.ocf_tools

Cross-section Classes
=====================

.. autosummary::
   :toctree: generated/
   
   Section - Base cross-section class and rectangular cross-section
   TrapSection - Trapezoidal cross-section class
   TriangularSection - Triangular cross-section class
   CircularSection - Circular cross-section class
   ParabolicSection - Parabolic cross-section class

Open Channel Class
==================

.. autosummary::
   :toctree: generated/
   
   OpenChannel - Class for computing open-channel hydraulic properties and flow
   
Open Channel Methods
====================

.. autosummary::
   :toctree: generated/
   
   OpenChannel.critical_depth - Critical depth given flow rate
   OpenChannel.normal_depth - Normal depth given flow rate and slope
   OpenChannel.manning_flow - Flow rate from Manning's equation given depth and slope
   OpenChannel.profile_type - Profile type (M1, M2, S1, etc) given depth at a control point, flow rate, and slope
   OpenChannel.profile - Commpute a gradually varied flow profile given depth at a control point, flow rate, and slope
   OpenChannel.plot_profile - Plot a gradually varied flow profile
   OpenChannel.get_profile_table - Create a table of data for a gradually varied flow profile
   OpenChannel.save_profile_table - Save a gradually varied profile dataset to a text file

Cross-section Methods
=====================

Each of the Section classes defined above have the same set of methods and the same interface to these methods.  Here, we link to the documentation for the base Section class, which also defines a rectangular section:

.. autosummary::
   :toctree: generated/
   
   Section.area - Cross-sectional area given depth
   Section.wetted_perimeter - Wetted perimeter given depth
   Section.top_width - Top width given depth
   Section.centroid_depth - centroid_depth given total depth
   Section.ne - effective Manning's coefficient given depth
   Section.hydraulic_radius - hydraulic radius given depth
   Section.froude_number - Froude number given depth and flow rate
   Section.velocity - velocity given depth and flow rate
   Section.specific_energy - specific energy given depth and flow rate
   Section.momentum_function - momentum function given depth and flow rate
   Section.print_geometry - a table of geometry data relevant to the present section object
   
Methods for each of the remaining Section classes are linked below:

.. autosummary::
   :toctree: generated/
   
   TrapSection.area - Cross-sectional area given depth
   TrapSection.wetted_perimeter - Wetted perimeter given depth
   TrapSection.top_width - Top width given depth
   TrapSection.centroid_depth - centroid_depth given total depth
   TrapSection.ne - effective Manning's coefficient given depth
   TrapSection.hydraulic_radius - hydraulic radius given depth
   TrapSection.froude_number - Froude number given depth and flow rate
   TrapSection.velocity - velocity given depth and flow rate
   TrapSection.specific_energy - specific energy given depth and flow rate
   TrapSection.momentum_function - momentum function given depth and flow rate
   TrapSection.print_geometry - a table of geometry data relevant to the present section object
   TriangularSection.area - Cross-sectional area given depth
   TriangularSection.wetted_perimeter - Wetted perimeter given depth
   TriangularSection.top_width - Top width given depth
   TriangularSection.centroid_depth - centroid_depth given total depth
   TriangularSection.ne - effective Manning's coefficient given depth
   TriangularSection.hydraulic_radius - hydraulic radius given depth
   TriangularSection.froude_number - Froude number given depth and flow rate
   TriangularSection.velocity - velocity given depth and flow rate
   TriangularSection.specific_energy - specific energy given depth and flow rate
   TriangularSection.momentum_function - momentum function given depth and flow rate
   TriangularSection.print_geometry - a table of geometry data relevant to the present section object
   CircularSection.area - Cross-sectional area given depth
   CircularSection.wetted_perimeter - Wetted perimeter given depth
   CircularSection.top_width - Top width given depth
   CircularSection.centroid_depth - centroid_depth given total depth
   CircularSection.ne - effective Manning's coefficient given depth
   CircularSection.hydraulic_radius - hydraulic radius given depth
   CircularSection.froude_number - Froude number given depth and flow rate
   CircularSection.velocity - velocity given depth and flow rate
   CircularSection.specific_energy - specific energy given depth and flow rate
   CircularSection.momentum_function - momentum function given depth and flow rate
   CircularSection.print_geometry - a table of geometry data relevant to the present section object
   ParabolicSection.area - Cross-sectional area given depth
   ParabolicSection.wetted_perimeter - Wetted perimeter given depth
   ParabolicSection.top_width - Top width given depth
   ParabolicSection.centroid_depth - centroid_depth given total depth
   ParabolicSection.ne - effective Manning's coefficient given depth
   ParabolicSection.hydraulic_radius - hydraulic radius given depth
   ParabolicSection.froude_number - Froude number given depth and flow rate
   ParabolicSection.velocity - velocity given depth and flow rate
   ParabolicSection.specific_energy - specific energy given depth and flow rate
   ParabolicSection.momentum_function - momentum function given depth and flow rate
   ParabolicSection.print_geometry - a table of geometry data relevant to the present section object
   
   
   
     