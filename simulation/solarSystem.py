import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from poliastro.bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune

# create objects for the sun and planets
sun = Sun()
mercury = Mercury()
venus = Venus()
earth = Earth()
mars = Mars()
jupiter = Jupiter()
saturn = Saturn()
uranus = Uranus()
neptune = Neptune()

# create a figure and an axes for the plot
fig, ax = plt.subplots()

# set the title and axis labels of the plot
ax.set_title("Solar System")
ax.set_xlabel("x (km)")
ax.set_ylabel("y (km)")

# create lines for the sun and planets
sun_line, = ax.plot([0], [0], "o", color="orange")
mercury_line, = ax.plot([], [], "o", color="gray")
venus_line, = ax.plot([], [], "o", color="yellow")
earth_line, = ax.plot([], [], "o", color="blue")
mars_line, = ax.plot([], [], "o", color="red")
jupiter_line, = ax.plot([], [], "o", color="brown")
saturn_line, = ax.plot([], [], "o", color="gold")
uranus_line, = ax.plot([], [], "o", color="cyan")
neptune_line, = ax.plot([], [], "o", color="green")

# create a list of lines for the planets
planet_lines = [mercury_line, venus_line, earth_line, mars_line, jupiter_line, saturn_line, uranus_line, neptune_line]

# create a function that updates the plot at each frame
def update_plot(frame):
    # calculate the positions of the sun and planets at the current frame
    sun_pos = sun.orbit.propagate(frame).r
    mercury_pos = mercury.orbit.propagate(frame).r
    venus_pos = venus.orbit.propagate(frame).r
    earth_pos = earth.orbit.propagate(frame).r
    mars_pos = mars.orbit.propagate(frame).r
    jupiter_pos = jupiter.orbit.propagate(frame).r
    saturn_pos = saturn.orbit.propagate(frame).r
    uranus_pos = uranus.orbit.propagate(frame).r
    neptune_pos = neptune.orbit.propagate(frame).r

    # update the lines with the new positions
    sun_line.set_data(sun_pos[0], sun_pos[1])
    mercury_line.set_data(mercury_pos[0], mercury_pos[1])
    venus_line.set_data(venus_pos[0], venus_pos[1])
    earth_line.set_data(earth_pos[0], earth_pos[1])
    mars_line.set_data(mars_pos[0], mars_pos[1])
    jupiter_line.set_data(jupiter_pos[0], jupiter_pos[1])
    saturn_line.set_data(saturn_pos[0], saturn_pos[1])
    uranus_line.set_data(uranus_pos[0], uranus_pos[1])
    neptune_line.set_data(neptune_pos[0], neptune_pos[1])

    # create an animation object using the update function


anim = FuncAnimation(fig, update_plot, frames=365, interval=20)

# display the animation
plt.show()
