#include <WiFi.h>
#include <HTTPClient.h>

// Change These with your mobile wifi and password
const char* ssid = "vivo";
const char* password = "12345678";

//Update the Token everytime will running 
String token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNpZGRhcnRoYUBnbWFpbC5jb20iLCJleHAiOjE3NzQ0MDc0NzR9.4BlgK6YAAOeAeUescxAWaSO3C7eaWlY5KcG5NBEPT4I";

// YOUR PC IP - Update the IP everytime will running
String server = "http://10.229.197.144:8000/predict";

HardwareSerial bpSerial(2);  // UART2

String data = "";

void setup() 
{
  Serial.begin(115200);
  delay(1000);

  Serial.println("🚀 ESP32 STARTED");
  bpSerial.begin(9600, SERIAL_8N1, 16, 17);

  // WIFI Connection
  Serial.println("📶 Connecting to WiFi...");
  WiFi.begin(ssid, password);

  int retry = 0;
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(1000);
    Serial.print(".");
    retry++;

    if (retry > 20) 
    {
      Serial.println("\n❌ WiFi Failed! Restarting...");
      ESP.restart();
    }
  }
  Serial.println("\n✅ WiFi Connected!");
  Serial.print("📡 IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() 
{
  while (bpSerial.available()) 
  {
    char c = bpSerial.read();
    if (c == '\n') 
    {
      data.trim();
      if (data.length() > 0) 
      {
        Serial.print("📥 Received: ");
        Serial.println(data);
        processPacket(data);
      }
      data = "";
    }
    else 
    {
      data += c;
    }
  }
}

//Processing of Blood Pressure Data
void processPacket(String packet) 
{
  if (packet == "start" || packet == "reading" || packet == "off") 
  {
    Serial.println("ℹ Status message ignored");
    return;
  }

  if (packet.startsWith("success")) 
  {
    int first = packet.indexOf(',');
    int second = packet.indexOf(',', first + 1);
    int third = packet.indexOf(',', second + 1);

    if (first > 0 && second > 0 && third > 0) 
    {
      int sbp = packet.substring(first + 1, second).toInt();
      int dbp = packet.substring(second + 1, third).toInt();
      int hr  = packet.substring(third + 1).toInt();

      Serial.println("🩺 ---- BP RESULT ----");
      Serial.print("SBP: "); Serial.println(sbp);
      Serial.print("DBP: "); Serial.println(dbp);
      Serial.print("HR : "); Serial.println(hr);
      Serial.println("---------------------");

      // Sending to cloud
      sendData(sbp, dbp, hr);
    }
    else 
    {
      Serial.println("❌ Invalid BP packet");
    }
  }
}

// Sending to API
void sendData(int sbp, int dbp, int hr) 
{
  if (WiFi.status() == WL_CONNECTED) 
  {
    HTTPClient http;

    String url = server + "?token=" + token;

    Serial.println("🌐 Sending data to server...");
    Serial.println("➡ URL: " + url);

    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"sbp\":" + String(sbp) +
                     ",\"dbp\":" + String(dbp) +
                     ",\"hr\":" + String(hr) + "}";

    Serial.println("📤 Payload: " + payload);

    int responseCode = http.POST(payload);

    Serial.print("📡 HTTP Response: ");
    Serial.println(responseCode);

    if (responseCode > 0) 
    {
      String response = http.getString();
      Serial.println("✅ Server Response: " + response);
    } 
    else 
    {
      Serial.println("❌ Error sending data");
    }
    http.end();
  } 
  else 
  {
    Serial.println("❌ WiFi not connected");
  }
}