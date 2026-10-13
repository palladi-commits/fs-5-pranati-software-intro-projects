#braking pt 5
#basic idea: to stop from 25 m/s how long does it take 

'''Equations
- braking force = driver input * max braking capacity
- acceleration = - (braking force / mass)
- velocity = velocity(previous) + acceleration * time step'''

#0-2 sec = cruising at 25 m/s (no braking), after 2 sec = full braking until stopped

import matplotlib.pyplot as plt #??? --> create and control the graph (https://matplotlib.org/stable/tutorials/pyplot.html)
import matplotlib.animation as animation #??? --> animates the graph (https://matplotlib.org/stable/api/animation_api.html)
from dataclasses import dataclass

# fixed vars
max_braking = 1850
mass = 300
time_step = 0.05

# changing vars
@dataclass
class State:
    time: float = 0.0
    driver_input: float = 0.0
    braking_force: float = 0.0
    acceleration: float = 0.0
    velocity: float = 25.0


def step(state: State) -> State:
    if state.time < 2: # for the first 2 seconds the car is just cruising
        state.driver_input = 0.0  
    else:  # after 2 seconds
        state.driver_input = 1.0 # full braking

    state.braking_force = state.driver_input * max_braking
    state.acceleration = -(state.braking_force / mass)
    state.velocity = state.velocity + state.acceleration * time_step
    if state.velocity < 0:  # car no reverse
        state.velocity = 0.0 # set it to zero --> the car shouldnt move backwards
    state.time += time_step

    return state

state = State()  # create the one State object that starts with all values at zero
times = []  #stores every time value --> plot it on the x-axis
velocities = []  #stores every time value --> plot it on the x-axis

def animate(i):
    global state
    if state.velocity > 0:  # stop sim once the car is stopped
        state = step(state)
        times.append(state.time)
        velocities.append(state.velocity)

    ax.clear()
    ax.grid()
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 30)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("velocity (m/s)")
    ax.plot(times, velocities)

fig = plt.figure(figsize=(4, 3), dpi=150)
ax = fig.add_subplot(111)
ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False)
plt.show()