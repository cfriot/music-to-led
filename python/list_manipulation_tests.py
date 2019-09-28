import numpy as np
import timeit

n = 6

p = np.tile(0, (3, n))
pixels = np.random.rand(3, n)
pixels *= 254
pixels = pixels.astype(int)

# print("origin values")
# print(pixels)
#
# print("reversed values")
# pixels[0] = list(reversed(pixels[0]))
# pixels[1] = list(reversed(pixels[1]))
# pixels[2] = list(reversed(pixels[2]))
# print(pixels)
#
# print("other way to reverse values")
# print(pixels[:, ::-1])
#
# print("mirroring values")


def mirror(p):
    tmp = p[:, 3:]
    tmp = np.concatenate((tmp, tmp[:, ::-1]), axis=1)
    return tmp


if __name__ == '__main__':

    print(mirror(pixels))

    # timeit.timeit('mirror(pixels)', setup="from __main__ import test" + ', '.join(globals()), number=10000)
    #
    # mirror_tmp = np.copy(tmp_p[:config.N_PIXELS // 2])
    # tmp_p = np.concatenate((mirror_tmp[:, ::-1], mirror_tmp), axis=1)

    # return np.concatenate((tmp_p[:, ::-1], tmp_p), axis=1)
    # tmp = np.concatenate((pixels1, pixels1[:, ::-1]), axis=1)
    # tmp = np.concatenate(pixels[:], (pixels[:, ::n // 2]), axis=1)

    # strip = [[],[],[]]
    # strip[0] = np.tile(0, (3, config.STRIP_LENGTH_1))
    # strip[1] = np.tile(0, (3, config.STRIP_LENGTH_2))
    # strip[2] = np.tile(0, (3, config.STRIP_LENGTH_3))

    # print(tmp)
    # print(p)
