import matplotlib.pyplot as plt
import numpy as np
import time
import pickle
# TODO: find positions to fill across time, not in time specifically...
# TODO: Thanks, toriod wrapping :/... https://math.stackexchange.com/questions/2213165/find-shortest-distance-between-lines-in-3d

n = 400
np.random.seed(4)

def simple_dist(start, end):
	return np.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)

def compute_traversal_dist(angle):
	"""
		Pretty sure all angles, irrespective of starting location, lead to the same overall distance traversed before returning to the start
		give angle as y-displacement upon full traversal. E.g. horizontal movement = 0, 90 degree angle = 400, 45 is 200 etc.
	"""
	total = 0
	current_point = (0, 0)
	while True:
		total += simple_dist(current_point, (n, current_point[1] + angle))
		current_point = (0, (current_point[1] + angle) % n)
		if current_point == (0, 0):
			break
	return total

def profile(x):
	return x

@profile
def generate_circle_points(x, y, size):
	points = []
	for i in range(-size, size + 1):
		for j in range(-size, size + 1):
			if i**2 + j**2 <= size**2:
				points.append((x + i, y + j))
	return points

@profile
def generate_circle_points_fast(x, y, size):
	xs, ys = np.meshgrid(np.arange(-size, size + 1), np.arange(-size, size + 1))
	circle = xs ** 2 + ys ** 2 <= size ** 2
	xs, ys = xs[circle], ys[circle]
	return np.vstack([xs + x, ys + y])

@profile
def fill_circle(array, t, x, y, size):
	# points = generate_circle_points(x, y, size)
	# for point in points:
	# 	array[t, point[0] % n, point[1] % n] = 1

	points = generate_circle_points_fast(x, y, size).T
	array[t, points[:, 0] % n, points[:, 1] % n] = 1

@profile
def compute_new_trajectory_fast(x, y, size, dis_x, dis_y):
	local_spacetime = np.zeros((total_duration, n, n))
	xs, ys = np.meshgrid(np.arange(-size, size + 1), np.arange(-size, size + 1))
	circle = xs ** 2 + ys ** 2 <= size ** 2
	xs, ys = xs[circle], ys[circle]
	time = np.arange(total_duration)
	local_spacetime[time[:, None], (dis_x * time[:, None] + xs + x).astype(int) % n, (dis_y * time[:, None] + ys + y).astype(int) % n] = 1
	return local_spacetime

def compute_new_trajectory(x, y, size, dis_x, dis_y):
	local_spacetime = np.zeros((total_duration, n, n))
	fill_circle(local_spacetime, 0, x, y, size)
	for t in range(1, total_duration):
		x += dis_x
		y += dis_y
		fill_circle(local_spacetime, t, int(x), int(y), size)
	return local_spacetime


print(simple_dist((0, 200), (400, 200)))
print(simple_dist((0, 0), (400, 400)))
print(simple_dist((0, 100), (100, 0)) + simple_dist((100, 400), (400, 100)))
print(simple_dist((300, 400), (400, 350)) + simple_dist((0, 350), (400, 150)) + simple_dist((0, 150), (300, 0)))
print(simple_dist((0, 0), (400, 200)) + simple_dist((0, 200), (400, 400)))

dists = []
good_angles, good_dists = [], []
for i in range(401):
	dists.append(compute_traversal_dist(i))
	if dists[-1] < 3000:
		good_angles.append(i)
		good_dists.append(dists[-1])

# plt.plot(dists)
# plt.ylim(0, 3000)
# plt.show()

total_duration = 320

n_circles = 18

for name in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
	start = time.time()

	infos = {}
	space_time = np.zeros((total_duration, n, n))
	a, b = [], []
	for i in range(n_circles):
		circle_placed = False
		attempts = 0
		while not circle_placed:
			attempts += 1
			size = int(np.random.uniform(5, 20))
			unnormalized_speed = np.random.choice(3, p=[0.25, 0.5, 0.25]) + 1
			displacement_index = np.random.choice(len(good_angles))

			# pick an angle (we treat angles as the amount of displacement along one axis while the other displaces by 1)
			displacement = good_angles[displacement_index]
			displacement = displacement if np.random.rand() < 0.5 else - displacement
			other_dir = -1 if np.random.rand() < 0.5 else 1
			dis_x, dis_y = (other_dir, displacement / 400) if np.random.rand() < 0.5 else (displacement / 400, other_dir)

			# break the down the total distance in need of covering
			normalized_speed = good_dists[displacement_index] / total_duration * unnormalized_speed

			# adapt the displacement to what we need to cover
			dis_x_prime = dis_x / np.sqrt(dis_x ** 2 + dis_y ** 2) * normalized_speed
			dis_y_prime = dis_y / np.sqrt(dis_x ** 2 + dis_y ** 2) * normalized_speed

			x, y = np.random.choice(n), np.random.choice(n)

			new_trajectory = compute_new_trajectory_fast(x, y, size, dis_x_prime, dis_y_prime)
			circle_placed = not ((space_time + new_trajectory) > 1).any()
			if circle_placed:
				space_time += new_trajectory
				print("Placed circle {} (with {} attempts)".format(i + 1, attempts))
				infos['x'] = x
				infos['y'] = y
				infos['size'] = size
				infos['dis_x_prime'] = dis_x_prime
				infos['dis_y_prime'] = dis_y_prime
			if attempts > 1200:
				print("Gave up after {} attempts".format(attempts))
				break

	print(time.time() - start)
	pickle.dump(infos, open("fits/" + name + "_infos", 'wb'))

	for t in range(total_duration):
		plt.imshow(space_time[t])
		plt.savefig("fits/" + name + "_{}".format(t))
		plt.close()