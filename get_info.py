#!/usr/bin/env python3

import sys
from nature_remo import NatureRemoCloud

TOKEN = sys.argv[1]
cloud_api = NatureRemoCloud(TOKEN)

print('[User]')
user = cloud_api.get_user()
print(f'Name: {user["nickname"]}')
print(f'  ID: {user["id"]}')
print()

print('[Devices]')
devices = cloud_api.get_devices()
for device in devices:
  print(f'<{device["name"]}>')
  print(f'Firmware: {device["firmware_version"]}')
  print(f'      ID: {device["id"]}')
  print()
  
print('[Appliances]')
appliances = cloud_api.get_appliances()
for appliance in appliances:
  print(f'<{appliance["nickname"]}>')
  print(f'  Model: {appliance["model"]["name"]}')
  print(f' Device: {appliance["device"]["name"]}')
  print(f'   Type: {appliance["type"]}')
  if appliance['type'] != 'AC':
    buttons = appliance[appliance['type'].lower()]["buttons"]
    print(f'Buttons: {[b["name"] for b in buttons]}')
  print(f'     ID: {appliance["id"]}')
  print()
