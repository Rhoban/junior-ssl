import numpy as np 

# Field dimension
length = 1.83  # x axis
width = 1.22   # y axis

# Width of the goal
goal_width = 0.6

# Side of the (green) border we should be able to see around the field
border_size = 0.3

# Field coordinates 
def fieldCoord() -> np.ndarray:
    field_coord = [[],[],[],[]]
    for sign, i in [(1,0), (-1,2)]:
        C = [sign*(length / 2.), sign*width / 2.]
        D = [sign*(length / 2.), -sign*width / 2.]
        field_coord[i] = C
        field_coord[i+1] = D
    return field_coord

# Goals coordinates
def goalsCoord(goals_color: str) -> np.ndarray:
    goals_coord = [[],[],[],[]]
    for sign, i in [(-1, 0), (1, 2)]:
        A = [sign*(length / 2.), -sign*goal_width / 2.]
        B = [sign*(length / 2.), sign*goal_width / 2.]
        goals_coord[i] = A
        goals_coord[i+1] = B
    green_goals_coord = np.array([goals_coord[0],goals_coord[1]])
    blue_goals_coord =  np.array([goals_coord[2],goals_coord[3]])
    if goals_color == "green":
        return green_goals_coord
    elif goals_color == "blue":
        return blue_goals_coord