#include <ESP8266WiFi.h>

const char* ssid = "vv"; // Replace with your Wi-Fi network name
const char* password = "1234567890"; // Replace with your Wi-Fi password
const char* server_ip = "192.168.134.239"; // Replace with NodeMCU 1's IP address
WiFiClient client;

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

  // Set up the client
  Serial.print("Connecting to server: ");
  Serial.println(server_ip);

  if (client.connect(server_ip, 80)) {
    Serial.println("Connected to server");
  } else {
    Serial.println("Connection failed");
  }
}

void loop() {
  // Connect to the server
  if (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line != "") {
      Serial.println("Server says: " + line);
    }
  } else {
    Serial.println("Disconnected from server");
    client.stop();

    // Attempt to reconnect
    if (client.connect(server_ip, 80)) {
      Serial.println("Reconnected to server");
    } else {
      Serial.println("Reconnection failed");
    }
  }

  delay(1000); 
}