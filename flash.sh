#!/bin/bash

PORT="$1"

uvx esptool --port $PORT write-flash --flash-size=detect 0x3fc000 bin/esp_init_data_default_v08.bin 0 bin/ESP8266_GENERIC-20251209-v1.27.0.bin 