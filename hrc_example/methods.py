import gtpyhop
import actions

# defines single action methods for the cleaning dishes domain
# these aren't currently in use for the methods but should be useful once depth search is implemented
def m_robot_move(state, loc):
    if state.loc['robot'] != loc:
        return [('robot_move', loc)]

def m_robot_pickup(state, obj):
    if state.loc['robot'] == state.loc[obj] and state.robot_carrying is None:
        return [('robot_pickup', obj)]
    
def m_robot_putdown(state, obj):
    if state.robot_carrying == obj:
        return [('robot_putdown', obj)]
    
def m_robot_handover(state, obj):
    if state.loc['robot'] == state.loc['human'] and state.robot_carrying == obj and state.human_carrying is None:
        return [('robot_handover', obj)]
    
def m_robot_unstack(state, obj):
    if state.loc['robot'] == state.loc[obj] and state.stack[obj] and state.robot_carrying is None:
        return [('robot_unstack', obj)]
    
def m_human_move(state, loc):
    if state.loc['human'] != loc:
        return [('human_move', loc)]
    
def m_human_pickup(state, obj):
    if state.loc['human'] == state.loc[obj] and state.human_carrying is None:
        return [('human_pickup', obj)]
    
def m_human_putdown(state, obj):
    if state.human_carrying == obj:
        return [('human_putdown', obj)]
    
def m_human_handover(state, obj):
    if state.loc['human'] == state.loc['robot'] and state.human_carrying == obj and state.robot_carrying is None:
        return [('human_handover', obj)]
    
def m_human_dry(state, obj):
    if state.loc['human'] == state.loc[obj] and state.human_carrying == obj:
        return [('human_dry', obj)]
    
def m_huam_wash(state, obj): 
    if state.loc['human'] == state.loc['sink'] and state.human_carrying == obj:
        return [('human_wash', obj)]

# higher level methods for the cleaning dishes domain

def robot_move_plate(state, loc, obj):
    if state.loc['robot'] != loc and state.loc[obj] == loc:
        location = state.loc[obj]
        return [('robot_move', location), ('robot_pickup', obj), ('robot_move', loc), ('robot_putdown', obj)]


def m_handoff_plate(state, obj, g):
    if state.loc['robot'] == state.loc['human'] and state.robot_carrying == obj and state.human_carrying is None:
        return [('robot_handover', obj)]


def m_clean_given_plate(state, obj, g):
    """
    Get the plate and hand it to the human to wash
    """
    if state.robot_carrying == None and state.human_carrying == None and state.plate_dirty[obj] == True \
    and state.loc[obj] in state.locations and state.plate_fragile[obj] == False:
        return [('robot_move', state.loc[obj]), ('robot_pickup', obj), ('robot_move', state.loc['human']), ('robot_handover', obj), ('human_move', 'sink'),
               ('human_wash', obj), ('human_dry', obj)]
    return False


def m_clean_plate(state, obj, g):
    if state.loc[obj] == 'human' and state.human_carrying == obj:
        return [('human_clean', obj), ('human_dry', obj)]
    return False


def m_human_clean_plate(state, obj, g):
    if state.human_carrying == None and state.plate_dirty[obj] == True:
        return [('human_move', state.loc[obj]), ('human_pickup', obj), ('human_move', 'sink'), ('human_wash', obj), ('human_dry', obj)]
    return False


def m_unstack_plates(state, obj, g):
    top_plate = actions.get_top_plate(state, obj)
    location = actions.get_plate_loc(state, obj)

    unstack_calls = []
    
    if state.loc['robot'] != location:
        unstack_calls.append(('robot_move', location))
    
    if state.robot_carrying is None and (state.plate_stack[obj] is not None or state.loc[obj] != location):
        
        unstack_calls = []
        
        while state.loc[top_plate] != location:
            unstack_calls.append(('robot_unstack', top_plate))
            top_plate = state.loc[top_plate]
            
        return unstack_calls
    
    return False


gtpyhop.declare_unigoal_methods('plate_dirty', m_unstack_plates, m_clean_given_plate, m_clean_plate, m_human_clean_plate)
gtpyhop.declare_unigoal_methods('loc', m_unstack_plates, m_clean_given_plate, m_clean_plate, m_robot_move, m_human_move)
gtpyhop.declare_unigoal_methods('robot_carrying', m_robot_pickup, m_robot_putdown, m_robot_handover, m_robot_unstack)
gtpyhop.declare_unigoal_methods('human_carrying', m_human_pickup, m_human_putdown, m_human_handover)
gtpyhop.declare_unigoal_methods('plate_stack', m_unstack_plates)


# did not test this yet so i'd recommend using unigoals for testing
def m_get_plate_goals(state, mg):
    plates = [p for p in mg.plate_dirty if mg.plate_dirty[p] == True]
    return [('plate_dirty', plate, mg.plate_dirty[plate]) for plate in p]
    

gtpyhop.declare_multigoal_methods(m_get_plate_goals)