import sys, struct, serial, time, glob
import numpy as np


class SerialToArduinoLedStrip:
    """ Send pixels data to arduino via serial port """
    def __init__(self, number_of_pixels=30, port="", baud_rate=1000000):
        self.serial_port = port
        self.serial_class = None
        self.trying_to_connect = False
        self.clear_command = b'\xff'
        self.show_command = b'\x00'
        self.send_number_of_pixel_command = b'\x02'
        self.send_data_command = b'\x01'
        self.number_of_pixels = number_of_pixels
        self.number_of_pixel_command = (self.number_of_pixels).to_bytes(2, byteorder="big")
        self.pixels = np.tile(.0, (3, number_of_pixels))
        self.raw_data = []
        self.baud_rate = baud_rate
        self.setup()

    @staticmethod
    def tryPort(port_name):
        try:
            s = serial.Serial(port_name)
            s.close()
        except (OSError, serial.SerialException):
            print("Serial port not found or busy, please check your config file -> ", port_name)
            print("Here's the audio ports available ->", SerialToArduinoLedStrip.listAvailableUsbSerialPorts())
            quit()

    @staticmethod
    def listAvailableUsbSerialPorts():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            # this excluses all ttys that are not tagged usbserial like arduinos
            ports = glob.glob('/dev/tty.usbserial*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def setup(self):

        try:
            self.serial_class = serial.Serial(
                self.serial_port, self.baud_rate, timeout=1, bytesize=serial.EIGHTBITS)
        except IOError:
            print("Hey it seem's that your cable is not plugged on port ", self.serial_port)
            time.sleep(1)
            self.setup()
            return

        self.serial_class.setDTR(False)
        time.sleep(1)
        self.serial_class.flushInput()
        self.serial_class.setDTR(True)
        print("Setup begin for %s" % self.serial_port)
        while True:
            message = self.serial_class.readline()
            if("Setup ok" in str(message)):
                break
        print("Setup finished for %s" % self.serial_port)
        while (message != self.show_command):
            message = self.serial_class.read(1)
        print("Begin transmision for %s" % self.serial_port)

    def getVector(self, array, col):
        vector = []
        imax = len(array)
        for i in range(imax):
            vector.append(array[i][col])
        return (vector)

    def getRawPixels(self, array):
        """ Transform pixels into the right data set

            input: [
                [r, ... * n_pixels],
                [g, ... * n_pixels],
                [b, ... * n_pixels]
            ]
            output: [
                [r, g, b, ... * n_pixels],
            ]
         """
        self.raw_data = []
        array = np.clip(array, 0, 255).astype(int)
        for i in range(self.number_of_pixels):
            self.raw_data += self.getVector(array, i)

    def update(self, pixels):
        """ Send frame to the arduino """
        self.pixels = np.tile(.0, (3, len(pixels[0])))
        self.number_of_pixels = len(pixels[0])
        self.pixels = pixels
        if(not self.trying_to_connect and self.serial_class):
            try:
                self.serial_class.write(self.show_command)
                self.serial_class.read(1)
                number_of_pixel_command = (self.number_of_pixels).to_bytes(2, byteorder="big")
                self.getRawPixels(self.pixels)
                message = self.send_data_command[:1] + number_of_pixel_command[:2] + bytes(self.raw_data)
                self.serial_class.write(message)
            except IOError:
                print("Hey it seem's that your cable has been unpluged on port ", self.serial_port)
                self.trying_to_connect = True
                self.setup()
                self.trying_to_connect = False
                return

if __name__ == "__main__":

    print('Starting SerialToArduinoLedStrip test on ports :')
    ports = SerialToArduinoLedStrip.listAvailableUsbSerialPorts()
    print(SerialToArduinoLedStrip.listAvailableUsbSerialPorts())
    # ports = ['/dev/tty.usbserial-14240', '/dev/tty.usbserial-14210']
    # 148
    number_of_pixels = 200
    serialToArduinoLedStrips = []

    pixels = np.tile(1, (3, number_of_pixels))
    pixels *= 0
    pixels[0, 0] = 125  # Set 1st pixel red
    pixels[1, 1] = 125  # Set 2nd pixel green
    pixels[2, 2] = 125  # Set 3rd pixel blue
    pixels[0, 3] = 255  # Set 1st pixel red
    pixels[1, 4] = 255  # Set 2nd pixel green
    pixels[2, 5] = 255  # Set 3rd pixel blue

    for port in ports:
        serialToArduinoLedStrips.append(SerialToArduinoLedStrip(
            number_of_pixels, port))

    while True:
        pixels = np.roll(pixels, 1, axis=1)
        for serialToArduinoLedStrip in serialToArduinoLedStrips:
            serialToArduinoLedStrip.update(pixels)
        time.sleep(.016)