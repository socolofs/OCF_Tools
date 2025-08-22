"""
ocf_tools.py
============

Functions to make typical computations in open channel flows. The input / output
structure of these functions is based on the Matlab programs by Terry Sturm
distributed with Open Channel Hydraulics, Third Edition, McGraw Hill. The
algorithms and numerical approaches were developed separately by Scott A.
Socolofsky in 2022.

For an example, please see Example.py.  Report all errors or problems to Scott
A. Socolofsky at <socolofs@tamu.edu>.

"""
# S. Socolofsky, Texas A&M University, September 2023, <socolofs@tamu.edu>

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import fsolve


class Section(object):
    """
    General class definitions for all Section objects
    
    This is a base class for section objects that computes all required
    geometric and flow properties. This base class defines the geometric
    properties (area, top width, etc.) for a wide rectangular channel. For
    other cross-sectional shapes, it would be expected that derived classes
    that inherit this base class would re-define at least the `area`,
    `wetted_perimeter`, `top_width`, `centroid_depth` and `ne` methods. All
    other class methods depend on the input parameters and these geometric
    methods, so should be inheritable without updating.
    
    These functions use either U.S. Customary units (ft, s) or SI units (m,
    s). In the documentation, the dimensions of each variable are specified
    using L, T, and the corresponding units depend on the unit system
    selected when the cross-section is created.
    
    Parameters
    ----------
    nb : float
        Manning's coefficient for the main channel
    section_args : tuple
        A tuple of geometric parameters that describe the given channel 
        geometry.  This base class object assumes the only parameter in the
        tuple is the top-width and that the channel is rectangular.
    units : int, default=0
        Unit system (0 : U.S. Customary Units (ft, s), 1 : SI units (m, s))
    
    """
    def __init__(self, nb, section_args=(), unit_system=0):
        super(Section, self).__init__()
        
        # Store the input parameters
        self.nb = nb
        self.section_args = section_args
        self.unit_system = unit_system
        
        # Create a dictionary of real units to use in text statements
        self.units = {}

        # Set the unit system and units dictionary
        if self.unit_system == 0:
            self.Kn = 1.49
            self.g = 32.17
            self.units['Q'] = 'cfs'
            self.units['L'] = 'ft'
            self.units['T'] = 's'
            
        elif self.unit_system == 1:
            self.Kn = 1.0
            self.g = 9.81
            self.units['Q'] = 'm^3/s'
            self.units['L'] = 'm'
            self.units['T'] = 's'
            
        else:
            print('\nError:  The selected units system (units = %d)' % units)
            print('        is not recognized by this program.  ')
            print('\n        --> In the section object, select:')
            print('            0: U.S. Customary (ft/s) or')
            print('            1: SI (m/s)')
        
    def area(self, y):
        """
        Compute the cross-sectional area for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        A : float
            Cross-sectional area, L^2
        
        """
        # Get the top width
        B, = self.section_args
        
        # Compute the cross-sectional area or a rectangular section
        return y * B
    
    def wetted_perimeter(self, y):
        """
        Compute the wetted perimeter for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        P : float
            Wetted perimeter, L
        
        """
        # Get the top width
        B, = self.section_args
        
        # Compute the wetted perimeter (Sturm, Table 2.1)
        return 2. * y + B
        
    def top_width(self, y):
        """
        Compute the top width for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        B : float
            Top width, L
        
        """
        # Get the top width
        B, = self.section_args
        
        # Compute the top width (Sturm, Table 2.1)
        return B
    
    def centroid_depth(self, y):
        """
        Compute the depth of the centroid for a given flow depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        hc : float
            Depth of the centroid of the area, L, measured from the free
            surface, positive down
        
        """
        # Compute the centroid depth (using Sturm, Table 3.1 as reference)
        hc = y / 2.
        
        return hc
    
    def ne(self, y):
        """
        Compute the effective Manning's coefficeint for a given depth
        
        If the banks have different Manning's coefficients than the channel
        bottom, then a wetted-perimeter average should be computed.
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        ne : float
            Average Manning's coefficient
        
        """
        # A rectangular channel has only one Manning's coefficient
        
        # Return the average
        return self.nb
    
    def hydraulic_radius(self, y):
        """
        Compute the hydraulic radius for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        R : float
            Hydraulic radius, L
        
        """        
        # Compute the hydraulic radius
        return self.area(y) / self.wetted_perimeter(y)

    def froude_number(self, y, Q):
        """
        Compute the Froude number for given depth and flow rate
        
        Parameters
        ----------
        y : float
            Water depth, L
        Q : float
            Flow rate, L^3/T
        
        Returns
        -------
        Fr : float
            Froude number, --
        
        """
        # Get the area, A, and hydraulic depth, D
        A = self.area(y)
        B = self.top_width(y)
        D = A / B
        
        # Compute the Froude number
        return (Q / A) / np.sqrt(self.g * D)
    
    def velocity(self, y, Q):
        """
        Cross-sectionally averaged velocity
        
        Parameters
        ----------
        y : float
            Water depth, L
        Q : float
            Channel flow rate, L^3/T
        
        Returns
        -------
        v : float
            Velocity given by Q / A
        
        """
        # Compute the velocity
        return (Q / self.area(y))

    def specific_energy(self, y, Q):
        """
        Specific energy for flow in the channel with the given parameters
        
        Parameters
        ----------
        y : float
            Water depth, L
        Q : float
            Channel flow rate, L^3/T
        
        Returns
        -------
        E : float
            Specific energy following equation Table 3.1, L^3
        
        """
        # Compute the specific energy
        return (y + Q**2 / (2. * self.g * self.area(y)**2))
    
    def momentum_function(self, y, Q):
        """
        Momentum function for flow in the channel with the given parameters
         
        Parameters
        ----------
        y : float
            Water depth, L
        Q : float
            Channel flow rate, L^3/T
        
        Returns
        -------
        E : float
            Specific energy following equation (2.16), L
        
        """
        #  Get the area and depth of the centroid
        A = self.area(y)
        hc = self.centroid_depth(y)
        
        # Compute the momentum function
        return (A * hc + Q**2 / (self.g * A))   
    
    def print_geometry(self):
        """
        Output the current geometry data for printing
        
        """
        # Set up an empty list for storing data
        out_lines = []

        # Write all of the geometry data relevant to this cross-section
        out_lines += ['Top width, b, %s = %g\n' % 
            (self.units['L'], self.top_width(1.))]
        out_lines += ["Bottom Manning's n = %g\n" % self.nb]
        
        # Return the results
        return out_lines
        

