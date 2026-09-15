"""
efm_tools.py
============

Tools to calculate the analytical solutions used in Environmental Fluid 
Mechanics for the transport equation

"""
# S. Socolofsky, Texas A&M University, October 2024, <socolofs@tamu.edu>

import ocf_tools

import numpy as np
import matplotlib.pyplot as plt


def ips_1d(x, t, A, u, m, D):
    """
    Instantaneous point source in one dimension
    
    Parameters
    ----------
    x : float or ndarray
        Location to compute the concentration, L
    t : float or ndarray
        Time to compute the concentration, T
    A : float
        Cross-sectional area of the one-dimensional cross section, L^2
    u : float
        Advection velocity, L/T
    m : float
        Spilled mass, M
    D : float
        Effective longitudinal diffusion coefficient, L^2/T
    
    Returns
    -------
    C : float or ndarray
        Concentration at the selected `x` and `t` values, M/L^3
    
    """
    # Compute the analytical equation and return the result
    return m / (A * np.sqrt(4. * np.pi * D * t)) * np.exp(-(x - u * t)**2 / 
        (4. * D * t))
    
def ips_2d(x, y, t, H, u, v, m, Dx, Dy):
    """
    Instantaneous point source in two dimensions
    
    Parameters
    ----------
    x : float or ndarray
        Longitudinal coordinate to compute the concentration, L
    y : float or ndarray
        Transverse coordinate to compute the concentration, L
    t : float or ndarray
        Time to compute the concentration, T
    H : float
        Depth of the two-dimensional domain, L
    u : float
        Advection velocity in the longitudinal direction, L/T
    v : float
        Advection velocity in the transverse direction, L/T
    m : float
        Spilled mass, M
    Dx : float
        Effective longitudinal diffusion coefficient, L^2/T
    Dy : float
        Effective transverse diffusion coefficient, L^2/T
    
    Returns
    -------
    C : float or ndarray
        Concentration at the selected `x`, `y`, and `t` values, M/L^3
    
    """
    # Compute the analytical equation and return the result
    return m / (H * 4. * np.pi * t * np.sqrt(Dx * Dy)) * np.exp(
            -(x - u * t)**2 / (4. * Dx * t) - (y - v * t)**2 / (4. * Dy * t))

def first_order_rxn(c0, k, t):
    """
    Compute a first-order reaction
    
    Parameters
    ----------
    c0 : float or ndarray
        Initial, non-reacted concentration, M/L^3
    k : float
        Reaction rate constant, 1/T.  Positive values are used for die-off.
    t : float or ndarray
        Time to compute the reacted concentration, T
    
    Returns
    -------
    C : float
        Concentration following a first-order decay process, M/L^3
    
    """
    # Compute the analytical equation and return the result
    return c0 * np.exp(-k * t)

def isd_1d(c0, x, t, u, D):
    """
    Initial spatial distribution in one dimension
    
    Parameters
    ----------
    c0 : float
        Concentration value of the initial, uniform concentration 
        distribution, M/L^3
    x : float or ndarray
        Longitudinal coordinate to compute the concentration, L
    t : float or ndarray
        Time to compute the concentration, T
    u : float
        Advection velocity in the longitudinal direction, L/T
    D : float
        Effective longitudinal diffusion coefficient, L^2/T
    
    Returns
    -------
    C : float or ndarray
        Concentration at the selected `x` and `t` values, M/L^3
    
    """
    # Get the error function
    from scipy.special import erf
    
    # Compute the analytical equation and return the result
    return c0 / 2. * (1. - erf((x - u * t) / np.sqrt(4. * D * t)))

def fixed_conc(c0, x, t, D):
    """
    Fixed concentration boundary
    
    Parameters
    ----------
    c0 : float
        Fixed concentration value at a boundary, M/L^3
    x : float or ndarray
        Longitudinal coordinate to compute the concentration, L
    t : float or ndarray
        Time to compute the concentration, T
    D : float
        Effective longitudinal diffusion coefficient, L^2/T
    
    Returns
    -------
    c : float or ndarray
        Concentration at the selected `x` and `t` values, M/L^3
    
    """
    # Get the error function
    from scipy.special import erf
    
    # Compute the analytical equation and return the result
    return c0 * (1. - erf(x / (np.sqrt(4. * D * t))))

def line_source(mdp, x, y, u, Dy):
    """
    Continuous line source neglecting longitudinal diffusion
    
    Parameters
    ----------
    mdp : float
        Time rate of mass injection per unit length along the source, M/L/T
    x : float or ndarray
        Longitudinal coordinate to compute the concentration, L
    y : float or ndarray
        Lateral coordinate to compute the concentration, L
    u : float
        Advection velocity in the longitudinal direction, L/T.  This solution
        assumes there is no transverse advection velocity.
    Dy : float
        Effective lateral diffusion coefficient, L^2/T
    
    Returns
    -------
    c : float or ndarray
        Concentration at the selected `x`, `y`, and `t` values, M/L^3
    
    """
    # Return Equation (B.33) from Socolofsky and Jirka (2005)
    return mdp / np.sqrt(4. * np.pi * x * u * Dy) * np.exp(-u * y**2 / 
        (4. * Dy * x))

