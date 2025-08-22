"""
storage_routing.py
==================

Solve the storage routing equation::

    dS/dt = I - O

using reservoir routing method.  This module imports the stage-discharge relationship from an Excel file, creates the required interpolation function
for::

    2S / dt + O

as a function stage, Z, and solves the ODE. The function `get_stage_discharge`
reads the Excel data file and returns an array with the following values as
columns: Z, S, O, 2S/dt + O. If the data are not provided by Excel, this
functoin can be replaced by code that generates the same array.

"""
# S. Socolofsky, Texas A&M University, November 2023, <socolofs@tamu.edu>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d

def get_stage_discharge(fname):
    """
    Read the stage-discharge data from Excel
    
    This function reads in the stage-discharge data from Excel using Pandas.
    For the main section of data, the column headers should be Z (stage, L), S
    (storage, L^3), and O (outflow, L^3/T). It is assumed that the first row
    of data under each header will be the units of each variable and that the
    data in the table start on the second row below the headers.
    
    Parameters
    ----------
    fname : str
        String file path and file name of the Excel file to read
    
    Returns
    -------
    res_data : ndarray
        A numpy array of reservoir stage-discharge data.  These data will be 
        returned with a different stage value (Z) for each row and with 
        columns organized as Z, S, and O.
    
    """
    # Read the Excel file
    df = pd.read_excel(fname, sheet_name='Sheet1')
    
    # Build the reservoir data array
    res_data = np.zeros((len(df['Z']) - 1, 3))
    res_data[:,0] = df['Z'][1:].to_numpy()
    res_data[:,1] = df['S'][1:].to_numpy()
    res_data[:,2] = df['O'][1:].to_numpy()
    
    return res_data

def get_inflow_hydrograph(fname):
    """
    Read in the inflow hydrograph in the provided file
    
    Read in the inflow hydrograph data from the provided Excel file, in which
    time (T) is in column 1 and the inflow (I) is in column 2.
    
    Parameters
    ----------
    fname : str
        String file path and file name of the Excel file to read
    
    Returns
    -------
    hydrograph_data : ndarray
        A numpy array of hydrogrfaph data.  These data will be returned with 
        a different time value for each row and with columns organized as
        T, I.  The time data will be converted to seconds.
        
    """
    # Read the Excel file
    df = pd.read_excel(fname, sheet_name='Sheet1')
    
    # Get the time units
    t_conv = 1.
    if 'hr' in df['T'][0]:
        t_conv = 3600.
    elif 'min' in df['T'][0]:
        t_conv = 60.
    
    # Build the hydrograph data array
    hydrograph_data = np.zeros((len(df['T']) - 1, 2))
    hydrograph_data[:,0] = df['T'][1:].to_numpy() * t_conv
    hydrograph_data[:,1] = df['I'][1:].to_numpy()
    
    return hydrograph_data
    
    
