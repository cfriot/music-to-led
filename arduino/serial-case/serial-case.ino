/***************************************************
   COMMANDS
   -----------------------------------------------
   00
   Displays the frame currently in the buffer
   Replies: 00
 *                                                 *
   01 nn b1 g1 r1 b2 g2 r2 ... bn gn rn
   Reads nn pixels into the frame buffer
   Replies: nothing
 *                                                 *
   FF
   Clears the display and terminates the animation
   Replies: nothing
 ***************************************************/

#include <Adafruit_NeoPixel.h>

#define NODE_CMU true

#if NODE_CMU
  #define DATAPIN D4
#else
  #define DATAPIN 4
#endif

#define PIXELS 500

byte pixelBuffer[3];

Adafruit_NeoPixel leds = Adafruit_NeoPixel(PIXELS, DATAPIN);

void setup()
{
  // Clear LEDs
  leds.begin();
  leds.clear();
  leds.show();

  // Open serial port and tell the controller we're ready.
  Serial.begin(1000000);
  Serial.println("Setup ok");
  Serial.write(0x00);
}

void loop()
{
  // Read a command
  while (Serial.available() == 0);
  byte command = Serial.read();
  byte count;
  switch (command)
  {
    // Show frame
    case 0x00:

      // Update LEDs
      leds.show();

      // Tell the controller we're ready
      // We don't want to be receiving serial data during leds.show() because data will be dropped
      Serial.write(0x00);
      break;

    // Load frame
    case 0x01:

      // Read number of pixels
      while (Serial.available() == 0);
      count = Serial.read();
      if (count > PIXELS) {
        count = PIXELS;
      }
      // Read and update pixels
      for (int i = 0; i < count; i++)
      {
        Serial.readBytes(pixelBuffer, 3);
        leds.setPixelColor(i, pixelBuffer[0], pixelBuffer[1], pixelBuffer[2]);
      }
      break;

    // Clear
    case 0xFF:
      leds.clear();
      leds.show();
      break;
  }
}
