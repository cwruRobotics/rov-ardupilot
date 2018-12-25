#include <SoftwareSerial.h>

SoftwareSerial comms(10,11);
int i = 0;

void setup() {
  // put your setup code here, to run once:
  comms.begin(9600);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  char c = comms.read();
  if (c != -1) {
    Serial.println("Hello");
  }
}
