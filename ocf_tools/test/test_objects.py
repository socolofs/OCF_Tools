"""
test_objects.py
---------------

Test that the main model classes exist and can be used to create object 
variables.

"""
# S. Socolofsky, June 2025, Texas A&M University, <socolofs@tamu.edu>

import ocf_tools
from ocf_tools import culvert_tools
from ocf_tools import storage_routing
from ocf_tools import ocf_tools

import types

def test_exists():
    """
    Check that the `ocf_tools` module can be imported
    
    """
    assert isinstance(ocf_tools, types.ModuleType) == True

def test_works():
    """
    Check that the 'ocf_tools' objects can be created
    
    """
    # Check for the existance of the culvert_tools main functions
    assert hasattr(culvert_tools, 'culvert_flow')
    assert hasattr(culvert_tools, 'Q_ic_1')
    assert hasattr(culvert_tools, 'Q_ic_2')
    assert hasattr(culvert_tools, 'Q_oc_1')
    assert hasattr(culvert_tools, 'reservoir_inflow')
    
    # Check for the existance of the storage_routing objects and functions
    assert hasattr(storage_routing, 'get_stage_discharge')
    assert hasattr(storage_routing, 'get_inflow_hydrograph')
    assert hasattr(storage_routing, 'ResRouter')
    
    # Check for the existance of the ocf_tools objects and functions
    assert hasattr(ocf_tools, 'Section')
    assert hasattr(ocf_tools, 'TrapSection')
    assert hasattr(ocf_tools, 'TriangularSection')
    assert hasattr(ocf_tools, 'CircularSection')
    assert hasattr(ocf_tools, 'ParabolicSection')
    assert hasattr(ocf_tools, 'OpenChannel')
    assert hasattr(ocf_tools, 'gvf_derivs')
    assert hasattr(ocf_tools, 'compute_gvf_profile')
    

