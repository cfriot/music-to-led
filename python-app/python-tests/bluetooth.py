import sys, struct, serial, time, glob
import numpy as np


class SerialToArduinoLedStrip:
    """ Send pixels data to arduino via serial port """
    def __init__(self, number_of_pixels=30, port=""):
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
        self.baud_rate = 9600  # 1228800
        self.setup()

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
        message = ""
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
    ports = ['/dev/tty.DSDTECHHC-05-DevB']
    # 148
    number_of_pixels = 10
    serialToArduinoLedStrips = []

    from colorDictionary import ColorDictionary
    colorDictionary = ColorDictionary()
    print(colorDictionary.dictionary)
    number_of_pixels_by_strip = 250

    pixels = np.tile(1, (3, number_of_pixels))
    pixels *= 0
    for i, color in enumerate(colorDictionary.dictionary):
        if(i < number_of_pixels):
            pixels[0, i] = color[0]
            pixels[1, i] = color[1]
            pixels[2, i] = color[2]

    for port in ports:
        serialToArduinoLedStrips.append(SerialToArduinoLedStrip(
            number_of_pixels, port))

    while 1:
        pixels = np.roll(pixels, 1, axis=1)
        for serialToArduinoLedStrip in serialToArduinoLedStrips:
            serialToArduinoLedStrip.update(pixels)
        # time.sleep(.01)

#
# import serial, glob, time
#
#
# serial_class = serial.Serial(
#     '/dev/tty.DSDTECHHC-05-DevB', 9600, timeout=1, bytesize=serial.EIGHTBITS)
#
# if(serial_class.isOpen()):
#     print(serial_class.name)
#
# toto = b'\xFF'
# toto2 = b'2'
#
# while(1):
#     if(serial_class.isOpen()):
#         #print(serial_class.name)
#         # print(serial_class.read(1))
#         serial_class.write(toto2)
#         # print(serial_class.read(1))
#         time.sleep(1)