class TrapSection(Section):
    """
    Class to handle cross-section data for a trapezoidal channel
    
    This class computes the area, wetted perimeter, hydraulic radius, etc., for 
    a trapezoidal channel.  
    
    Parameters
    ----------
    m : float
        Side slope ratio as `m` horizontal units (L) for every 1 vertical 
        unit (L)
    b : float
        Bottom width, L
    nb : float
        Manning's n for the channel bottom, universal dimensions
    ns : float, default=None
        Manning's n for the channel sides, universal dimensions. If ns = None,
        then it is assumed that the side slopes have the same Manning's 
        coefficient as the channel bottom
    units : int, default=0
        Unit system (0 : U.S. Customary Units (ft, s), 1 : SI units (m, s))
    
    """
    def __init__(self, m, b, nb, ns=None, units=0):

        # Package the geometric properties into a tuple
        section_args = (m, b)
        
        # Call the instantiation of the Section object
        super(TrapSection, self).__init__(nb, section_args, units)

        # Store the remaining input parameters
        self.m = m
        self.b = b
        if isinstance(ns, type(None)):
            self.ns = nb
        else:
            self.ns = ns        
    
    def area(self, y):
        """
        Compute the cross-sectional area for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        A : float
            Cross-sectional area, L^2
        
        """
        # Compute the cross-sectional area (Sturm, Table 2.1)
        return y * (self.b + self.m * y)
    
    def wetted_perimeter(self, y):
        """
        Compute the wetted perimeter for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        P : float
            Wetted perimeter, L
        
        """
        # Compute the wetted perimeter (Sturm, Table 2.1)
        return self.b + 2. * y * np.sqrt(1. + self.m**2)
    
    def top_width(self, y):
        """
        Compute the top width for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        B : float
            Top width, L
        
        """
        # Compute the top width (Sturm, Table 2.1)
        return (self.b + 2. * self.m * y)
    
    def centroid_depth(self, y):
        """
        Compute the depth of the centroid for a given flow depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        hc : float
            Depth of the centroid of the area, L, measured from the free
            surface, positive down
        
        """
        # Compute the centroid depth (using Sturm, Table 3.1 as reference)
        hc = (self.b * y**2 / 2. + self.m * y**3 / 3.) / self.area(y)
        
        return hc
    
    def ne(self, y):
        """
        Compute the effective Manning's coefficeint for a given depth
        
        If the banks have different Manning's coefficients than the channel
        bottom, then a wetted-perimeter average is computed.
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        ne : float
            Average Manning's coefficient
        
        """
        # Get the total wetted perimeter
        P = self.wetted_perimeter(y)
        
        # Sum the contributions from the banks and bottom
        ne2 = (2. * self.ns**2 * np.sqrt(1. + self.m**2) * y + 
            self.nb**2 * self.b) / P
        
        # Return the average
        return np.sqrt(ne2)
    
    def print_geometry(self):
        """
        Output the current geometry data for printing
        
        """
        # Set up an empty list for storing data
        out_lines = []

        # Write all of the geometry data relevant to this cross-section
        out_lines += ['Bottom width, b, %s = %g\n' % 
            (self.units['L'], self.b)]
        out_lines += ['Side slope ratio, m:1 = %g\n' % self.m]
        out_lines += ["Bottom Manning's n = %g\n" % self.nb]
        out_lines += ["Sides Manning's n = %g\n" % self.ns]
        
        # Return the results
        return out_lines
        

