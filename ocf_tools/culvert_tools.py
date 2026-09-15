"""
Culvert_tools.py
================

Python functions to compute discharge through various culvert designs.

"""
# S. Socolofsky, Texas A&M University, September 2023, <socolofs@tamu.edu>

import ocf_tools

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import fsolve

def culvert_flow(hw, tw, culvert, S, K, M, c, Y, Ke, L, report=True):
    """
    Compute the flow rate through a culvert for given conditions
    
    Compute the discharge through a culvert with given head water `hw` and
    culvert parameters. Because the culvert parameters are dimensional, U.S.
    Customary Units have to be used for all variables.
    
    Parameters
    ----------
    hw : float
        Culvert upstream head water level, ft
    tw : float
        Culvert downstream head water level, ft
    culvert : ocf_tools.OpenChannel
        An `ocf_tools.OpenChannel` object for computing normal and critical depth
        and flow profiles.
    S : float
        Culvert slope, ft/ft
    K : float
        K-parameter for inlet control from Table 6.3
    M : float
        M-parameter inlet control from Table 6.3
    c : float
        c-parameter inlet control from Table 6.3
    Y : float
        Y-parameter inlet control from Table 6.3
    Ke : float
        Entrance loss coefficient for outlet control from Table 6.5
    L : float
        Length of the culvert barrel, ft
    report : bool
        A flag indicating whether or not to print summary results of 
        calculations
    
    Returns
    -------
    Q : float
        Flow rate through the culvert, cfs
    flow_type : str
        String name describing the flow type
    
    """
    # Extract the culvert diameter from the section object
    d = culvert.section.d
    
    # Check for a steep or mild full-barrel flow
    Q0 = culvert.manning_flow(0.94 * d, S)
    y0 = 0.90 * 0.94 * d
    yc = culvert.critical_depth(Q0, y0)
    
    if report:
        print('Full culvert characteristics:  ')
        print('    Qf, cfs = %g' % Q0)
        print('    yn, ft  = %g' % y0)
        print('    yc, ft  = %g' % yc)
    
    full_steep = False
    if yc > y0:
        full_steep = True
    
    if report:
        if full_steep:
            print('    --> Steep')
        else:
            print('    --> Mild')
    
    # Compute maximum flow at the normal depth
    Qn = culvert.manning_flow(0.94 * d, S)
    
    if report:
        print('    --> Maximum full flow, cfs = %g' % Qn)
    
    # Compute the relative head at the entrance
    hp = hw / d
    
    # Assume channel is inlet controlled
    if hp <= 1.5:
        # Compute Q for an unsubmerged inlet (Type IC-2)
        Q = Q_ic_2(hw, culvert, S, K, M)
        flow_type = 2
        
    else:
        # Compute Q for a submerged inlet (Type IC-1)
        Q = Q_ic_1(hw, culvert, S, c, Y)
        flow_type = 1
    
    # Compute the critical and normal depths at this flow rate
    if hw < d:
        yc = culvert.critical_depth(Q, 0.1 * d)
    else:
        yc = culvert.critical_depth(Q, 0.7 * d)
    
    if Q <= Qn:
        if hw < d:
            yn = culvert.normal_depth(Q, S, 0.95 * yc)
        else:
            yn = culvert.normal_depth(Q, S, 0.9 * d)
    else:
        yn = np.nan
    
    # Decide if the culvert is outlet controlled instead
    if not np.isnan(yn) and yn > yc:
        # Mild-slope open-channel flow inside culvert
        Q, y0 = reservoir_inflow(hw, culvert, S, Ke)
        flow_type = 4
        if np.isnan(y0) and hw > d:
            # Could not find solution...submerged
            Q = Q_oc_1(hw, tw, culvert, S, Ke, L)
            flow_type = 3      
        
    elif np.isnan(yn) and not full_steep:
        # Mild-slope closed-conduit flow inside culvert
        Q = Q_oc_1(hw, tw, culvert, S, Ke, L)
        flow_type = 3
    
    elif tw / d > 1.5:
        # Downstream is downed, assume closed-conduit flow
        Q = Q_oc_1(hw, tw, culvert, S, Ke, L)
        flow_type = 3
    
    types = ['Type IC-1', 'Type IC-2', 'Type OC-1', 'Type OC-2']
    if report:
        print('\nFlow at given conditions:')
        print('    %s' % (types[flow_type - 1]))
        print('    Q, cfs = %g' % Q)
        print('    yc, ft = %g' % yc)
        print('    y0, ft = %g\n' % yn)
    
    return Q, flow_type, yc, yn


