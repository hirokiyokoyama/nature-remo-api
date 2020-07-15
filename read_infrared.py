#!/usr/bin/env python3

import sys
from nature_remo import NatureRemoLocal

HOSTNAME = sys.argv[1]
#TOKEN = input('token: ')

local_api = NatureRemoLocal(HOSTNAME)
#cloud_api = NatureRemoCloud(TOKEN)

def to_hex(arr):
  hex = lambda x: f'{x:02x}'
  return '0x '+' '.join(map(hex, arr))

signal = local_api.capture_signal(decode=False)
print(signal)
import matplotlib.pyplot as plt
plt.plot(signal['data'], 'o-')
plt.show()
#print(f'Format: {signal["format"]}')
#print(f'Custom: {to_hex(signal["custom"])}')
#print(f'  Data: {to_hex(signal["data"])}')
#print(f'  Freq: {signal["freq"]}kHz')
#print(f'     T: {signal["T"]}us')

#message = local_api.get('/messages')
#print(remo.post('/messages', **message))

#remo_data = decode_signal(message)
#message = encode_signal(remo_data)

#print(cloud_api.get('/1/appliances/b25c74b8-c3dd-4fd5-8e95-dfa0b2237536/signals'))
#cloud_api.post('/1/signals/c1a4b1fc-0b7c-4429-bc53-dfd731333b74/send')

#cloud_api.post('/1/appliances/50af9c7f-2319-4342-872a-8f9d5b2b3ba0/signals',
#               message=json.dumps(message), image='ico_tool', name='clean')
#print(cloud_api.get('/1/appliances/50af9c7f-2319-4342-872a-8f9d5b2b3ba0/signals'))

