# Bluetooth-at-command-mode

To change the baud rate of the HC-05 module and let him take a DTR command,
we need to pass it into command mode and update theses settings manually


![at-command-mode-wiring](../images/at-command-mode.png)

https://www.instructables.com/id/Modify-The-HC-05-Bluetooth-Module-Defaults-Using-A/

Wire the HC-05 and Arduino Uno per instructions.
BEFORE YOU CONNECT THE ARDUINO TO THE USB remove the VCC (power) red wire from the HC-05 so it's not getting any power from the Arduino. All other wires are still connected.
Now connect the Arduino Uno to the USB cable extended from your PC.
Make sure the HC-05 module is NOT PAIRED with any other Bluetooth device.
Re-connect the Arduino Uno 5V wire to the HC-05's VCC (5V power) pin.
The HC-05 LED will blink on and off at about 2 second intervals. Now the HC-05 is in AT command mode ready to accept commands to change configuration and settings.
To test if everything is wired correctly,  open the Serial Monitor from the Arduino IDE and type "AT" and click SEND. You should see an "OK"
If you don't see an "OK" check your wiring.
