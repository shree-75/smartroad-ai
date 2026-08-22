/**
 * @file wifi_config.h
 * @brief SmartRoad AI - ESP32 Wi-Fi & PC LAN Configuration Header
 * 
 * Configured for PC LAN IPv4: 192.168.31.139
 */

#ifndef WIFI_CONFIG_H
#define WIFI_CONFIG_H

// Wi-Fi Access Point Credentials
const char* WIFI_SSID = "AirFiber-aic9P";
const char* WIFI_PASS = "vijaya07";

// PC LAN Server Configuration (Obtained from 'ipconfig' on Windows)
const char* SERVER_IP   = "192.168.31.139"; // Active PC LAN IP
const int   SERVER_PORT = 8000;
const char* API_PATH    = "/api/v1/iot/telemetry";

#endif // WIFI_CONFIG_H
