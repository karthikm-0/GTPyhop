import gtpyhop

######## helpers ########

def get_plate_loc(state, obj):
    """ Returns a stacked object's core location """
    loc = state.loc[obj]
    while loc not in state.locations:
        loc = state.loc[loc]
    return loc


def get_top_plate(state, plate):
    """ Returns the top plate in a stack """
    top_plate = plate
    while state.plate_stack[top_plate] is not None:
        top_plate = state.plate_stack[top_plate]
    return top_plate


########## robot actions ###########

def robot_move(state, loc, robot='robot'):
    if state.loc[robot] != loc:
        state.loc[robot] = loc
        return state
    return state


def robot_pickup(state, obj, robot='robot'):
    if state.loc[robot] == state.loc[obj] and state.robot_carrying is None:
        state.robot_carrying = obj
        state.loc[obj] = robot
        return state
    return False


def robot_putdown(state, obj, robot='robot'):
    if state.robot_carrying == obj:
        state.loc[obj] = state.loc[robot]
        state.robot_carrying = None
        return state
    return False


def robot_handover(state, obj, robot='robot', human='human'):
    if state.loc[robot] == state.loc[human] and state.robot_carrying == obj and state.human_carrying is None:
        state.robot_carrying = None
        state.human_carrying = obj
        return state
    return False


def robot_unstack(state, obj, robot='robot'):
    # top plate on stack only
    plate_loc = get_plate_loc(state, obj)
    if state.loc[robot] == plate_loc and state.robot_carrying is None and state.plate_stack[obj] is None:
        plate_below = state.loc[obj]
        state.loc[obj] = get_plate_loc(state, obj)
        state.plate_stack[plate_below] = None
        return state
    return False

########### human actions ###########

def human_move(state, loc, human='human'):
    if state.loc[human] != loc:
        state.loc[human] = loc
        return state
    return state


def human_pickup(state, obj,  human='human'):
    if state.loc[human] == state.loc[obj] and state.human_carrying is None:
        state.human_carrying = obj
        state.loc[obj] = human
        return state
    return False


def human_putdown(state, obj,  human='human'):
    if state.human_carrying == obj:
        state.loc[obj] = state.loc[human]
        state.human_carrying = None
        return state
    return False


def human_handover(state, obj, robot='robot', human='human'):
    if state.loc[human] == state.loc[robot] and state.human_carrying == obj and state.robot_carrying is None:
        state.robot_carrying = obj
        state.human_carrying = None
        return state
    return False


def human_wash(state, obj, human='human'):
    if state.loc[human] == 'sink' and state.human_carrying == obj:
        state.plate_dirty[obj] = False
        return state
    return False


def human_dry(state, obj, human='human'):
    if state.loc[human] == 'sink' and state.human_carrying == obj:
        state.human_carrying = None
        state.loc[obj] = 'dishrack'
        return state
    return False


gtpyhop.declare_actions(robot_move, robot_pickup, robot_putdown, robot_handover, robot_unstack, human_move, human_pickup, human_putdown, human_handover, human_wash, human_dry)