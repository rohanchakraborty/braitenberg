import numpy as np
import math
import matplotlib.pyplot as plt
import random

# Constants
MAX_TIME = 1000
PI = math.pi
SPEED = 0.01
SENSOR_MAX_DIST = 0.15  # 15% of the grid width
GRID_SIZE = 1000

# Initialize the grid with obstacles
obstacles = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
# Define border and internal obstacles
for i in range(GRID_SIZE):
    obstacles[i, 0] = obstacles[i, -1] = True
    obstacles[0, i] = obstacles[-1, i] = True
obstacles[:300, 397:400] = True
obstacles[700:, 597:600] = True
obstacles[500:503, :800] = True

def adjust_position(x, y):
    if x < 0 or x >= 1 or y < 0 or y >= 1:
        return None
    x_idx, y_idx = int(x * GRID_SIZE), int(y * GRID_SIZE)
    if obstacles[x_idx, y_idx]:
        return None
    return x, y

def proximity_sensor(x, y, direction):
    dist = 0.0
    step_size = 0.001  # increased precision
    while dist <= SENSOR_MAX_DIST:
        x += step_size * math.cos(direction)
        y += step_size * math.sin(direction)
        if x < 0 or x >= 1 or y < 0 or y >= 1:
            return SENSOR_MAX_DIST
        x_idx, y_idx = int(x * GRID_SIZE), int(y * GRID_SIZE)
        if obstacles[x_idx, y_idx]:
            return dist
        dist += step_size
    return SENSOR_MAX_DIST

def smart_heading_adjustment(sensor_left, sensor_center, sensor_right):
    if sensor_center < SENSOR_MAX_DIST:
        return PI / 4 if sensor_left > sensor_right else -PI / 4
    elif sensor_left < sensor_right:
        return PI / 8  # smaller adjustment if left is clearer
    else:
        return -PI / 8  # smaller adjustment if right is clearer

def main():
    x, y = 0.01, 0.91  # Start position
    heading = random.random() * 2 * PI - PI  # Randomized initial heading
    trajectory = [(x, y)]

    for _ in range(MAX_TIME):
        sensor_left = proximity_sensor(x, y, heading + PI/4)
        sensor_center = proximity_sensor(x, y, heading)
        sensor_right = proximity_sensor(x, y, heading - PI/4)

        heading += smart_heading_adjustment(sensor_left, sensor_center, sensor_right)

        x_new = x + SPEED * math.cos(heading)
        y_new = y + SPEED * math.sin(heading)

        new_position = adjust_position(x_new, y_new)
        if new_position:
            x, y = new_position
            trajectory.append((x, y))
        else:
            heading += PI / 4 

    # Plotting
    plt.figure(figsize=(10, 8), facecolor='white')
    plt.imshow(obstacles.T, cmap='Blues', origin='lower', extent=[0, 1, 0, 1], alpha=0.2)
    xs, ys = zip(*trajectory)
    plt.plot(xs, ys, 'b-', lw=1, label='Trajectory')
    plt.title('Task 2: Braitenberg Vehicle with Enhanced Navigation')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()
    plt.savefig("part2_proximity_sensors.png")

if __name__ == "__main__":
    main()
