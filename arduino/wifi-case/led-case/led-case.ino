/****************************************
 Audio 2 Led project

 ESP8266 Led controller firmware v0.1
****************************************/

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NeoPixelBus.h>

#define NUM_LEDS 135 // Set to the number of LEDs in your LED strip
#define BUFFER_LEN 1024 // Maximum number of packets to hold in the buffer. Don't change this.
#define DEV_MODE 1 // Print debug to serial


#if DEV_MODE

  #define IP 36 // LEFT
  //#define IP 240 // RIGHT

  const char* ssid     = "gingerlednetwork2";
  const char* password = "lesledscestbienetinternetaussi";
  // IP LEFT 13 RIGHT 10 at home
  IPAddress ip(192, 168, 31, IP); // IP must match the IP in config.py
  IPAddress gateway(192, 168, 31, 1); // Set gateway to your router's gateway 192.168.1.234
  IPAddress subnet(255, 255, 255, 0);
  unsigned int localPort = 7777;

#endif

#if !DEV_MODE

  #define IP 23 // LEFT 4 RIGHT 5

  const char* ssid     = "boiteainternet"; // "Livebox-FF8E";
  const char* password = "internetcestbienetlesponeysaussi"; // "Berli0zz";
  IPAddress ip(10, 0, 0, IP); // IP must match the IP in config.py
  IPAddress gateway(10, 0, 0, 1); // Set gateway to your router's gateway 192.168.43.1
  IPAddress subnet(255, 255, 255, 0);
  unsigned int localPort = 7777;

#endif

const uint8_t PixelPin = 3;  // make sure to set this to the correct pin, ignored for Esp8266(set to 3 by default for DMA)
NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod> ledstrip(NUM_LEDS, PixelPin);
WiFiUDP port;
char packetBuffer[BUFFER_LEN];
uint8_t N = 0;
bool hasAlreadyRecieveAnything = false;

uint8_t ledFeedback = D5;

#if DEV_MODE
  uint16_t fpsCounter = 0;
  uint32_t secondTimer = 0;

static void printFps() {
  if (millis() - secondTimer >= 1000U) {
    secondTimer = millis();
    Serial.printf("FPS: %d\n", fpsCounter);
    fpsCounter = 0;
  }
}
#endif

static void sendMicroThroughUdp(unsigned long now) {
  static unsigned long next;
  if (next > now)
    return;
  next = now + 500;

  port.beginPacket(ip, localPort);
  port.print(analogRead(0));
  #if DEV_MODE
    Serial.print("MICRO : ");
    Serial.println(analogRead(0));
  #endif
  port.endPacket();

}

void setup() {
    delay(5000);
    Serial.begin(115200);
    WiFi.config(ip, gateway, subnet);
    WiFi.begin(ssid, password);
    Serial.println();

    pinMode(ledFeedback, OUTPUT);

    // Connect to wifi and print the IP address over serial
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        digitalWrite(ledFeedback, !digitalRead(ledFeedback));
    }

    digitalWrite(ledFeedback, HIGH);

    //#if DEV_MODE
      Serial.println("");
      Serial.print("Connected to ");
      Serial.println(ssid);
      Serial.print("IP address: ");
      Serial.println(WiFi.localIP());
    //#endif DEV_MODE

    port.begin(localPort);
    ledstrip.Begin(); // Begin output
    ledstrip.Show(); // Clear the strip for use
}

void loop() {

     unsigned long now = millis();
    // Read data over socket
    int packetSize = port.parsePacket();
    // If packets have been received, interpret the command

    if (packetSize) {
        if(!hasAlreadyRecieveAnything) { hasAlreadyRecieveAnything = true; }
        digitalWrite(ledFeedback, HIGH);
        int len = port.read(packetBuffer, BUFFER_LEN);
        for(int i = 0; i < len; i += 4) {
            packetBuffer[len] = 0;
            N = packetBuffer[i];
            RgbColor pixel((uint8_t)packetBuffer[i+1], (uint8_t)packetBuffer[i+2], (uint8_t)packetBuffer[i+3]);
            ledstrip.SetPixelColor(N, pixel);
        }
        ledstrip.Show();
        #if DEV_MODE
            fpsCounter++;
            Serial.print("."); // Monitors connection(shows jumps/jitters in packets)
        #endif
    }
    else if (hasAlreadyRecieveAnything) {
      digitalWrite(ledFeedback, LOW);
    }

    sendMicroThroughUdp(now);

    #if DEV_MODE
      printFps();
    #endif
}
