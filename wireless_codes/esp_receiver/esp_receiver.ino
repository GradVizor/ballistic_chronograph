#include <WiFi.h>
#include <HTTPClient.h>

// Wi-Fi credentials
const char* ssid = "realme 7";
const char* password = "reishabh1234";

// Server URL to send the data (replace with your endpoint)
const char* serverURL = "http://192.168.249.158:8080/endpoint";

void setup() {
  Serial.begin(115200); // Debugging Serial Monitor
  Serial1.begin(9600, SERIAL_8N1, 16, 17); // Initialize UART with RX=GPIO16, TX=GPIO17

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
}

void loop() {
  // Check if data is available from Teensy
  if (Serial1.available()) {
    String receivedData = Serial1.readStringUntil('\n'); // Read data until newline
    int receivedNumber = receivedData.toInt(); // Convert string to integer

    Serial.print("Received from Teensy: ");
    Serial.println(receivedNumber);

    // Send the data over Wi-Fi to the server
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(serverURL);
      http.addHeader("Content-Type", "application/json");

      // Create a JSON payload with the integer data
      String jsonData = "{\"number\": " + String(receivedNumber) + "}";

      // Send HTTP POST request
      int httpResponseCode = http.POST(jsonData);

      // Print response
      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println("Response: " + response);
      } else {
        Serial.println("Error in POST: " + String(httpResponseCode));
      }

      http.end();
    } else {
      Serial.println("Wi-Fi disconnected");
    }
  }
}
