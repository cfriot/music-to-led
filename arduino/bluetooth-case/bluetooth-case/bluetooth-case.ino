/***************************************************
   COMMANDS
   -----------------------------------------------
   00
   Displays the frame currently in the buffer
   Replies: 00
 *                                                 *
   02
   Setup led strip length
   Replies: nothing
 *                                                 *
    01 b1 g1 r1 b2 g2 r2 ... bn gn rn
   Reads nn pixels into the frame buffer
   Replies: nothing
 *                                                 *
   FF
   Clears the display and terminates the animation
   Replies: nothing
 ***************************************************/

#include <Adafruit_NeoPixel.h>

#define BLUETOOTH_MODE true
#define PIXELS 500

#if defined(ARDUINO_AVR_NANO)
  #define DATAPIN 4
#else
  #define DATAPIN D4
#endif

#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(11, 10); // (RX, TX) (pin Rx BT, pin Tx BT)

byte pixelBuffer[3];
byte countBuffer[3];
int count = 0;

const byte showFrame = 0x00;
const byte loadFrame = 0x01;
const byte clearFrame = 0xFF;

Adafruit_NeoPixel leds = Adafruit_NeoPixel(PIXELS, DATAPIN);

void setup()
{
  // Clear LEDs
  leds.begin();
  leds.clear();
  leds.show();

  // Open serial port and tell the controller we're ready.
  Serial.begin(9600);
  Bluetooth.begin(9600);
  Serial.println("setup ok");
  Bluetooth.println("Setup ok");
  Bluetooth.write(showFrame);
}

int bytesToInt(unsigned int x_high, unsigned int x_low) {
  int combined;
  combined = x_high;
  combined = combined*256;
  combined |= x_low;
  return combined;
}

void loop()
{
  // Read a command
  while (Bluetooth.available() == 0);
  byte command = Bluetooth.read();
  //Serial.println(".");
  switch (command)
  {
    // Show frame
    case showFrame:

      // Update LEDs
      leds.show();
      //Serial.println("Show");
      // Tell the controller we're ready
      // We don't want to be receiving serial data during leds.show() because data will be dropped
      Bluetooth.write(showFrame);
      break;

    // Load frame
    case loadFrame:

      // Read number of pixels
      while (Bluetooth.available() == 0);
//      Serial.println("Load");
      Bluetooth.readBytes(countBuffer, 2);
      count = bytesToInt(countBuffer[0], countBuffer[1]);
//      Serial.print("Count of pixels :");
//      Serial.println(count);
      // Read and update pixels
      for (int i = 0; i < count; i++)
      {
        Bluetooth.readBytes(pixelBuffer, 3);
        leds.setPixelColor(i, pixelBuffer[0], pixelBuffer[1], pixelBuffer[2]);
//        Serial.print("Pixel ");
//        Serial.print(i);
//        Serial.print(" => ");
//        Serial.print(pixelBuffer[0]);
//        Serial.print(" ");
//        Serial.print(pixelBuffer[1]);
//        Serial.print(" ");
//        Serial.println(pixelBuffer[2]);
      }
      break;

    // Clear
    case clearFrame:
      leds.clear();
      leds.show();
      //Serial.println("Clear");
      break;
  }
}
