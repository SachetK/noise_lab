const int ledPin = 9;
const int sensorPin = A0;
const unsigned long sampleInterval = 100; // ms
unsigned long lastSample = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();
  if (now - lastSample >= sampleInterval) {
    int val = analogRead(sensorPin);
    Serial.print(now);      // timestamp in ms
    Serial.print(",");      // CSV separator
    Serial.println(val);    // sensor reading
    lastSample = now;
  }
}
