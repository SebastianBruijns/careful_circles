import imageio

images = []
for t in range(320):
    images.append(imageio.imread("t_{}".format(t) + '.png'))
imageio.mimsave('circles.gif', images, format='GIF', duration=0.05, loop=0)