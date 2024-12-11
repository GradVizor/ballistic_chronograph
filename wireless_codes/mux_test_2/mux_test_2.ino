#define S0 14
#define S1 27
#define S2 26
#define S3 25
#define Sig 33 // Sig pin as input

unsigned long startMicros, endMicros;
void setup() {
  Serial.begin(115200);
  // Set selection pins as outputs
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  
  // Set Sig pin as an output
  pinMode(Sig, INPUT);
  Serial.println("Program has started...");
}

void loop() {
  startMicros = micros();
  Serial.println(startMicros);
  for (int channel = 0; channel < 16; channel++) {
    selectChannel(channel);       // Select the channel
    int inp = digitalRead(Sig);          // Pause before the next channel
    // Serial.print(inp);
  }
  endMicros = micros();
  Serial.println(endMicros);
  Serial.println("Total time :- ");
  Serial.println(endMicros - startMicros);
  Serial.println("______");
  delay(2000);
}

void selectChannel(int channel) {
  digitalWrite(S0, channel & 0x01);        // Least significant bit
  digitalWrite(S1, (channel >> 1) & 0x01); // Second bit
  digitalWrite(S2, (channel >> 2) & 0x01); // Third bit
  digitalWrite(S3, (channel >> 3) & 0x01); // Most significant bit
}