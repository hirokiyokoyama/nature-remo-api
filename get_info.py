#!/usr/bin/env python3

import sys
from nature_remo import NatureRemoCloud

TOKEN = sys.argv[1]
cloud_api = NatureRemoCloud(TOKEN)

print('[User]')
user = cloud_api.get_user()
print(f'  ID: {user["id"]}')
print(f'Name: {user["nickname"]}')
print()

print('[Devices]')
devices = cloud_api.get_devices()
for device in devices:
  print(f'<{device["name"]}>')
  print(f'      ID: {device["id"]}')
  print(f'Firmware: {device["firmware_version"]}')
  events = device["newest_events"]
  if 'te' in events:
    print(f'    Temp: {events["te"]["val"]}')
  if 'hu' in events:
    print(f'Humidity: {events["hu"]["val"]}')
  if 'il' in events:
    print(f'   Illum: {events["il"]["val"]}')
  if 'mo' in events:
    print(f'Movement: {events["mo"]["val"]}')
  print()
  
print('[Appliances]')
appliances = cloud_api.get_appliances()
for appliance in appliances:
  print(f'<{appliance["nickname"]}>')
  print(f'     ID: {appliance["id"]}')
  print(f'  Model: {appliance["model"]["name"]}')
  print(f' Device: {appliance["device"]["name"]}')
  print(f'   Type: {appliance["type"]}')
  if appliance['type'] != 'AC':
    buttons = appliance[appliance['type'].lower()]["buttons"]
    print(f'Buttons: {[b["name"] for b in buttons]}')
  print()