class TriangularSection(Section):
    """
    Class to handle cross-section data for a triangular channel
    
    This class computes the area, wetted perimeter, hydraulic radius, etc., for 
    a triangular channel.  
    
    Parameters
    ----------
    m : float
        Side slope ratio as `m` horizontal units (L) for every 1 vertical 
        unit (L)
    nb : float
        Manning's n for the channel bottom, universal dimensions
    units : int, default=0
        Unit system (0 : U.S. Customary Units (ft, s), 1 : SI units (m, s))
    
    """
    def __init__(self, m, nb, units=0):

        # Package the geometric properties into a tuple
        section_args = (m,)
        
        # Call the instantiation of the Section object
        super(TriangularSection, self).__init__(nb, section_args, units)

        # Store the remaining input parameters
        self.m = m      
    
    def area(self, y):
        """
        Compute the cross-sectional area for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        A : float
            Cross-sectional area, L^2
        
        """
        # Compute the cross-sectional area (Sturm, Table 2.1)
        return self.m * y**2
    
    def wetted_perimeter(self, y):
        """
        Compute the wetted perimeter for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        P : float
            Wetted perimeter, L
        
        """
        # Compute the wetted perimeter (Sturm, Table 2.1)
        return 2. * y * np.sqrt(1. + self.m**2)
    
    def top_width(self, y):
        """
        Compute the top width for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        B : float
            Top width, L
        
        """
        # Compute the top width (Sturm, Table 2.1)
        return (2. * self.m * y)
    
    def centroid_depth(self, y):
        """
        Compute the depth of the centroid for a given flow depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        hc : float
            Depth of the centroid of the area, L, measured from the free
            surface, positive down
        
        """
        # Compute the centroid depth (using Sturm, Table 3.1 as reference)        
        return y / 3.
    
    def print_geometry(self, units):
        """
        Output the current geometry data for printing
        
        """
        # Set up an empty list for storing data
        out_lines = []

        # Write all of the geometry data relevant to this cross-section
        out_lines += ['Side slope ratio, m:1 = %g\n' % self.m]
        out_lines += ["Bottom Manning's n = %g\n" % self.nb]
        
        # Return the results
        return out_lines
    

class CircularSection(Section):
    """
    Class to handle cross-section data for a circular channel
    
    This class computes the area, wetted perimeter, hydraulic radius, etc., for 
    a circular channel.  
    
    Parameters
    ----------
    d : float
        Diameter of the conduit, L
    nb : float
        Manning's n for the channel bottom, universal dimensions
    units : int, default=0
        Unit system (0 : U.S. Customary Units (ft, s), 1 : SI units (m, s))
    
    """
    def __init__(self, d, nb, units=0):

        # Package the geometric properties into a tuple
        section_args = (d,)
        
        # Call the instantiation of the Section object
        super(CircularSection, self).__init__(nb, section_args, units)

        # Store the remaining input parameters
        self.d = d      
    
    def theta(self, y):
        """
        Angle to the free surface in circular channel flow
        
        Angle relating the free surface to the center of the circular
        channel.  See Sturm (2021) Table 2.1, footnote for circular
        cross-section
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        theta : float
            Angle through the channel center to the free surface intersection
            with the circular channel walls.
        
        """
        # Compute the angle from the equation in Sturm, Table 2.1
        return 2. * np.arccos(1. - 2. * y / self.d)
    
    def area(self, y):
        """
        Compute the cross-sectional area for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        A : float
            Cross-sectional area, L^2
        
        """
        # Compute the cross-sectional area (Sturm, Table 2.1)
        return (self.theta(y) - np.sin(self.theta(y))) * self.d**2 / 8.
    
    def wetted_perimeter(self, y):
        """
        Compute the wetted perimeter for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        P : float
            Wetted perimeter, L
        
        """
        # Compute the wetted perimeter (Sturm, Table 2.1)
        return self.theta(y) * self.d / 2.
    
    def top_width(self, y):
        """
        Compute the top width for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        B : float
            Top width, L
        
        """
        # Compute the top width (Sturm, Table 2.1)
        return self.d * np.sin(self.theta(y) / 2.)
    
    def centroid_depth(self, y):
        """
        Compute the depth of the centroid for a given flow depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        hc : float
            Depth of the centroid of the area, L, measured from the free
            surface, positive down
        
        """
        # Get the internal angle
        theta = self.theta(y)
        
        # Compute the centroid depth (using Sturm, Table 3.1 as reference)
        hc = (3. * np.sin(theta / 2.) - (np.sin(theta / 2.))**3 - 3. * \
            theta / 2. * np.cos(theta / 2.)) * self.d**3 / 24. / self.area(y)
        
        return hc
    
    def print_geometry(self):
        """
        Output the current geometry data for printing
        
        """
        # Set up an empty list for storing data
        out_lines = []

        # Write all of the geometry data relevant to this cross-section
        out_lines += ['Channel diameter, d, %s = %g\n' % 
            (self.units['L'], self.d)]
        out_lines += ["Bottom Manning's n = %g\n" % self.nb]
        
        # Return the results
        return out_lines


