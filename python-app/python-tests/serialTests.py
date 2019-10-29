import sys
import struct
import serial
import time
import glob
import numpy as np

# ARDUINO CODE
'''
int combineTwoBytesIntoInt(unsigned int x_high, unsigned int x_low) {
  int combined;
  combined = x_high;
  combined = combined*256;
  combined |= x_low;
  return combined;
}

void printByte(byte b) {
  char s[4];
  snprintf(s, 4, "%d", b);
  Serial.println(s);
}

byte countBuffer[2];

void setup() {
  Serial.begin(1000000);
}

void loop() {
  int count;
  Serial.readBytes(countBuffer, 2);
  count = combineTwoBytesIntoInt(countBuffer[0], countBuffer[1]);
  Serial.println(count);
}
'''


with serial.Serial(port="/dev/tty.usbserial-14220", baudrate=1000000, timeout=1, writeTimeout=1) as serial_port:
    if serial_port.isOpen():
        while True:
            # ligne = serial_port.read_line()
            # print ligne
            number_of_pixels = (300).to_bytes(2, byteorder="big")
            # print(number_of_pixels[:2])
            serial_port.write(number_of_pixels[:2])
            ligne = serial_port.readline()
            print(ligne)
            time.sleep(1)
