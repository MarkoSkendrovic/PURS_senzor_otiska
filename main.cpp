#include <Adafruit_Fingerprint.h>
#include <WiFi.h>
#include <HTTPClient.h>

volatile int finger_status = -1;

#define MODEM_RX 16
#define MODEM_TX 17
#define mySerial Serial2 // use for ESP32
#define LED_ZELENO 33
#define LED_CRVENO 32


Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

const char* ssid = "Dutkovic";
const char* password = "ABCD1234";

void setup()  
{
  pinMode(LED_ZELENO, OUTPUT);
  pinMode(LED_CRVENO, OUTPUT);
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  } 
  Serial.print("Connected ");  
  Serial.println(WiFi.localIP());

  
  while (!Serial);  // For Yun/Leo/Micro/Zero/...
  delay(100);
  Serial.println("\n\nAdafruit finger detect test");

  // set the data rate for the sensor serial port
  finger.begin(57600);
  
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  } else {
    Serial.println("Did not find fingerprint sensor :(");
    while (1) { delay(1); }
  }

  finger.getTemplateCount();
  Serial.print("Sensor contains "); Serial.print(finger.templateCount); Serial.println(" templates");
  Serial.println("Waiting for valid finger...");
}






int getFingerprintIDez() {
  uint8_t p = finger.getImage();
  if (p!=2){
    //Serial.println(p);
  }
  if (p != FINGERPRINT_OK)  return -1;
  
  p = finger.image2Tz();
  if (p!=2){
    //Serial.println(p);
  }
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -2;
  
  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID); 
  HTTPClient http;
  http.begin("http://192.168.1.7:5000/checkin");
  http.addHeader("Content-Type", "application/json");
  http.POST("{\"id\":"+String(finger.fingerID)+"}");
  Serial.println(http.getString());
  http.end();
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  return finger.fingerID; 
}



void loop()                     // run over and over again
{
  finger_status = getFingerprintIDez();
  if (finger_status!=-1 and finger_status!=-2){
    Serial.print("Match\n \r");
    digitalWrite(LED_ZELENO, HIGH);
    delay(5000);
    digitalWrite(LED_ZELENO, LOW);
  } else{
    if (finger_status==-2){
      for (int ii=0;ii<1;ii++){
        Serial.print("Not Match\n \r");
        digitalWrite(LED_CRVENO, HIGH);
        delay(5000);
        digitalWrite(LED_CRVENO, LOW);
      }
    }
  }
  delay(1000);            //don't ned to run this at full speed.
}







