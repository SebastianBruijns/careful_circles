import matplotlib.pyplot as plt
import numpy as np

n = 400

straight_dist = n

x, y = 100, 100

def simple_dist(start, end):
	return np.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)

def compute_traversal_dist(angle):
	"""
		Pretty sure all angles, irrespective of starting location, lead to the same overall distance traversed before returning to the start
		give angle as y-displacement upon full traversal. E.g. horizontal movement = 0, 90 degree angle = 400, 45 is 200 etc.
	"""
	total = 0
	current_point = (0, 0)
	while(True):
		total += simple_dist(current_point, (n, current_point[1] + angle))
		current_point = (0, (current_point[1] + angle) % n)
		if current_point == (0, 0):
			break
	return total


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