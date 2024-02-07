import gtpyhop

the_domain = gtpyhop.Domain(__package__)

from methods import *
from actions import *


if __name__ == '__main__':
    gtpyhop.current_domain = the_domain
    gtpyhop.print_domain()
    
    # create a state for the diswashing scenario
    state = gtpyhop.State('state')
    
    # sets to keep track of plate names and locations
    state.plates = {'plate1', 'plate2', 'plate3', 'plate4'}
    state.locations = {'island', 'sink', 'dishrack', 'counter'}
    
    # easy version of the domain
    # For stacked plates, the location of the plate is the plate below it. The plate_stack entry points to the plate above it.
    state.loc = {'human':'sink', 'robot':'island', 'plate1':'island', 'plate2':'island', 'plate4':'counter', 'plate3':'counter'}
    state.plate_stack = {'plate1': None, 'plate2': None, 'plate3': None, 'plate4': None}

    # 
    state.plate_fragile = {'plate1':False, 'plate2':True, 'plate3':False, 'plate4':False}
    state.plate_dirty = {'plate1':True, 'plate2':True, 'plate3':True, 'plate4':True}

    state.robot_carrying = None
    state.human_carrying = None

    # note this is only a partial state for planning, the plan runner will keep track of additional variables 
    # like the current human action (if the human action doesn't match the planner, it'll trigger an event response)
    
    gtpyhop.verbose = 3
    
    print("Plan to clean all the plates")
    goal = [('plate_dirty', 'plate1', False), ('plate_dirty', 'plate2', False), ('plate_dirty', 'plate3', False), ('plate_dirty', 'plate4', False)]
    
    gtpyhop.find_plan(state, goal)
    
    print("""
          
          Plan to clean plates with unstacking
          
          """)
    
    # hard version, should fail without search
    state.loc = {'human':'sink', 'robot':'island', 'plate1':'island', 'plate2':'plate1', 'plate4':'counter', 'plate3':'counter'}
    state.plate_stack = {'plate1': 'plate2', 'plate2': None, 'plate3': None, 'plate4': None}
    
    # Can succeed if the goal is updated and ordered correctly to unstack the plates first (But ideally we want the planner to be able to figure this out on its own)
    # goal = [('plate_stack', 'plate1', None), ('plate_dirty', 'plate2', False), ('plate_dirty', 'plate1', False),  ('plate_dirty', 'plate3', False), ('plate_dirty', 'plate4', False)]
    
    #gtpyhop.find_plan(state, goal)
    
