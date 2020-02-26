#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi/MQTT parameters
#define WLAN_SSID       "NETGEAR17"
#define WLAN_PASS       "largefire005"
#define BROKER_IP       "192.168.0.34"

//pins

int lightstate;

WiFiClient client;
PubSubClient mqttclient(client);

#define SENSOR A0
#define LED 5
void callback (char* topic, byte* payload, unsigned int length){
  payload[length] = '\0';
  if(strcmp((char *)payload, "on") == 0){
    Serial.println("pi->arduino : on");
    digitalWrite(LED, HIGH);
  }

  else if(strcmp((char *)payload, "off") == 0){
    Serial.println("pi->arduino : off");
    digitalWrite(LED, LOW);
  }
}


void setup() {
  Serial.begin(115200);
  
  // connect to wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }

  Serial.println(F("WiFi connected"));
  Serial.println(F("IP address: "));
  Serial.println(WiFi.localIP());

  // connect to mqtt server
  mqttclient.setServer(BROKER_IP, 1883);
  mqttclient.setCallback(callback);

  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);


}

void loop() {
  if (!mqttclient.connected()) {
    connect();
  }
  mqttclient.loop();

    //vars to keep track of time
  static const unsigned long REFRESH_INTERVAL = 1000; // ms
  static unsigned long lastRefreshTime = 0;


  //if time between now and last update is more than time interval
  if(millis() - lastRefreshTime >= REFRESH_INTERVAL)
  {
    lastRefreshTime += REFRESH_INTERVAL;
    lightstate = analogRead(A0);
    mqttclient.publish("/light", String(lightstate).c_str(), false);
    Serial.println(analogRead(A0));
  }
}


void connect() {
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println(F("Wifi issue"));
    delay(3000);
  }
  Serial.print(F("Connecting to MQTT server... "));
  while(!mqttclient.connected()) {
    if (mqttclient.connect(WiFi.macAddress().c_str())) {
      Serial.println(F("MQTT server Connected!"));

       mqttclient.subscribe("/arduino");
      
    } else {
      Serial.print(F("MQTT server connection failed! rc="));
      Serial.print(mqttclient.state());
      Serial.println("try again in 10 seconds");
      // Wait 5 seconds before retrying
      delay(20000);
    }
  }
}
