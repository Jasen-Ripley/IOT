#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi/MQTT parameters
#define WLAN_SSID       "NETGEAR17"
#define WLAN_PASS       "largefire005"
#define BROKER_IP       "192.168.0.34"

//pins
#define BUTTON 4
#define LED 5
bool buttonstate;
bool ledstate = LOW;
bool clickedflag = false;

WiFiClient client;
PubSubClient mqttclient(client);

void callback (char* topic, byte* payload, unsigned int length) {

  payload[length] = '\0'; // add null terminator to byte payload so we can treat it as a string
  

  if (strcmp((char *)payload, "on") == 0){
    digitalWrite(LED, HIGH);
    } else if (strcmp((char *)payload, "off") == 0){
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
  connect();

  //setup pins
  pinMode(BUTTON, INPUT);
  pinMode(LED, OUTPUT); // setup pin for input
}

void loop() {
  if (!mqttclient.connected()) {
    connect();
  }
  mqttclient.loop();
  
  buttonstate = digitalRead(BUTTON);
  // if the button is clicked and it was not clicked previously
  if (buttonstate and not clickedflag){
      
      // set the clicked flag
      clickedflag = true;
  }

  // if the button is not clicked now and it was clicked previously (a commplete click has now happened)
  if (not buttonstate and clickedflag){

    // set the clicked flag
    clickedflag = false;
    if (ledstate == HIGH){
      //digitalWrite(LED, LOW);
      ledstate = LOW;
      mqttclient.publish("/PI", "off", false);
    }
    else if (ledstate == LOW){
      //digitalWrite(LED, HIGH);
      ledstate = HIGH;
      mqttclient.publish("/PI", "on", false);
    }
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

       mqttclient.subscribe("/aled");
      
    } else {
      Serial.print(F("MQTT server connection failed! rc="));
      Serial.print(mqttclient.state());
      Serial.println("try again in 10 seconds");
      // Wait 5 seconds before retrying
      delay(20000);
    }
  }
}
