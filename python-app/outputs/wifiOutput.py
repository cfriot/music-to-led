import numpy as np
import socket

# Not implemented yet but the wifi protocol is working

class WifiOutput:
    """ Send pixels data to arduino via serial port """
    def __init__(self, number_of_pixels=30, ip="192.168.0.1", port=7777):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """Gamma lookup table used for nonlinear brightness correction"""
        self.prev_pixels = np.tile(253, (3, number_of_pixels))
        """Pixel values that were most recently displayed on the LED strip"""
        self.pixels = np.tile(1, (3, number_of_pixels))
        """Pixel values for the LED strip"""
        self.ip = ip
        """IP address of the ESP8266. Must match IP in ws2812_controller.ino"""
        self.port = port
        """Udp port. Must match IP in ws2812_controller.ino"""
        self.max_pixels_per_packet = 126
        """Max pixels per packet"""

    def update(self):
        """Sends UDP packets to ESP8266 to update LED strip values

        The ESP8266 will receive and decode the packets to determine what values
        to display on the LED strip. The communication protocol supports LED strips
        with a maximum of 256 LEDs.

        The packet encoding scheme is:
            |i|r|g|b|
        where
            i (0 to 255): Index of LED to change (zero-based)
            r (0 to 255): Red value of LED
            g (0 to 255): Green value of LED
            b (0 to 255): Blue value of LED
        """
        # Truncate values and cast to integer
        self.pixels = np.clip(self.pixels, 0, 255).astype(int)
        p = np.copy(self.pixels)
        # Pixel indices
        idx = range(self.pixels.shape[1])
        idx = [i for i in idx if not np.array_equal(p[:, i], self.prev_pixels[:, i])]
        n_packets = len(idx) // self.max_pixels_per_packet + 1
        idx = np.array_split(idx, n_packets)
        for packet_indices in idx:
            m = []
            for i in packet_indices:
                m.append(i)  # Index of pixel to change
                m.append(p[0][i])  # Pixel red value
                m.append(p[1][i])  # Pixel green value
                m.append(p[2][i])  # Pixel blue value
            m = bytes(m)
            self.sock.sendto(m, (self.ip, self.port))
        self.prev_pixels = np.copy(p)

# Execute this file to run a LED strand test
# If everything is working, you should see a red, green, and blue pixel scroll
# across the LED strip continously
if __name__ == '__main__':
    import time

    number_of_pixels = 30
    pixels = np.tile(1, (3, number_of_pixels))
    # Turn all pixels off
    pixels *= 0
    pixels[0, 0] = 255  # Set 1st pixel red
    pixels[1, 1] = 255  # Set 2nd pixel green
    pixels[2, 2] = 255  # Set 3rd pixel blue

    wifiClass = WifiOutput(number_of_pixels=number_of_pixels, ip="109.12.208.144")

    print('Starting LED strand test')
    while True:
        pixels = np.roll(pixels, 1, axis=1)
        wifiClass.pixels = pixels
        wifiClass.update()
        time.sleep(.016)
