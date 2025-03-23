def apply_ai_actions(actions: dict, agent, terrain):
    """
    Applies actions like irrigation, reroute, and ventilation.
    Updates simulation state and returns a control status dict.
    """
    status_flags = {
        "irrigation": False,
        "rerouted": False,
        "ventilation": False
    }

    if actions.get("irrigate"):
        status_flags["irrigation"] = True
        print("AI Action: Irrigation turned ON")

    if actions.get("ventilate"):
        status_flags["ventilation"] = True
        print("AI Action: Ventilation triggered (virtual effect)")

    if actions.get("reroute"):
        new_goal = _find_new_goal(terrain, exclude=[agent.state] + list(terrain.obstacles))
        if new_goal:
            agent.goal = new_goal
            terrain.goal = new_goal
            status_flags["rerouted"] = True
            print(f"AI Action: Goal rerouted to {new_goal}")
        else:
            print("Reroute requested, but no valid goal found.")

    return status_flags


def _find_new_goal(terrain, exclude=[]):
    """
    Selects a new random goal position that's valid and not excluded.
    """
    from random import shuffle
    candidates = [(x, y) for x in range(terrain.width) for y in range(terrain.height)]
    shuffle(candidates)
    for pos in candidates:
        if pos not in exclude and terrain.is_valid(pos):
            return pos
    return None
