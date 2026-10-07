# pt6: BRAKING WITH AIR DRAG
# pt5 only used the brake force. In real life, air drag also pushes against the car and helps it slow down.

'''Equations
- drag = 0.5 * area * drag coefficient * air density * velocity^2
- braking force = driver input * max braking capacity
- acceleration = - (braking force + drag) / mass
- velocity = velocity(previous) + acceleration * time step'''

import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
from dataclasses import dataclass 

# fixed vars from pt 5
max_braking = 1850  
mass = 300  
time_step = 0.05  

# fixed vars from pt 3 (air drag)
cross_area = 1.2  
drag_coefficient = 0.7 
air_density = 1.2  

# changing vars 
@dataclass  
class State:  
    time: float = 0.0 
    driver_input: float = 0.0  
    braking_force: float = 0.0 
    drag: float = 0.0  
    acceleration: float = 0.0 
    velocity: float = 25.0 
    distance: float = 0.0 

state = State()  
times = []  
velocities = [] 

def step(state: State) -> State:  
    if state.time < 2:  # for the first 2 seconds the car is just cruising
        state.driver_input = 0.0  
    else: 
        state.driver_input = 1.0  # full braking

    state.drag = 0.5 * cross_area * drag_coefficient * air_density * state.velocity ** 2 
    state.braking_force = state.driver_input * max_braking  
    state.acceleration = -(state.braking_force + state.drag) / mass  
    state.velocity = state.velocity + state.acceleration * time_step 
    if state.velocity < 0:
        state.velocity = 0.0  # set it to zero, since the car should not move backwards
    state.distance = state.distance + state.velocity * time_step  # distance = old distance + speed * time
    state.time += time_step 

    return state  

def animate(i):  
    global state  
    if state.velocity > 0:  # keep going until the car has stopped
        state = step(state)  
        times.append(state.time)  
        velocities.append(state.velocity)  

    ax.clear()  
    ax.grid() 
    ax.set_xlim(0, 8)  #x-axis from 0 to 8 s so the graph doesn't zoom
    ax.set_ylim(0, 30)  #y-axis from 0 to 30 m/s so the graph doesn't zoom
    ax.set_xlabel("time(s)") 
    ax.set_ylabel("velocity(m/s)") 
    ax.plot(times, velocities)  # draw the car's speed as a line

fig = plt.figure(figsize=(4, 3), dpi=150) 
ax = fig.add_subplot(111) 
ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False) 
plt.show()  