class ParabolicSection(Section):
    """
    Class to handle cross-section data for a parabolic channel
    
    This class computes the area, wetted perimeter, hydraulic radius, etc., for 
    a parabolic channel.  
    
    Parameters
    ----------
    B1 : float
        Top-wdith of the full channel, L
    y1 : float
        Depth of the full channel, L
    nb : float
        Manning's n for the channel bottom, universal dimensions
    units : int, default=0
        Unit system (0 : U.S. Customary Units (ft, s), 1 : SI units (m, s))
    
    """
    def __init__(self, B1, y1, nb, units=0):

        # Package the geometric properties into a tuple
        section_args = (B1, y1)
        
        # Call the instantiation of the Section object
        super(ParabolicSection, self).__init__(nb, section_args, units)

        # Store the remaining input parameters
        self.B1 = B1
        self.y1 = y1
    
    def area(self, y):
        """
        Compute the cross-sectional area for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        A : float
            Cross-sectional area, L^2
        
        """
        # Get the top-width
        B = self.top_width(y)
        
        # Compute the cross-sectional area (Sturm, Table 2.1)
        return 2. / 3. * B * y
    
    def wetted_perimeter(self, y):
        """
        Compute the wetted perimeter for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        P : float
            Wetted perimeter, L
        
        """
        # Get the top-width
        B = self.top_width(y)
        
        # Compute the wetted perimeter (Sturm, Table 2.1)
        if y / B < 0.25:
            P = B + (8. / 3.) * y**2 / B
            
        else:
            x = 4. * y / B
            P = B / 2. * (np.sqrt(1 + x**2) + 1. / x * np.log(x + 
                np.sqrt(1. + x**2)))
        
        return P
    
    def top_width(self, y):
        """
        Compute the top width for a given depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        B : float
            Top width, L
        
        """
        # Compute the top width (Sturm, Table 2.1)
        return self.B1 * (np.sqrt(y / self.y1))
    
    def centroid_depth(self, y):
        """
        Compute the depth of the centroid for a given flow depth
        
        Parameters
        ----------
        y : float
            Water depth, L
        
        Returns
        -------
        hc : float
            Depth of the centroid of the area, L, measured from the free
            surface, positive down
        
        """
        # Get the csi parameter
        csi = self.B1 / np.sqrt(self.y1)
        
        # Compute the centroid depth (using Sturm, Table 3.1 as reference)
        hc = (4. / 15. * csi * y**(5./2.)) / self.area(y)
        
        return hc
    
    def print_geometry(self):
        """
        Output the current geometry data for printing
        
        """
        # Set up an empty list for storing data
        out_lines = []

        # Write all of the geometry data relevant to this cross-section
        out_lines += ['Full top-width, B1, %s = %g\n' % 
            (self.units['L'], self.B1)]
        out_lines += ['Full channel depth, y1, %s = %g\n' %
            (self.units['L'], self.y1)]
        out_lines += ["Bottom Manning's n = %g\n" % self.nb]
        
        # Return the results
        return out_lines


