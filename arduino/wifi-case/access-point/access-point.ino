/****************************************
 Audio 2 Led project

 ESP8266 Hotspot wifi v0.1
****************************************/


#include <ESP8266WiFi.h>

uint8_t ledFeedback1 = D6;
uint8_t ledFeedback2 = D7;
uint8_t ledFeedback3 = D8;

void setLedState(int state) {
  digitalWrite(ledFeedback1, state);
  digitalWrite(ledFeedback2, state);
  digitalWrite(ledFeedback3, state);
}

void ledBlink() {
  setLedState(HIGH);
  delay(250);
  setLedState(LOW);
  delay(250);
  setLedState(HIGH);
  delay(250);
  setLedState(LOW);
  delay(250);
}

void setup()
{
  delay(2500);
  Serial.begin(115200);
  Serial.println();

  Serial.print("Setting soft-AP ... ");
  boolean result = WiFi.softAP("dodocwifi", "password");
}

void loop()
{
  Serial.printf("Stations connected = %d\n", WiFi.softAPgetStationNum());
  delay(3000);
}
