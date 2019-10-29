import numpy as np
import time


def reversePixels2(pixels):
    """Reverse pixels"""
    pixels[0] = list(reversed(pixels[0]))
    pixels[1] = list(reversed(pixels[1]))
    pixels[2] = list(reversed(pixels[2]))
    return pixels

def mirrorPixels(pixels, number_of_pixels, was_reversed_before):
    """Mirror pixels"""
    if(was_reversed_before):
        tmp = np.copy(pixels[:, number_of_pixels // 2:])
        return np.concatenate((tmp[:, ::-1], tmp), axis=1)
    else:
        tmp = np.copy(pixels[:, :number_of_pixels // 2])
        return np.concatenate((tmp[:, ::-1], tmp), axis=1)



number_of_pixels = 10

pixels = np.tile(0., (3, number_of_pixels))
pixels[0, 0] = 255
pixels[1, 1] = 255

# pixels[0, number_of_pixels - 1] = 255
# pixels[1, number_of_pixels - 2] = 255

print("before reverse")
print(pixels)
pixels = reversePixels2(pixels)
print("after")
print(pixels)

print("before mirror")
print(pixels)
pixels = mirrorPixels(pixels, len(pixels[0]), True)
print("after")
print(pixels)
