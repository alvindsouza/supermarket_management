import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

# Pendulum rod lengths (m), bob masses (kg).
L1, L2 = 1, 1
m1, m2 = 1, 1
# The gravitational acceleration (m/s^2).
g = 9.81

def deriv(y, t, L1, L2, m1, m2):
    """Return the first derivatives of y = theta1, z1, theta2, z2."""
    theta1, z1, theta2, z2 = y
    c, s = np.cos(theta1 - theta2), np.sin(theta1 - theta2)
    theta1dot = z1
    z1dot = (m2*g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) -
             (m1+m2)*g*np.sin(theta1)) / (L1 * (m1 + m2*s**2))
    theta2dot = z2
    z2dot = ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) +
             m2*L2*z2**2*s*c) / (L2 * (m1 + m2*s**2))
    return theta1dot, z1dot, theta2dot, z2dot

# Maximum time, time point spacings and the time grid (all in s).
tmax, dt = 100, 0.01
t = np.arange(0, tmax+dt, dt)

velocity = 10
# Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
y0 = np.array([3*np.pi/7, velocity, 3*np.pi/4, 0])

# Do the numerical integration of the equations of motion.
y = odeint(deriv, y0, t, args=(L1, L2, m1, m2))

# Unpack theta1, theta2 as a function of time.
theta1, theta2 = y[:,0], y[:,2]

# Convert to Cartesian coordinates of the two bob positions.
x1 = L1 * np.sin(theta1)
y1 = -L1 * np.cos(theta1)
x2 = x1 + L2 * np.sin(theta2)
y2 = y1 - L2 * np.cos(theta2)

# Plotted bob circle radius.
r = 0.05
# Plot a trail of the m2 bob's position for the last trail_secs seconds.
trail_secs = 50
# This corresponds to max_trail time points.
max_trail = int(trail_secs / dt)

fig, ax = plt.subplots(figsize=(8, 6))

# Set up the plot limits
ax.set_xlim(-L1-L2-0.1, L1+L2+0.1)
ax.set_ylim(-L1-L2-0.1, L1+L2+0.1)
ax.set_aspect('equal', adjustable='box')
plt.axis('off')

# Lines and circles to be updated during animation
line, = ax.plot([], [], lw=2, c='k')
trail, = ax.plot([], [], c='b', lw=1, solid_capstyle='butt', alpha=0.7)
circle1 = Circle((0, 0), r, fc='b', ec='b', zorder=10)
circle2 = Circle((0, 0), r, fc='r', ec='r', zorder=10)

ax.add_patch(circle1)
ax.add_patch(circle2)

def init():
    line.set_data([], [])
    trail.set_data([], [])
    circle1.set_center((0, 0))
    circle2.set_center((0, 0))
    return line, trail, circle1, circle2

def animate(i):
    # Update the line representing the pendulum rods
    line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
    
    # Update the circles representing the bobs
    circle1.set_center((x1[i], y1[i]))
    circle2.set_center((x2[i], y2[i]))

    
    # Update the trail of the second bob
    imin = max(0, i - max_trail)
    trail.set_data(x2[imin:i], y2[imin:i])
    
    return line, trail, circle1, circle2

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, interval=dt**10, blit=True)

plt.show()