class ResRouter(object):
    """
    Create a simple class for performing reservoir routing
    
    Creates a simple class that allows the user perform reservoir routing
    on arrays of reservoir data and inflow hydrograph data.  The reservoir
    data should be stored with stage in the first column and the other 
    routing parameters (S, O, and 2S/dt + O) in the other columns; the 
    inflow hydrographs should be stored with time in the figure column and
    inflow rate in the second column.  The `route()` method performs the 
    routing simulation, and the plotting methods provide various displays
    of the data
    
    Parameters
    ----------
    res_data : ndarray
        An array of reservoir stage-discharge data with the stage (Z) in 
        the first column of data and storage (S), and outflow (O).
    inflow_data : ndarray
        An array of inflow hydrograph data with the time (T in s) in the first
        column and the inflow (I in units that agree with `res_data`) in the
        second column.
    col_names : list, default=['Z', 'S', 'O']
        A list of string names designating the variable in each column of the
        `res_data` array.  While the user can change the string names, the
        order of these data must always be the same as given here.
    
    """
    def __init__(self, res_data, inflow_data, 
        col_names=['Z', 'S', 'O']):
        super(ResRouter, self).__init__()

        # Save the original input data
        self.res_data = res_data
        self.inflow_data = inflow_data
        self.col_names = col_names
        
        # Build a 1d interpolator for the reservoir data
        self.res_fun = interp1d(res_data[:,0], res_data[:,1:], axis=0)
        
        # Create a dictionary of column indices for the res_fun data
        self.cols = {
            col_names[i] : i-1 for i in range(len(col_names))
        }
        
        # Build a 1d interpolator for the inflow data
        self.inflow = interp1d(inflow_data[:,0], inflow_data[:,1], 
            bounds_error=False, fill_value=0.)
        
        # Set the simulation flag to false
        self.sim_stored = False
        
    def get_res_values(self, z, var):
        """
        Get an interpolated result for variable `var` at a given stage `z`
        
        Interpolate the original `res_data` database at the stage `z` and
        return the result for the variable `var`.  If `var` is a list,
        return the corresponding value for each variable in the list.
        
        Parameters
        ----------
        z : float
            Stage level at which to interpolate the reservoir data
        var : str or list
            Variable name(s) for the dependent variables that should be 
            returned
        
        """
        # Make var be a list
        if isinstance(var, str):
            var = [var]
            
        # Get the interpolated data
        interp_data = self.res_fun(z)
        
        # Get the requested data to return
        ans = np.zeros(len(var))
        for i in range(len(var)):
            ans[i] = interp_data[self.cols[var[i]]]
        
        # Return the desired output variable(s)
        return ans
    
    def route(self, t0, z0, dt, tf=-1):
        """
        Route the hydrograph through the reservoir
        
        Route the current inflow hydrograph through the reservoir defined by
        the reservoir data with initial condition Z = z0 at T = t0 using a
        simulation time-step of dt. Note that the simulation time-step does
        not have to match the time-step used in the reservoir data or in the
        inflow hydrograph.
        
        Parameters
        ----------
        t0 : float
            Initial time of the simulation (s) corresponding to times in the
            inflow hydrograph data.
        z0 : float
            Initial stage in the reservoir (L)
        dt : float
            Time step (s) to use in the simulation
        tf : float, default=-1
            Final time to compute in the simulation.  If `tf` = -1, then the
            last time in the inflow hydrograph dataset will be used.  
        
        Returns
        -------
        t : ndarray
            An array of computed times (s)
        stage : ndarray
            An array of stage values at each time (L^3)
        outflow : ndarray
            An array of outflow rates at each time (L^3/s)
        
        """
        # Initialize the output variables to the initial condition
        t = [t0]
        stage = [z0]
        outflow = [self.get_res_values(z0, 'O')[0]]
        storage = self.get_res_values(z0, 'S')[0]
        
        # Create the LHS of equation (9.8)
        res_fac = 2. * self.res_data[:,1] / dt + self.res_data[:,2]
        
        # Create a interpolator for the reservoir factor
        sim_fun = interp1d(res_fac, self.res_data, axis=0)
        
        # Determine the stop time for the simulation
        if tf < 0:
            tf = self.inflow_data[-1,0]

        # Perform the simulation
        while t[-1] < tf:
            
            # Compute RHS of Equation (9.8)
            res_fac = self.inflow(t[-1]) + self.inflow(t[-1] + dt) + \
                2. * storage / dt - outflow[-1]
            
            # Find the new outflow from the res_fac using the res_data
            o2 = sim_fun(res_fac)[-1]
            
            # Find the new storage from the LHS of Equation (9.8) 
            s2 = (res_fac - o2) * dt / 2.
            
            # Get the new stage
            z2 = sim_fun(res_fac)[0]
            
            # Save the data at the new time-step
            t.append(t[-1] + dt)
            stage.append(z2)
            outflow.append(o2)
            storage = s2
        
        # Convert the output variables to arrays
        self.t = np.array(t)
        self.stage = np.array(stage)
        self.outflow = np.array(outflow)
        
        # Set the simulation flag to true
        self.sim_stored = True
         
        # Return the results
        return (self.t, self.stage, self.outflow)
    
    def check_sim(self):
        """
        Check if the simulation data exist and report and error as needed

        """
        if self.sim_stored:
            return True
        
        else:
            print('\nError:  You need to complete a simulation before using')
            print('        this method.  Run the method route() first.\n')
            return False
    
    def plot_inflow(self, fig=1, clear=True):
        """
        Plot the inflow hydrograph
        
        Parameters
        ----------
        fig : int
            Figure number to use to plot
        clear : bool
            Flag indicating whether or not to clear the figure before 
            plotting
        
        """
        # Check if the sim data exist
        if not self.check_sim():
            return
            
        # Create a figure
        plt.figure(fig)
        if clear:
            plt.clf()
        
        # Plot the data
        plt.plot(self.inflow_data[:,0] / 3600., 
            self.inflow_data[:,1], label='Inflow')
        plt.xlabel('Time, hr')
        plt.ylabel('Q, L^3/s')
        plt.grid()
        plt.show()
    
    def plot_sim(self, fig, clear=True):
        """
        Plot the inflow and outflow hydrographs
        
        Parameters
        ----------
        fig : int
            Figure number to use to plot
        clear : bool
            Flag indicating whether or not to clear the figure before 
            plotting
        
        """
        # Check if the sim data exist
        if not self.check_sim():
            return
        
        # Plot the inflow hydrograph
        self.plot_inflow(fig, clear)
        
        # Plot the outflow hydrograph
        plt.plot(self.t / 3600., self.outflow, '.-', label='Outflow')
        plt.legend()
        plt.show()
    
    def plot_sim_params(self, fig, clear=True):
        """
        Plot the inflow, outflow, stage, and storage as a function of time
        for the present simulation data
        
        Parameters
        ----------
        fig : int
            Figure number to use to plot
        clear : bool
            Flag indicating whether or not to clear the figure before 
            plotting
        
        """
        # Check if the sim data exist
        if not self.check_sim():
            return
        
        # Create a figure
        plt.figure(fig)
        if clear:
            plt.clf()
        
        # Create the default annotations
        def annotate(ax, xlabel, ylabel):
            """
            Add labels, etc. to plots consistently
            
            """
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid()
        
        # Plot each variable
        ax = plt.subplot(221)
        ax.plot(self.inflow_data[:,0] / 3600., self.inflow_data[:,1])
        annotate(ax, 'Time, hr', 'Inflow, L^3/s')
        
        ax = plt.subplot(222)
        ax.plot(self.t / 3600., self.outflow)
        annotate(ax, 'Time, hr', 'Outflow, L^3/s')
        
        ax = plt.subplot(223)
        ax.plot(self.t / 3600, self.stage)
        annotate(ax, 'Time, hr', 'Stage, L')
        
        ax = plt.subplot(224)
        ax.plot(self.t / 3600, self.res_fun(self.stage)[:,self.cols['S']])
        annotate(ax, 'Time, hr', 'Storage, L^3')
        
        # Set some final formatting things
        plt.tight_layout()
        plt.show()
        

if __name__ == '__main__':
    
    # Set up the simulation settings
    resdata_fname = 'Table_91.xlsx'
    hydrograph_fname = 'Inflow_hydrograph.xlsx'
    z0 = 0.     # Initial pool stage in reservoir
    t0 = 0.     # Initial time of the hydrograph
    dt = 0.1    # Timestep to use in the simulation (hr)
    
    # Read in the stage-discharge data from Excel...replace this with any other
    # function call or code that will generate the required res_data array if 
    # not using Excel.
    res_data = get_stage_discharge(resdata_fname)
    
    # Read in the inflow hydrograph data from Excel...replace this with any
    # other function call or code that will generage the required
    # hydrograph_data array if not using Excel.    
    hydrograph_data = get_inflow_hydrograph(hydrograph_fname)
    
    # Create the reservoir interpolator object
    reservoir = ResRouter(res_data, hydrograph_data)
    
    # Route the hydrograph through the reservoir
    t, z, outflow = reservoir.route(t0, z0, dt * 3600., 40*3600.)
    
    # Plot the default outputs
    reservoir.plot_sim(1)
    reservoir.plot_sim_params(2)
    
    
    