def Q_ic_1(hw, culvert, S, c, Y):
    """
    Compute flow rate assuming a Type IC-1 culvert
    
    Compute the flow rate from Sturm (2021), equation (6.13) for a culvert 
    having inlet control with a submerged inlet.  This is Type IC-1 flow.
    
    Parameters
    ----------
    hw : float
        Culvert upstream head water level, ft
    culvert : ocf_tools.OpenChannel
        An `ocf_tools.OpenChannel` object for computing normal and critical depth
        and flow profiles.
    S : float
        Culvert slope, ft/ft
    c : float
        c-parameter inlet control from Table 6.3
    Y : float
        Y-parameter inlet control from Table 6.3
    
    Returns
    -------
    Q : float
        Flow rate assuming a Type IC-1 culvert, cfs
    
    """
    # Extract some channel properties from the section object
    d = culvert.section.d         # Diameter, ft
    A = culvert.section.area(d)   # Full area, ft^2
    
    # Solve for Q from equation (6.13)
    Q = np.sqrt((hw / d - Y + 0.5 * S) / c) * A * np.sqrt(d)
    
    return Q

def Q_ic_2(hw, culvert, S, K, M):
    """
    Compute flow rate assuming a Type IC-2 culvert
    
    Compute the flow rate from Sturm (2021), equation (6.12a) for a culvert 
    having inlet control with a unsubmerged inlet.  This is Type IC-2 flow.
    
    Parameters
    ----------
    hw : float
        Culvert upstream head water level, ft
    culvert : ocf_tools.OpenChannel
        An `ocf_tools.OpenChannel` object for computing normal and critical depth
        and flow profiles.
    S : float
        Culvert slope, ft/ft
    K : float
        K-parameter for inlet control from Table 6.3
    M : float
        M-parameter inlet control from Table 6.3
    
    Returns
    -------
    Q : float
        Flow rate assuming a Type IC-1 culvert, cfs
    
    """
    # Extract some channel properties from the section object
    d = culvert.section.d         # Diameter, ft
    A = culvert.section.area(d)   # Full area, ft^2
    
    def residual(Q):
        """
        Residual of the discharge for given Q
        
        """
        # Compute the critical depth
        yc = culvert.critical_depth(Q, hw)
        if yc == hw:
            if hw < d / 2.:
                yc = culvert.critical_depth(Q, hw / 2.)
            else:
                yc = culvert.critical_depth(Q, d / 2.)
        Ec = culvert.section.specific_energy(yc, Q)
        
        # Solve for Q from equation (6.13)
        if (hw/d - Ec/d) < 0:
            Qp = 0.
        else:
            Qp = ((hw / d - Ec / d + 0.5 * S) / K)**(1./M) * A * np.sqrt(d)
        
        # Return the present residual
        return (Q - Qp)
    
    # Find a discharge that matches the given conditions
    if hw > d:
        A0 = culvert.section.area(d)
    else:
        A0 = culvert.section.area(hw)
    Q0 = 1.0 * A0 * np.sqrt(culvert.g * hw) 
    Q = fsolve(residual, Q0)[0]
    
    return Q

def Q_oc_1(hw, tw, culvert, S, Ke, L):
    """
    Compute flow rate assuming a Type OC-1 culvert
    
    Compute the flow rate fromm Sturm (2021), equation (6.15b) fo a culvert
    having outlet control with closed-conduit flow along the barrel.  This is
    a Type OC-1 flow.
    
    Parameters
    ----------
    hw : float
        Culvert upstream head water level, ft
    tw : float
        Culvert downstream head water level, ft
    culvert : ocf_tools.OpenChannel
        An `ocf_tools.OpenChannel` object for computing normal and critical depth
        and flow profiles.
    S : float
        Culvert slope, ft/ft
    Ke : float
        Entrance loss coefficient, --
    L : float
        Length of the culvert barrel, ft
    
    Returns
    -------
    Q : float
        Flow rate assuming a Type OC-1 culvert, cfs
    
    """
    # Extract some channel properties from the section object
    d = culvert.section.d                     # Diameter, ft
    A = culvert.section.area(d)               # Full area, ft^2
    R = culvert.section.hydraulic_radius(d)   # Full hydraulic radius, ft
    n = culvert.section.ne(d)                 # Manning's coefficient
    Kn = culvert.section.Kn                   # Unit conversion parameter
    g = culvert.section.g                     # Acceleration of gravity
    
    # Get the major loss parameter using Manning's n
    Km = 2. * g * n**2 * L / (Kn**2 * R**(4./3.))
    
    # Compute Q from equation (6.15b)
    Q = A * np.sqrt((2. * g * (hw - tw + S * L)) / (1. + Ke + Km))
    
    return Q        

