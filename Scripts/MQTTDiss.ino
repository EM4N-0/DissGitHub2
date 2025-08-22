#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "UCL_IoT";
const char* password = "NkE7SSMkiG";

// MQTT server details
const char* mqtt_server = "mqtt.cetools.org";
const int mqtt_port = 1884;
const char* mqtt_user = "student";
const char* mqtt_pass = "ce2021-mqtt-forget-whale";
const char* topic = "student/ucfneeg/status";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("Booting NodeMCU...");

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n Connected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT
  client.setServer(mqtt_server, mqtt_port);
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("NodeMCUClient", mqtt_user, mqtt_pass)) {
      Serial.println(" MQTT connected!");
      client.publish(topic, "start_show", true); // <--  trigger LED matrix
    } else {
      delay(500);
    }
  }
}

void loop() {
  if (!client.connected()) {
    while (!client.connect("NodeMCUClient", mqtt_user, mqtt_pass)) {
      delay(500);
    }
    client.publish(topic, "start_show", true); // Re-publish if reconnect
  }
  client.loop();
}