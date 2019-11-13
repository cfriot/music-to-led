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

const char* ssid     = "SFR-c3f8";
const char* password = "DRDKV4NNDM1J";
// IP LEFT 13 RIGHT 10 at home
IPAddress ip(109, 12, 208, 144); // IP must match the IP in config.py
IPAddress gateway(109, 12, 208, 1); // Set gateway to your router's gateway
IPAddress subnet(255, 255, 254, 0);
unsigned int localPort = 7777;


const uint8_t PixelPin = 3;  // make sure to set this to the correct pin, ignored for Esp8266(set to 3 by default for DMA)
NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod> ledstrip(NUM_LEDS, PixelPin);
WiFiUDP port;
char packetBuffer[BUFFER_LEN];
uint8_t N = 0;
bool hasAlreadyRecieveAnything = false;

uint8_t ledFeedback = D5;

uint16_t fpsCounter = 0;
uint32_t secondTimer = 0;

static void printFps() {
  if (millis() - secondTimer >= 1000U) {
    secondTimer = millis();
    Serial.printf("FPS: %d\n", fpsCounter);
    fpsCounter = 0;
  }
}

static void sendMicroThroughUdp(unsigned long now) {
  static unsigned long next;
  if (next > now)
    return;
  next = now + 500;

  port.beginPacket(ip, localPort);
  port.print(analogRead(0));
  Serial.print("MICRO : ");
  Serial.println(analogRead(0));
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

    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

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
          fpsCounter++;
          Serial.print("."); // Monitors connection(shows jumps/jitters in packets)
    }
    else if (hasAlreadyRecieveAnything) {
      digitalWrite(ledFeedback, LOW);
    }

    sendMicroThroughUdp(now);

    printFps();
}