def reservoir_inflow(hw, culvert, S, Ke):
    """
    Solve the reservoir inflow problem for inflow to a culvert
    
    Solve the reservoir inflow problem assuming a mild slope for flow into 
    a culvert.  Take care to estimate when the culvert will be submerged.
    
    Returns
    -------
    Q : float
        Flow rate at the entrance based on reservoir inflow, cfs
    y0 : float
        Water depth at the inlect section computed as normal depth, cfs
    
    """
    # Extract some channel properties from the section object
    d = culvert.section.d                     # Diameter, ft
    n = culvert.section.ne(d)                 # Manning's coefficient
    Kn = culvert.section.Kn                   # Unit conversion parameter
    g = culvert.section.g                     # Acceleration of gravity
    
    # Compute the residual of the total head at the entrance
    def residual(y):
        """
        Residual of the total head equation at the inlet
        
        """
        # Compute the hydraulic radius at the present depth
        R = culvert.section.hydraulic_radius(y)
        
        return hw - (y + (1. + Ke) * Kn**2 / (2. * g * n**2) * R**(4./3.) * S)
        
    # Find the inflow depth
    y0, ans, ier, mesg = fsolve(residual, d / 2., full_output=True)
    
    if ier == 1:
        # Compute Q from the inflow depth
        A = culvert.section.area(y0)
        R = culvert.section.hydraulic_radius(y0) 
        Q = Kn / n * A * R**(2./3.) * np.sqrt(S)
    else:
        y0 = np.nan
        Q = np.nan
        
    # Return the depth and flow rate
    return Q, y0

if __name__ == '__main__':
    
    
    # Culvert dimensions
    d = 3.      # Diameter, ft
    S = 0.02    # Slope, ft/ft
    n = 0.015   # Manning's coefficient
    tw = 1.5    # Outlet water depth, ft
    L = 150.    # Culvert length, ft
    
    # Create a cross-section and channel object with these parameter values
    culvert_section = ocf_tools.CircularSection(d, n, units=0)
    culvert = ocf_tools.OpenChannel(culvert_section)
    
    # Design parameters for Circular concrete square-edged headwall
    
    # Steep slope fit coefficients
    K = 0.0098  # K - Table 6.3
    M = 2.0     # M - Table 6.3
    c = 0.0398  # c - Table 6.3
    Y = 0.67    # Y - Table 6.3
    
    # Mild slope fit coefficients
    Ke = 0.5    # Ke - Table 6.5
    
    # Compute the different head water depths to develop performance curve
    hw = np.linspace(0.01, 3.0, num=30) * d
    
    # Create an array to hold the flow rates and flow class
    Q = np.zeros(hw.shape)
    flow_class = np.zeros(hw.shape)
    yc = np.zeros(hw.shape)
    yn = np.zeros(hw.shape)
    
    # Compute the performance curve
    for i in range(len(hw)):
        
        # Compute the flow rate
        Q[i], flow_class[i], yc[i], yn[i] = culvert_flow(
            hw[i], tw, culvert, S, K, M, c, Y, Ke, L, report=False)

    # Plot the performance curve
    plt.figure(1)
    plt.clf()
    
    ax = plt.subplot(211)
    ax.plot(Q, hw, '.-')
    ax.set_xlabel('Flow rate, cfs')
    ax.set_ylabel('Headwater depth, ft')
    
    ax = plt.subplot(212)
    ax.plot(flow_class, hw, '.')
    ax.set_xlabel('Flow type (1:IC-1, 2:IC-2, 3:OC-1, 4:OC-2)')
    ax.set_ylabel('Headwater depth, ft')
    
    plt.show()
    
    # Plot the normal and critical depths
    plt.figure(2)
    plt.clf()
    
    plt.plot(yc, hw, '.-', label='Critical depth')
    plt.plot(yn, hw, '.-', label='Normal depth')
    plt.xlabel('Depth, ft')
    plt.ylabel('Headwater depth, ft')
    plt.legend()

    plt.show()
     
    
    
    
    
        
    
    
    
