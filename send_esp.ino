#include <ESP8266WiFi.h>

const char* ssid = "NOYB_05"; // Remove the space at the end of the SSID
const char* password = "zelp0264";
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  delay(10);

  // Connect to Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());


  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Client connected");

    while (client.connected()) {
      if (Serial.available()) {
        //char message = Serial.read(); // Read a character from the Serial Monitor
        String message = Serial.readStringUntil('\n');

        client.print(message);
        
        //client.print('\n'); // Send the character to the client
        //Serial.println("Sent to client: ");
        //Serial.println(message);
      }

      // if (client.available()) {
      //   char response = client.read(); // Read data from the client (if any)
      //   // Do something with the received data from the client (if needed)
      // }
    }

    // Client disconnected
    // Serial.println("Client disconnected");
  }
}