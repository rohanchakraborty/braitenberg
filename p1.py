import numpy as np
import math
import matplotlib.pyplot as plt
import random

# Constants
MAX_TIME = 1000
PI = math.pi
SPEED = 0.01  # Max speed per time step
TURN_ANGLE = PI / 8  # Max turn angle per time step
GRID_SIZE = 1000
LIGHT_X, LIGHT_Y = 0.5, 0.5  # Position of the light source in normalized coordinates
SENSOR_ANGLE = PI / 4  # Angle of sensors relative to the heading

def adjust_position(x, y):
    # Handles the torus space condition by wrapping around the positions.
    return x % 1, y % 1

def light_intensity(x, y):
    # Calculate light intensity based on distance from the light source
    distance = math.sqrt((x - LIGHT_X)**2 + (y - LIGHT_Y)**2)
    return max(0, 1 - distance)  # Assuming light intensity decreases linearly with distance

def get_sensor_positions(x, y, heading):
    # Calculate positions of left and right sensors based on current position and heading
    left_x = x + 0.05 * math.cos(heading + SENSOR_ANGLE)  # 0.05 is sensor offset from center
    left_y = y + 0.05 * math.sin(heading + SENSOR_ANGLE)
    right_x = x + 0.05 * math.cos(heading - SENSOR_ANGLE)
    right_y = y + 0.05 * math.sin(heading - SENSOR_ANGLE)
    return (adjust_position(left_x, left_y), adjust_position(right_x, right_y))

def sensor_readings(x, y, heading):
    # Get sensor positions
    (left_x, left_y), (right_x, right_y) = get_sensor_positions(x, y, heading)
    # Calculate light intensity at sensor positions
    sl = light_intensity(left_x, left_y)
    sr = light_intensity(right_x, right_y)
    return sl, sr

def update_heading(heading, sl, sr, mode='aggression'):
    # Update heading based on sensor readings and behavior mode
    if mode == 'aggression':
        # More light causes faster turning towards the light
        d_phi = TURN_ANGLE * (sr - sl)
    elif mode == 'fear':
        # More light causes faster turning away from the light
        d_phi = TURN_ANGLE * (sl - sr)
    return (heading + d_phi) % (2 * PI)
    
def plot_light_distribution():
    # Create a grid of points and calculate light intensity at each point
    grid_x, grid_y = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
    intensity = light_intensity(grid_x, grid_y)
    plt.figure(figsize=(10, 8))
    plt.imshow(intensity, origin='lower', extent=(0, 1, 0, 1), cmap='viridis')
    plt.colorbar(label='Light Intensity')
    plt.scatter([LIGHT_X], [LIGHT_Y], color='red', s=100, label='Light Source')
    plt.title('Light Intensity Distribution')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

def main(mode='aggression'):
    x, y = 0.1, 0.9  # Initial position
    heading = random.random() * 2 * PI  # Initial random heading

    trajectory = [(x, y)]

    for _ in range(MAX_TIME):
        sl, sr = sensor_readings(x, y, heading)
        heading = update_heading(heading, sl, sr, mode)

        # Calculate new position based on updated heading
        x_new = (x + SPEED * math.cos(heading)) % 1
        y_new = (y + SPEED * math.sin(heading)) % 1
        x, y = adjust_position(x_new, y_new)
        trajectory.append((x, y))
    name = f'Part1_plot_{mode}'
    # Plotting light dist
    plot_light_distribution()
    # Plotting trajectory
    plt.figure(figsize=(10, 8))
    xs, ys = zip(*trajectory)
    plt.plot(xs, ys, 'b-', lw=1, label=f'Trajectory - {mode}')
    plt.scatter([LIGHT_X], [LIGHT_Y], color='yellow', s=100, label='Light Source')
    plt.title('Braitenberg Vehicle Trajectory')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.savefig(name+'.png')
    plt.show()

if __name__ == "__main__":
    main(mode='fear')  # Change to 'fear' to test the other behavior
