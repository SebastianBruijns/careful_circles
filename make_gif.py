import imageio

for name in ['a', 'b']:
    images = []
    for t in range(320):
        images.append(imageio.imread("fits/{}_{}".format(name, t) + '.png'))
    imageio.mimsave('circles_{}.gif'.format(name), images, format='GIF', duration=0.07, loop=0)