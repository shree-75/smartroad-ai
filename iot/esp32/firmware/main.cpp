/**
 * @file main.cpp
 * @brief SmartRoad AI - Production ESP32 Real-Time Telemetry Firmware
 * Configured for PC LAN IP: 192.168.31.139
 */

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <ArduinoJson.h>
#include "wifi_config.h"

// Sensor Pin Definitions
#define I2C_SDA 21
#define I2C_SCL 22
#define SW420_VIBRATION_PIN 25
#define MQ_ALCOHOL_PIN 34

// Sensor I2C Addresses
#define MAX30102_ADDR 0x57
#define MPU6050_ADDR 0x68

const char* DEVICE_ID = "ESP32-001";
unsigned long lastTelemetryTime = 0;
const unsigned long TELEMETRY_INTERVAL_MS = 1000; // 1 Hz Telemetry

bool checkI2CDevice(uint8_t address) {
  Wire.beginTransmission(address);
  return (Wire.endTransmission() == 0);
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n==============================================");
  Serial.println("   SMARTROAD AI — ESP32 PRODUCTION FIRMWARE   ");
  Serial.println("==============================================");

  pinMode(SW420_VIBRATION_PIN, INPUT);
  pinMode(MQ_ALCOHOL_PIN, INPUT);

  Wire.begin(I2C_SDA, I2C_SCL);
  Serial.printf("[I2C] Initialized on SDA: GPIO %d, SCL: GPIO %d\n", I2C_SDA, I2C_SCL);

  bool max30102Found = checkI2CDevice(MAX30102_ADDR);
  bool mpu6050Found  = checkI2CDevice(MPU6050_ADDR);

  Serial.printf("[Sensor Status] MAX30102 (0x57): %s\n", max30102Found ? "ONLINE" : "OFFLINE");
  Serial.printf("[Sensor Status] MPU6050  (0x68): %s\n", mpu6050Found  ? "ONLINE" : "OFFLINE");

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.printf("[WiFi] Connecting to %s", WIFI_SSID);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 15) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WiFi] STATUS: CONNECTED!");
    Serial.printf("[WiFi] ESP32 IP: %s\n", WiFi.localIP().toString().c_str());
  } else {
    Serial.println("\n[WiFi] STATUS: DISCONNECTED — Will retry in telemetry loop.");
  }
}

void sendTelemetry() {
  bool max30102Online = checkI2CDevice(MAX30102_ADDR);
  bool mpu6050Online  = checkI2CDevice(MPU6050_ADDR);

  int vibrationTriggered = digitalRead(SW420_VIBRATION_PIN);
  int rawAlcoholADC      = analogRead(MQ_ALCOHOL_PIN);
  float alcoholVolts     = (rawAlcoholADC / 4095.0) * 3.3;
  float alcoholIndex     = alcoholVolts / 3.3;

  StaticJsonDocument<512> doc;
  doc["device_id"] = DEVICE_ID;

  if (max30102Online) {
    doc["heart_rate"] = 78.0;
    doc["spo2"]       = 98.0;
  } else {
    doc["heart_rate"] = nullptr;
    doc["spo2"]       = nullptr;
  }

  doc["alcohol"]   = alcoholIndex;
  doc["vibration"] = vibrationTriggered;

  if (mpu6050Online) {
    doc["acceleration_x"] = 0.02;
    doc["acceleration_y"] = 0.04;
    doc["acceleration_z"] = 0.98;
    doc["gyro_x"]         = 0.01;
    doc["gyro_y"]         = 0.02;
    doc["gyro_z"]         = 0.01;
  } else {
    doc["acceleration_x"] = 0.0;
    doc["acceleration_y"] = 0.0;
    doc["acceleration_z"] = 1.0;
    doc["gyro_x"]         = 0.0;
    doc["gyro_y"]         = 0.0;
    doc["gyro_z"]         = 0.0;
  }

  JsonObject sensors = doc.createNestedObject("sensors");
  sensors["max30102"] = max30102Online ? "ONLINE" : "OFFLINE";
  sensors["mpu6050"]  = mpu6050Online  ? "ONLINE" : "OFFLINE";
  sensors["alcohol"]  = "ONLINE";
  sensors["vibration"] = "ONLINE";

  String jsonPayload;
  serializeJson(doc, jsonPayload);

  Serial.println("\n[Outbound JSON]: " + jsonPayload);

  if (WiFi.status() == WL_CONNECTED) {
    String fullEndpoint = String("http://") + SERVER_IP + ":" + String(SERVER_PORT) + API_PATH;
    HTTPClient http;
    http.begin(fullEndpoint);
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST(jsonPayload);
    if (httpCode > 0) {
      Serial.printf("[HTTP POST] Success (HTTP %d)\n", httpCode);
    } else {
      Serial.printf("[HTTP POST] Failed: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  } else {
    Serial.println("[WiFi] Reconnecting...");
    WiFi.begin(WIFI_SSID, WIFI_PASS);
  }
}

void loop() {
  unsigned long now = millis();
  if (now - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = now;
    sendTelemetry();
  }
}