class OpenChannel(object):
    """
    Class object to compute open channel flow profiles
    
    Parameters
    ----------
    section : TrapSection
        A trapezoidal section object that is used to compute cross-sectional
        properties of area, wetted perimeter, hydraulic radius, and top 
        width, etc.
    
    """
    def __init__(self, section):
        super(OpenChannel, self).__init__()
        
        # Save the input data
        self.section = section
        
        # Extract some properties from the section object
        self.Kn = section.Kn
        self.g = section.g
        self.units = section.units
        
        # Set a flag indicating whether a profile has been computed
        self.profile_stored = False
    
    def critical_depth(self, Q, y0=1.):
        """
        Compute the critical depth for the given flow rate
        
        Parameters
        ----------
        Q : float
            Channel flow rate, L^3/T
        y0 : float
            Initial guess for the critical depth, L.  Default = 1.0
        
        Returns
        -------
        yc : float
            Critical depth, L
        
        """
        def residual(y, Q):
            """
            Compute the difference between the Froude number at the given 
            water depth and a value of 1
            
            """
            # Compute 
            Fr = self.section.froude_number(y, Q)
            
            # Return the residual
            return (Fr - 1.)
        
        # Find the critical depth by finding where Fr = 1
        yc = fsolve(residual, y0, args=(Q,))[0]
            
        return yc
    
    def normal_depth(self, Q, S, y0=1.):
        """
        Compute the normal depth for the given flow rate and slope
        
        Parameters
        ----------
        Q : float
            Channel flow rate, L^3/T
        S : float
            Channel slope, --
        y0 : float
            Initial guess for the normal depth, L.  Default = 1.0
        
        Returns
        -------
        yn : float
            Normal depth, L
        
        """
        def residual(y, Q, S):
            """
            Compute the difference between the normal flow at the given water
            depth and the desired flow rate
            
            """
            return (Q - self.manning_flow(y, S))
        
        # Find the normal depth by finding where the uniform flow is the
        # given flow rate
        if S <= 0:
            # There is no normal depth
            yn = np.nan
        else:
            yn = fsolve(residual, y0, args=(Q, S))[0]
            if yn == y0:
                # Search got lost...try initializing at critical depth
                yc = self.critical_depth(Q)
                yn = fsolve(residual, yc, args=(Q, S))[0]
        
        return yn
    
    def sequent_depth(self, Q, y0):
        """
        Compute the sequent depth of a hydraulic jump
        
        Compute the sequent depth for a hydraulic jump in the section.  This
        method first computes the Froude number to determine whether the 
        given depth is sub- or super-critical.  It then solves for the 
        corresponding super- or sub-critical critical depth by enforcing 
        conservation of the momentum function through the jump.  This method
        assumes a horizontal channel through the jump section.
        
        Parameters
        ----------
        Q : float
            Channel flow rate, L^3/T
        y0 : float
            Water depth on one side of the hydraulic jump, L.  If the 
            Froude number for `y0` and `Q` is greater than 1, `y0` is the
            downstream depth `y2`; otherwise, `y0` is the upstream depth
            `y1`.
        
        Returns
        -------
        ys : float 
            The appropriate sequent depth, L
        
        """
        # Compute the Froude number
        Fr0 = self.section.froude_number(y0, Q)
        
        # And the momentum function of the given flow
        M1 = self.section.momentum_function(y0, Q)
        
        # Determine which sequent depth we are searching for and set an 
        # initial guess for the sought value
        if Fr0 > 1:
            # Given flow is super-critical...find the critical depth
            yc = self.critical_depth(Q, 1.15 * y0)
            
            # Set a guess for the sequent depth
            ys_0 = 1.25 * yc
        
        elif Fr0 < 1:
            # Given flow is sub-critical...find the critical depth
            yc = self.critical_depth(Q, 0.85 * y0)
            
            # Set a guess for the sequent depth
            ys_0 = 0.5 * yc
        
        else:
            # Given flow is critical...no jump expected
            print('\nWARNING:  The given condition is critical; hence, a ')
            print('          hydraulic jump is not expected.  The sequent')
            print('          depth would be the same as the given')
            print('          conditions.\n')
            return y0
        
        # Write a residual function to conserve the momentum function
        def residual(y, Q, M1, section):
            """
            Residual of the expression F(y2) = M1 - M2(y2) = 0
            
            """
            return M1 - section.momentum_function(y, Q)

        # Search for the sequent depth
        from scipy.optimize import fsolve
        ys = fsolve(residual, ys_0, args=(Q, M1, self.section))[0]
        
        # Check the Froude number
        Fr1 = self.section.froude_number(ys, Q)
        if (Fr0 < 1 and Fr1 < 1) or (Fr0 > 1 and Fr1 > 1):
            # Could not find jumped depth
            print('\nERROR:  Found a sequent depth that has the same ')
            print('        conditions as the inflow; hence, the present')
            print('        algorithm is unstable.\n')
            return np.nan
        
        # Return the found sequent depth
        return ys
    
    def manning_flow(self, y, S):
        """
        Compute the flow from Manning's equation for the given depth and slope
        
        Parameters
        ----------
        y : float
            Water depth, L
        S : float
            Channel slope, --
        
        Returns
        -------
        Qn : float
            Flow rate using a Manning's equation, L^3/T
        
        """
        # Get the area, hydraulic radius, and effective Manning's n
        A = self.section.area(y)
        R = self.section.hydraulic_radius(y)
        ne = self.section.ne(y)
        
        # Compute Manning's equation
        if S >= 0.:
            Qn = self.Kn / ne * A * R**(2./3.) * np.sqrt(S)
        else:
            # Adverse friction slope -- impossible
            Qn = np.nan
        
        return Qn

    def profile_type(self, y0, Q, S, control_section=1):
        """
        Determine the profile type (M1, M2, S1, etc) for the given conditions
        
        Determine which gradually-varied flow profile type will be computed
        for the specified initial depth at the given flow rate and channel
        slope.
        
        Parameters
        ----------
        y0 : float
            The water depth at the channel control point, L.  The control can 
            either be downstream (mild slopes) or upstream (steep slopes).
        Q : float
            Channel flow rate, L^3/T
        S : float
            Channel slope, --
        control_section : int, default=1
            A flag indicating where the control is located (0 : upstream / 
            supercritical flow, 1 : downstream / subcritical flow)
        
        Returns
        -------
        shape : str
            String reporting the profile shape using terms in Figure 5.2
        
        """
        # Get the normal and critical depths
        yn = self.normal_depth(Q, S, y0=y0)
        if not np.isnan(yn):
            yc = self.critical_depth(Q, y0=0.5 * yn)
        else:
            yc = self.critical_depth(Q, y0)
        
        # Determine the slope type
        if yn == yc:
            # Critical slope
            if control_section == 0:
                if y0 < yc:
                    shape = 'C2'
                else:
                    shape = None
            else:
                if y0 > yc:
                    shape = 'C1'
                else:
                    shape = None
        
        elif S == 0:
            # Horizontal slope
            if control_section == 0:
                if y0 < yc:
                    shape = 'H2'
                else:
                    shape = None
            else:
                if y0 > yc:
                    shape = 'H1'
                else:
                    shape = None
            
        elif S < 0:
            # Adverse slope
            if control_section == 0:
                if y0 < yc:
                    shape = 'A2'
                else:
                    shape = None
            else:
                if y0 > yc:
                    shape = 'A1'
                else:
                    shape = None
        
        elif yn > yc:
            # Mild slope
            if control_section == 0:
                if y0 < yc:
                    shape = 'M3'
                else:
                    shape = None
            else:
                if y0 < yn and y0 > yc:
                    shape = 'M2'
                elif y0 > yn:
                    shape = 'M1'
                else:
                    shape = None
        
        elif yc > yn:
            # Steep slope
            if control_section == 0:
                if y0 < yn:
                    shape = 'S3'
                elif y0 < yc:
                    shape = 'S2'
                else:
                    shape = None
            else:
                if y0 > yc:
                    shape = 'S1'
                else:
                    shape = None

        else:
            shape = None
        
        if isinstance(shape, type(None)):
            print('\nError:  This flow situation cannot be classified...')
            print('        Either the control section is wrong or the flow')
            print('        is rapidly varied.')
            shape = 'Error'
         
        return shape
    
    def profile(self, x0, y0, Q, S, control_section=1, delta_x=1000., 
        max_x=None):
        """
        Compute a gradually varied flow profile for the given conditions
        
        Parameters
        ----------
        x0 : float
            The x-coordinate to assign to the channel control, L.  The control is 
            the point in the channel where the water depth `y0` is specified.
        y0 : float
            The water depth at the channel control point, L.  The control can 
            either be downstream (mild slopes) or upstream (steep slopes).
        Q : float
            Channel flow rate, L^3/T
        S : float
            Channel slope, --
        control_section : int, default=1
            A flag indicating where the control is located (0 : upstream /  
            steep slope, 1 : downstream / mild slope)
        delta_x : float, default=1000.
            Maximum spatial step, L, to take in the computed profile; 
            default = 1000.
        max_x : float, default=None
            Maximum along-stream distance to compute, L; default = None. If
            `None`, then the model computes until the water depth is within 
            0.1 percent of the normal or critical depth.
         
        Returns
        -------
        x : ndarray
            Array of positions, L, where the solution has been computed
        y : ndarray 
            Array of water depths, L, computed at each corresponding `x` 
            position
        
        """
        # Store parameters describing the profile
        self.x0 = x0
        self.y0 = y0
        self.Q = Q
        self.S = S
        self.control_section = control_section
        
        # Compute the normal depth and critical depth (we will stop integrating
        # if we get close to either of these)
        self.yn = self.normal_depth(Q, S, y0=y0)
        if not np.isnan(self.yn):
            self.yc = self.critical_depth(Q, y0=self.yn)
        else:
            self.yc = self.critical_depth(Q, y0)
        
        # Determine the integration direction
        if control_section == 0:
            upstream_control = True
        else:
            upstream_control = False
        
        # Compute the profile
        self.x, self.y = compute_gvf_profile(x0, y0, self.yc, self.yn,
            self.section, Q, S, upstream_control, delta_x, max_x)
        self.profile_stored = True
        
        # Return the profile
        return self.x, self.y

    def plot_profile(self, fig=1, label='GVF Profile', clearfig=True):
        """
        Plot the currently-stored gradually varied flow profile
        
        """
        # Throw an error if the profile is not stored yet
        if not self.profile_stored:
            print('\nError:  Compute a gradually varied flow profile using')
            print('        OpenChannel.profile() before plotting')
            return
        
        # Write a title
        title_text = 'Q = %g (%s), S = %g (--)' % (self.Q, self.units['Q'], 
            self.S)
        
        # Compute channel bottom and water elevations
        zp = np.zeros(self.x.shape)
        yp = np.zeros(self.y.shape)
        yp[0] = self.y[0]
        for i in range(1, len(self.x)):
            zp[i] = zp[i-1] + self.S * (self.x[i-1] - self.x[i])
            yp[i] = self.y[i] + zp[i]
        ynp = zp + self.yn
        ycp = zp + self.yc
        
        # Open a figure
        plt.figure(fig, figsize=(9,5))
        if clearfig:
            plt.clf()
        
        # Create and plot
        plt.plot(self.x, zp, 'k-', label='Channel bottom')
        plt.plot(self.x, ynp, 'g:', label='Normal depth')
        plt.plot(self.x, ycp, 'c--', label='Critical depth')
        plt.plot(self.x, yp, 'b-', label=label)
        plt.plot(self.x[0], yp[0], 'mo', label='Control')
        plt.xlabel('Distance (%s)' % (self.units['L']))
        plt.ylabel('Depth (%s)' % (self.units['L']))
        plt.legend()
        plt.title(title_text)
        plt.draw()
        plt.show()
        
    def get_profile_table(self):
        """
        Create a table of output data for the present profile
        
        Create a table of output data following the format of Table B3 is
        Sturm, Open Channel Hydraulics, Third Edition, McGraw Hill
    
        """
        # Throw an error if the profile is not stored yet
        if not self.profile_stored:
            print('\nError:  Compute a gradually varied flow profile using')
            print('        OpenChannel.profile() before plotting')
            return
        
        # Write a header
        header = '    X, %s   Y, %s  V, %s/%s  E, %s   MF, %s^3' % \
            (self.units['L'], self.units['L'], self.units['L'], 
            self.units['T'], self.units['L'], self.units['L'])
        
        # Initialize an array to hold the data
        data = np.zeros((len(self.x), 5))
        
        # Create the data
        for i in range(len(self.x)):
            
            # Position and depth
            data[i,0] = self.x[i]
            data[i,1] = self.y[i]
            
            # Velocity = Q / A
            data[i,2] = self.section.velocity(self.y[i], self.Q)
            
            # Specific Energy 
            data[i,3] = self.section.specific_energy(self.y[i], self.Q)
            
            # Momentum Function
            data[i,4] = self.section.momentum_function(self.y[i], self.Q)
            
        return (header, data)
    
    def save_profile_table(self, fname):
        """
        Save the profile data table to a file
        
        Save the profile data table, which includes the position, depth, 
        velocity, specific energy, and momentum function at each computed
        position.
        
        Parameters
        ----------
        fname : str
            File name with absolute or relative path for the file to save
        
        """
        # Get the data for the table
        header, data = self.get_profile_table()
        
        # Write the additional information describing the run
        out_lines = []
        out_lines += ['Discharge, %s = %g\n' % (self.units['Q'], self.Q)]
        out_lines += ['Slope, %s/%s = %g\n' % (self.units['L'], 
            self.units['L'], self.S)]
        out_lines += self.section.print_geometry()
        out_lines += ['Profile length, %s = %g\n\n' % (self.units['L'], 
            np.max(np.abs(self.x)))]
        out_lines += ['*******************************\n']
        out_lines += ['Normal depth, %s = %g\n' % (self.units['L'], self.yn)]
        out_lines += ['Critical depth, %s = %g\n' % (self.units['L'], self.yc)]
        out_lines += ['Control depth, %s = %g\n' % (self.units['L'], 
            self.y[0])]
        out_lines += ['Profile Type = %s\n' % (self.profile_type(self.y0, 
            self.Q, self.S, self.control_section))]
        out_lines += ['*******************************\n\n']
        out_lines += [header + '\n']
        out_lines += ['********************************************\n']
        for i in range(len(data[:,0])):
            out_lines += ['%9.6g %7.4g %7.3g %7.3g %10.6g\n' % (data[i,0],
                data[i,1], data[i,2], data[i,3], data[i,4])]
        
        # Create the output string
        output = ''.join(out_lines)
        
        # Write the file
        with open(fname, 'w') as datfile:
            datfile.write(output)
        
        return output
        
