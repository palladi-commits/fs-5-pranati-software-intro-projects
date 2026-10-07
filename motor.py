#motor model pt 4
#basic idea: why does car have a top speed

'''Equations
- propulsion force = max propulsion force * throttle input * (1 - (velocity / max velocity))
- acceleration = force / mass
- velocity = velocity(previous) + acceleration * time step'''


import matplotlib.pyplot as plt #??? --> create and control the graph (https://matplotlib.org/stable/tutorials/pyplot.html)
import matplotlib.animation as animation #??? --> animates the graph (https://matplotlib.org/stable/api/animation_api.html)
from dataclasses import dataclass

# fixed vars
max_force = 2000
max_velocity = 27
mass = 300
time_step = 0.05

# changing vars
@dataclass
class State:
    time: float = 0.0
    throttle: float = 0.0
    force: float = 0.0
    acceleration: float = 0.0
    velocity: float = 0.0

def step(state: State) -> State:
    if state.time <= 3: # during the first 3 seconds the driver is pressing the pedal down
        state.throttle = state.time / 3
    else: # after 3 seconds
        state.throttle = 1.0 # held at full throttle

    state.force = max_force * state.throttle * (1 - (state.velocity / max_velocity))
    state.acceleration = state.force / mass #rearrange force equation --> only need acceleration
    state.velocity = state.velocity + state.acceleration * time_step
    state.time += time_step

    return state

state = State()  # create the one State object that starts with all values at zero
times = []  #stores every time value --> plot it on the x-axis
velocities = []  #stores every time value --> plot it on the x-axis

def animate(i):
    global state
    if state.time < 23:  # keep simulating until 23 seconds (3+20(holding))
        state = step(state)
        times.append(state.time)
        velocities.append(state.velocity)

    ax.clear()
    ax.grid()
    ax.set_xlim(0, 23)
    ax.set_ylim(0, 30)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("velocity (m/s)")
    ax.plot(times, velocities)

fig = plt.figure(figsize=(4, 3), dpi=150)
ax = fig.add_subplot(111)
ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False)
plt.show()