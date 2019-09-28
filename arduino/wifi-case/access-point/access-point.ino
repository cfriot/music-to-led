/****************************************
 Ginger Led Network

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

  pinMode(ledFeedback1, OUTPUT);
  pinMode(ledFeedback2, OUTPUT);
  pinMode(ledFeedback3, OUTPUT);

  Serial.print("Setting soft-AP ... ");
  boolean result = WiFi.softAP("gingerlednetwork", "lesledscestbienetlesponeysaussi");
  if(result == true)
  {
    Serial.println("Ready");
    setLedState(HIGH);
  }
  else
  {
    ledBlink();
    Serial.println("Failed!");
  }
  delay(2500);
  setLedState(LOW);
}

void loop()
{
  setLedState(LOW);
  Serial.printf("Stations connected = %d\n", WiFi.softAPgetStationNum());
  if(WiFi.softAPgetStationNum() == 1) {
    digitalWrite(ledFeedback1, HIGH);
  }
  else if(WiFi.softAPgetStationNum() == 2) {
    digitalWrite(ledFeedback1, HIGH);
    digitalWrite(ledFeedback2, HIGH);
  }
  else if(WiFi.softAPgetStationNum() == 3) {
    digitalWrite(ledFeedback1, HIGH);
    digitalWrite(ledFeedback2, HIGH);
    digitalWrite(ledFeedback3, HIGH);
  }
  
  delay(3000);
}
