#!/usr/bin/env python3

import sys
from nature_remo import NatureRemoLocal

HOSTNAME = sys.argv[1]
local_api = NatureRemoLocal(HOSTNAME)

def to_hex(arr):
  hex = lambda x: f'{x:02x}'
  return '0x '+' '.join(map(hex, arr))

# turn on toshiba TV
signal = {
  'format': 'NEC',
  'custom': [0x40, 0xbf],
  'data': [0x12, 0xed],
  'freq': 37,
  'T': 550
}
local_api.send_signal(signal)