def gvf_derivs(x, y, section, Q, S, upstream_control=False):
    """
    Compute the right-hand-side of the gradually-varied flow 
    
    Parameters
    ----------
    x : float
        Current position along the channel, L
    y : float
        Current water depth at the present channel location, L
    section : TrapSection
        A trapezoidal section object that is used to compute cross-sectional
        properties
    Q : float
        Channel flow rate, L^3/T
    S : float
        Channel slope, --
    upstream_control : bool, default=False
        A flag indicating whether the control is upstream (True, steep slopes) 
        or downstream (False, mild slopes).  Default value is `False`.
    
    Returns
    -------
    yp : float
        The slope of the water surface profile, given by the gradually-varied
        flow equation:  (S0 - Sf) / (1 - Fr^2)
    
    Notes
    -----
    This function uses the Manning equation to estimate the slope of the
    energy grade line under the gradually-varied flow assumption
    
    """
    if upstream_control:
        # Iterate in the downstream direction (positive x-direction)
        x_dir = 1.
    else:
        # Iterate in the upstream direction (negative x-direction)
        x_dir = -1.
    
    # Get the section parameters
    R = section.hydraulic_radius(y)
    B = section.top_width(y)
    A = section.area(y)
    
    # Compute the local velocity 
    v = Q / A
    
    # Compute the local Froude number
    Fr = section.froude_number(y, Q)
    
    # Compute the friction slope from Manning's equation
    ne = section.ne(y)
    Kn = section.Kn
    Sf = (v / (Kn / ne * R**(2./3.)))**2
    
    # Compute the governing ODE
    yp = x_dir * (S - Sf) / (1. - Fr**2)
    
    return yp

