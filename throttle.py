#throttle pt 1

#basic idea:when the driver presses the gas how fast does car speed up 


'''Equations
- command torque = driver input * max motor torque
- force at wheels = (command torque * gear ratio) / wheel radius
- acceleration = force / mass
- velocity = velocity(previous) + acceleration * time step'''


import matplotlib.pyplot as plt #??? --> create and control the graph (https://matplotlib.org/stable/tutorials/pyplot.html)
import matplotlib.animation as animation #??? --> animates the graph (https://matplotlib.org/stable/api/animation_api.html)
from dataclasses import dataclass

# fixed vars
max_torque = 180
mass = 300
gear_ratio = 3
wheel_radius = 0.216
time_step = 0.05

# changing vars
@dataclass
class State:
    time: float = 0.0  # time in seconds
    driver_input: float = 0.0
    command_torque: float = 0.0
    force: float = 0.0
    acceleration: float = 0.0
    velocity: float = 0.0

def step(state: State) -> State:
    if state.time <= 7:
        state.driver_input = state.time / 7
         #ramps the pedal in a straight line 0.0 to 1.0
    elif state.time <=22:
        state.driver_input = 1.0  # the pedal is held at full throttle
    else:
        state.driver_input =0.0

    state.command_torque = state.driver_input * max_torque
    state.force = (state.command_torque * gear_ratio) / wheel_radius
    state.acceleration = state.force / mass
    state.velocity = state.velocity + state.acceleration * time_step
    state.time += time_step

    return state  # hand the updated state back


state = State()  # create the one State object that starts with all values at zero
times = []  #stores  time values -> plot it on the x-axis
velocities = []  #stores  velocity values -> plot it on the x-axis

def animate(i):
    global state #lets animate change the state variable outside it
    if state.time < 22:  # 7s + 15s
        state = step(state) #saves result
        times.append(state.time) #puts in array and saves moment of time to plot on the graph
        velocities.append(state.velocity) #puts in array and saves the moment's speed to plot on the graph

    ax.clear()
    ax.grid() # draw grid lines -> easier to read
    ax.set_xlim(0, 22) #x-axis from 0 to 22 
    ax.set_ylim(0, 170)#y-axis from 0 to 170
    ax.set_xlabel("time (s)")
    ax.set_ylabel("velocity (m/s)")
    ax.plot(times, velocities)

fig = plt.figure(figsize=(4, 3), dpi=150) #create the window thats 4x3 inches at 150 dots per inch
ax = fig.add_subplot(111)
ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False)
plt.show()