#traction pt 2
#basic idea:how much does car slide sideways when you turm wheel


'''Equations
- slip angle = steer angle - (lateral velocity / forward speed)
- lateral force = - cornering stiffness * slip angle
- lateral acceleration = lateral force / mass
- lateral velocity = lateral velocity(previous) + (lateral acceleration * 0.5)'''


import matplotlib.pyplot as plt  
#??? --> create and control the graph (https://matplotlib.org/stable/tutorials/pyplot.html)
import matplotlib.animation as animation 
#??? --> animates the graph (https://matplotlib.org/stable/api/animation_api.html)
from dataclasses import dataclass
import numpy as np 
#??? --> mathemathical functions

# fixed vars
forward_speed = 15
cornering_stiffness = 36000
mass = 300
time_step = 0.05

# changing vars
@dataclass
class State:
    time = 0.0
    steer_angle = 0.0
    slip_angle = 0.0
    lateral_force = 0.0
    lateral_acceleration = 0.0
    lateral_velocity = 0.0
    lateral_position = 0.0 

state = State()

def step (state:State) -> State: #?? --> means the function takes a State as input and returns an updated State
    if state.time <= 3: # during the first 3 seconds driver is turning wheel
        state.steer_angle = (state.time / 3) * 5
    else:
        state.steer_angle = 5

    #radians
    convert_radians = state.steer_angle * np.pi / 180

    # all the eqations given
    state.slip_angle = convert_radians - (state.lateral_velocity / forward_speed)
    state.lateral_force =cornering_stiffness * state.slip_angle   # doesnt work w the negative sign so converted to postive
    state.lateral_acceleration = state.lateral_force / mass #equation switched up because need to find acceleratrion
    state.lateral_velocity = state.lateral_velocity + state.lateral_acceleration * time_step # new sideways speed = old + gained speed thing
    state.lateral_position = state.lateral_position + state.lateral_velocity * time_step #same thing for distance
    state.time += time_step

    return state

def animate (_):
    global state
    if state.time < 10: # 3s+7s holding
        state = step(state)

    ax.clear()
    ax.grid()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 12)
    ax.plot(0, state.lateral_position, "o") # draw the car as a dot at sideways position


#??? -->  set up the graph and animation
fig = plt.figure(figsize=(3,3), dpi=150)  #create the window thats 3x3 inches at 150 dots per inch
ax = fig.add_subplot(111) 
ax.grid()
ax.set_xlim(-2, 2) #--> graph the x-axis from -2 to 2
ax.set_ylim(-1, 12)#--> graph the x-axis from -1 to 12
# these lines are so the animation doesnt zoom in or out
ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False)
plt.show()