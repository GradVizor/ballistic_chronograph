#define n 16  // number of fotosensors along length and breadth

const int X_pins[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}; // pin numbers along length
const int Y_pins[] = {17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29. 30, 31, 32}; // pin numbers along breadth

unsigned long currentMicros;
unsigned long previousMicros;

int x_coordinate, y_coordinate;

// Assuming bottom left corner as origin
void setup() {
  Serial.begin(9600);
  for (int i=0; i<n; i++){
    pinMode(X_pins[i], INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(X_pins[i]), xCoordinate, CHANGE);

    pinMode(Y_pins[i], INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(Y_pins[i]), yCoordinate, CHANGE);
  }
}

void loop() {
  currentMicros = micros();
  if (currentMicros - previousMicros)>=50){
    previousMicros = currentMicros;
    Serial.print("Coordinates :- ")
    Serial.print(x_coordinate);
    Serial.print(",");
    Serial.println(y_coordinate);
  }
}

void xCoordinate() {
  for (int j=0; j<n; j++){
    if (digitalRead(X_pins[j]) == LOW){
      x_coordinate = j;
    }
  }
}

void yCoordinate() {
  for (int k=0; k<n; k++){
    if (digitalRead(X_pins[k]) == LOW){
      y_coordinate = k;
    }
  }
}