"""
weir_tools.py
-------------

Functions to compute weir formulas from Sturm (2021), Section 2.8

"""
# S. Socolofsky, Texas A&M University, July 2025, <socolofs@tamu.edu>

import numpy as np


def sharp_crested_weir(H, P, L, units=0):
    """
    Sharp-Crested, Rectangual Notch Weir
    
    Discharge formula for the sharp-crested, rectangular notch weir, given
    by Equation (2.39) in Sturm (2021).  This function only implements a 
    suppressed weir, in which the notch width equals the channel width.
    
    Parameters
    ----------
    H : float
        Head above the notch in the unperturbed upstream flow, L
    P : float
        Height of the notch crest above the channel bottom, L
    L : float
        Length of the notch, L
    units : int, default=0
        Unit system (0 : U.S. Customary Units (ft, s), 1 : SI units (m, s))
    
    Returns
    -------
    Q : float
        Discharge, L^3/s
    
    Notes
    -----
    This function computes the updated value of Cd in Equation (2.42) based
    on the Pugh et al. (J. Hydraulic Engineering, Vol 4, 2023) interpretation
    of the original Kindsvater & Carter (1957) paper and data such that::
    
        Cd = 0.602 + 0.075 (H/P)
    
    Otherwise, this function follows Sturm (2021).
    
    """
    # Set the unit system
    if units == 0:
        g = 32.2   # ft/s^2
    else:
        g = 9.81   # m/s^2
    
    # Compute the discharge coefficient from the modified Equation (2.42)
    Cd = 0.602 + 0.075 * (H / P)
    
    # Compute Equation (2.39)
    Q = 2. / 3. * np.sqrt(2. * g) * Cd * L * H**(3./2.)
    
    return Q

def broad_crested_weir(H, P, L, l, units=0):
    """
    Broad-crested weir
    
    Discharge formula for the broad-crested weir, given by Equation (2.47)
    in Sturm (2021).  This function only implements the truly broad-crested
    version with Cd = 0.848.  It does check for being broad and return an 
    error if the weir is short-crested.
    
    Parameters
    ----------
    H : float
        Head above the notch in the unperturbed upstream flow, L
    P : float
        Height of the notch crest above the channel bottom, L
    L : float
        Length of the notch, L
    l : float
        Length of the weir in the flow direction, L
    units : int, default=0
        Unit system (0 : U.S. Customary Units (ft, s), 1 : SI units (m, s))
    
    Returns
    -------
    Q : float
        Discharge, L^3/s
    
    """
    # Set the unit system
    if units == 0:
        g = 32.2   # ft/s^2
    else:
        g = 9.81   # m/s^2
    
    # Check for broad-crested weir status
    if H / l > 0.33 and H / L < 1.5:
        print('\nERROR:  This is a short-crested weir.\n')
        return np.nan
    elif H / l > 1.5:
        print('\nWARNING:  This is a sharp-crested weir.  Using the formula')
        print('          for a suppressed, sharp-crested, rectangular weir\n')
        return sharp_crested_weir(H, P, L, units)
    elif H / l > 0.08 and H / l < 0.33:
        # Check the H versus P criteria
        if H / (H + P) > 0.35:
            val = H / (H + P)
            print(f'\nERROR:  The ratio H / (H + P) = {val:.2f} exceeds 0.35.')
            print('        This condition is not permitted for the equations')
            print('        in Sturm (2021).\n')
            return np.nan
        
        # This is the broad-cresed weir...define some variables
        Cd = 0.848
        As = L * H
        A1 = L * (H + P)
        
        # Set up an equation to find Cv
        def residual(Cv):
            """
            Residual of Equation (2.48) to evaluate Cv
            
            """
            return Cd * As / A1 - np.sqrt(Cv**(2./3.) - 1) / (0.385 * Cv)
        
        # Seek Cv
        from scipy.optimize import fsolve
        Cv = fsolve(residual, 1.)[0]
        
        # Solve equation (2.47)
        Q = Cv * Cd * 2./3. * np.sqrt(2./3. * g) * L * H**(3./2.)
        
        return Q
        
    else:
        print(f'\nERROR:  This condition of H/l = {H/l:.3f} cannot be handled')
        print('        by the weir equations in Sturm (2021)\n')
        return np.nan
        
    
    