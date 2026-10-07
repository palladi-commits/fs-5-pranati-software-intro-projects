#drag pt 3
#basic idea :while speeding up and while slowing down how air resistance affect the car 

'''Equations
- drag = 0.5 * cross sectional area * drag coefficient * air density * velocity^2
- net acceleration = acceleration - (drag / mass)
- velocity = velocity(previous) + net acceleration * time step'''

import matplotlib.pyplot as plt #??? --> create and control the graph (https://matplotlib.org/stable/tutorials/pyplot.html)
import matplotlib.animation as animation #??? --> animates the graph (https://matplotlib.org/stable/api/animation_api.html)
from dataclasses import dataclass

# fixed vars
cross_area = 1.2 
drag_coefficient = 0.7
air_density = 1.2
mass = 300
time_step = 0.05
steps_per_frame = 200  # took too long and crashed ->  each frame skips ahead 10 sim seconds

# changing vars
@dataclass
class State:
    time: float = 0.0
    acceleration: float = 0.0
    drag: float = 0.0
    net_acceleration: float = 0.0
    velocity: float = 0.0


def step(state: State) -> State:
    if state.time < 10: # for the first 10 seconds the car is accelerating
        state.acceleration = 5.0
    else: #after 10 seconds
        state.acceleration = 0.0 # the engine stop -> only drag acts on the car

    #all equations from above
    state.drag = 0.5 * cross_area * drag_coefficient * air_density * state.velocity ** 2
    state.net_acceleration = state.acceleration - (state.drag / mass)
    state.velocity = state.velocity + state.net_acceleration * time_step
    state.time += time_step

    return state


state = State()  # create the one State object that starts with all values at zero
times = []  #stores  time values -> plot it on the x-axis
velocities = []  #stores  velocity values -> plot it on the x-axis

def animate(i):
    global state
    for i in range(steps_per_frame):
        if state.time < 10 or state.velocity > 0.1:  # stop once coasting reaches 0.1 m/s
            state = step(state)
            times.append(state.time)
            velocities.append(state.velocity)

    ax.clear()
    ax.grid()
    #print(max(velocities), times[-1])
    ax.set_xlim(0, 6000)#--> graph the x-axis from 0 to 6000
    ax.set_ylim(0, 45)#--> graph the y-axis from 0 to 45
    ax.set_xlabel("time(s)")
    ax.set_ylabel("velocity(m/s)")
    ax.plot(times, velocities)

fig = plt.figure(figsize=(4, 3), dpi=150)
ax = fig.add_subplot(111)
ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False)
plt.show()