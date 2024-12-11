void setup() {
  Serial1.begin(9600); // Initialize UART on pins TX1=1, RX1=0
}

void loop() {
  int numberToSend = 42; // Example integer to send
  Serial1.println(numberToSend); // Send the integer as a string over UART
  delay(1000); // Send data every second
}