def compute_gvf_profile(x0, y0, yc, yn, section, Q, S, upstream_control=False,
    delta_x=1000., max_x=None):
    """
    Compute a gradually-varied flow profile with given initial conditions
    
    Compute a gradually-varied flow profile with initial conditions `x0` 
    and `y0` in a given channel at a given flow rate and slope.
    
    Parameters
    ----------
    x0 : float
        The x-coordinate to assign to the channel control, L.  The control is 
        the point in the channel where the water depth `y0` is specified.
    y0 : float
        The water depth at the channel control point, L.  The control can either
        be downstream (mild slopes) or upstream (steep slopes).
    yc : float
        Critical depth at the given Q, L
    yn : float
        Channel normal depth at the given Q and S, L
    section : TrapSection
        A trapezoidal section object that is used to compute cross-sectional
        properties
    Q : float
        Channel flow rate, L^3/T
    S : float
        Channel slope, --
    upstream_control : bool, default=False
        A flag indicating whether the control is upstream (True, steep slopes) 
        or downstream (False, mild slopes).  Default value is `False`.
    delta_x : float, default=1000.
        Maximum spatial step, L, to take in the computed profile; default = 
        1000.
    max_x : float, default=None
        Maximum upstream distance to compute, L; default = None.  If `None`, then
        the model computes until the water depth is within 0.1 percent of the 
        normal or critical depth.
    
    Returns 
    -------
    x : ndarray
        Array of positions, L, where the solution has been computed
    y : ndarray 
        Array of water depths, L, computed at each corresponding `x` position
        
    """
    # Import the ODE solver module from Scipy
    from scipy import integrate
    
    # Set up the integrator
    r = integrate.ode(gvf_derivs).set_integrator('vode', method='bdf',
        atol=1.e-6, rtol=1.e-3, order=5, max_step=delta_x)
    
    # Set the initial conditions
    print('\n--- Computing GVF Profile ---')
    r.set_initial_value(y0, x0)
    
    # Set the additional parameters to pass to the derivatives function
    r.set_f_params(section, Q, S, upstream_control)
    
    # Create lists to hold the solution and store the initial conditions
    x = [x0]
    y = [y0]
    
    # Set up the integration
    k = 0
    kmax = 100000
    psteps = 5
    stop = False
    if section.unit_system == 0:
        L_unit = 'ft'
    else:
        L_unit = 'm'
    
    # Integrate the profile
    while r.successful() and not stop:
        
        # Perform one step of the integration
        r.integrate(x[-1] + delta_x, step=True)
        k += 1
        
        # Store the current solution point
        x.append(r.t)
        y.append(r.y[0])
        
        # Print progress to the screen
        if k % psteps == 0:
            print('    -> k = %4.4d: x = %g (%s), y = %g (%s)' % (k, x[-1], 
                L_unit, y[-1], L_unit))
    
        # Evaluate the stop criteria
        if k > kmax:
            stop = True
            print('\nMaximum number of iterations achieved...Stopping\n')
        if np.abs(y[-1] - yn) / yn <= 0.001:
            stop = True
            print('\nReached normal depth...Stopping\n')
        if np.abs(y[-1] - yc) / yc <= 0.001:
            stop = True
            print('\nReached critical depth...Stopping\n')
        if not isinstance(max_x, type(None)):
            if np.abs(x[-1] - x[0]) > max_x:
                stop = True
                print('\nReached maximum profile length requested...Stopping\n')
    
    # Convert solution vectors to arrays
    if upstream_control:
        # Data were computed in the positive x-direction
        x = np.array(x)
    else:
        # Data were computed in the negative x-direction
        x = x0 + (x0 - np.array(x))
    y = np.array(y)
    
    # Return the solution vectors
    return x, y

    
    
    
    
    