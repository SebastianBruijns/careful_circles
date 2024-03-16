import imageio

for name in ['a']:
    images = []
    for t in range(500):
        images.append(imageio.imread("fits/{}_{}".format(name, t) + '.png'))
    imageio.mimsave('circles_{}.gif'.format(name), images, format='GIF', duration=0.065, loop=0)