def sigma_c(D, t):
    """
    Width of a concentration distribution
    
    Parameters
    ----------
    D : float
        Effective diffusion coefficient, L^2/T
    t : float
        Time to compute the concentration width, T
    
    Returns
    -------
    sigma : float
        Concentration characteristic width, L
    
    """
    # Return the standard deviation of the Gaussian distribution
    return np.sqrt(2. * D * t)
    
def normal_flow(y, B, nb, S, units):
    """
    Compute the normal flow rate for a channel
    
    Compute the normal flow rate from Manning's equation for a channel with
    the given depth and geometry
    
    Parameters
    ----------
    y : float
        Water depth, L
    B : float
        Rectangual channel top width, L        
    nb : float
        Manning's coefficient for the channel, --
    S : float
        Channel slope, L/L
    units : int
        Flag indicating the unit system:  (0: U.S. Customary Units; 1: SI 
        units)
    
    Returns
    -------
    Qn : float
        Flow rate at the given normal depth, L^3/T
    
    """
    # Create a channel object
    xsec = ocf_tools.Section(nb, (B,), units)
    
    # Create an open-channel object
    channel = ocf_tools.OpenChannel(xsec)
    
    # Compute the normal flow rate
    return channel.manning_flow(y, S)

def normal_depth(Q, B, nb, S, units):
    """
    Compute the normal depth for a channel
    
    Compute the normal depth from Manning's equation for a channel with the
    given flow rate and geometry
    
    Parameters
    ----------
    Q : float
        Flow rate, L^3/T
    B : float
        Rectangual channel top width, L        
    nb : float
        Manning's coefficient for the channel, --
    S : float
        Channel slope, L/L
    units : int
        Flag indicating the unit system:  (0: U.S. Customary Units; 1: SI 
        units)
    
    Returns
    -------
    yn : float
        Normal depth at the given flow rate, L
    
    """
    # Create a channel object
    xsec = ocf_tools.Section(nb, (B,), units)
    
    # Create an open-channel object
    channel = ocf_tools.OpenChannel(xsec)
    
    # Compute the normal flow rate
    return channel.normal_depth(Q, S)
    
def dl_fischer(h, B, u, us=None):
    """
    Longitudinal dispersion coefficient after Fisher et al. (1979)
    
    Parameters
    ----------
    h : float
        Water depth, L
    B : float
        Channel width, L
    u : float
        Cross-sectional average velocity, L/T
    us : float, default=None
        Bottom shear velocity, L/T.  If `None`, then the shear velocity will
        be estimated as 0.15 u.
    
    Returns
    -------
    Dl : float
        Longitudinal dispersion coefficient, L^2/T
    
    """
    # Compute the shear velocity, if necessary
    if isinstance(us, type(None)):
        us = 0.15 * u
    
    # Return the result
    return 0.011 * u**2 * B**2 / (us * h)

def dl_deng(h, B, u, us=None):
    """
    Longitudinal dispersion coefficient after Deng et al. (2001)
    
    Parameters
    ----------
    h : float
        Water depth, L
    B : float
        Channel width, L
    u : float
        Cross-sectional average velocity, L/T
    us : float, default=None
        Bottom shear velocity, L/T.  If `None`, then the shear velocity will
        be estimated as 0.15 u.
    
    Returns
    -------
    Dl : float
        Longitudinal dispersion coefficient, L^2/T
    
    """
    # Compute the shear velocity, if necessary
    if isinstance(us, type(None)):
        us = 0.15 * u
    
    # Compute the equation
    et0 = 0.145 + 1. / 3520. * (u / us) * (B / h)**1.38
    Dl = 0.15 / (8. * et0) * (B / h)**(5./3.) * (u / us)**2 * us * h
    
    return Dl

def l_mix_side(L, u, D):
    """
    Distance for lateral mixing for a side injection
    
    Parameters
    ----------
    L : float
        Distance transverse to cross-section, L
    u : float
        Cross-sectional average velocity, L/T
    D : float
        Effective diffusion coefficient in the direction that lateral
        mixing is occurring
    
    Returns
    -------
    L_mix : float
        Downstream distance, L, at which a side injection can be considered
        well mixed.  If time is desired, convert to time using L = u t
    
    """
    return L**2 * u / (2. * D)

def l_mix_center(L, u, D):
    """
    Distance for lateral mixing for a centerline injection
    
    Parameters
    ----------
    L : float
        Distance transverse to cross-section, L
    u : float
        Cross-sectional average velocity, L/T
    D : float
        Effective diffusion coefficient in the direction that lateral
        mixing is occurring
    
    Returns
    -------
    L_mix : float
        Downstream distance, L, at which a centerline injection can be 
        considered well mixed.  If time is desired, convert to time using 
        L = u t
    
    """
    return L**2 * u / (8. * D)
    
    