const int trigPin = 9;
const int echoPin = 10;
long duration;
int distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  // IMPORTANT: Output raw JSON for our Kafka Bridge
  Serial.print("{\"sensor_id\": \"arduino_hc_sr04\", \"distance_cm\": ");
  Serial.print(distance);
  Serial.println("}");

  delay(3000); // 3-second interval is better for monitoring batches
}