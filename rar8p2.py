#!/usr/bin/env python3

import sys
from nature_remo import NatureRemoLocal, NatureRemoCloud
from nature_remo.signal import bits_to_bytes, bytes_to_bits

#HOSTNAME = sys.argv[1]
#local_api = NatureRemoLocal(HOSTNAME)
TOKEN = sys.argv[1]
DEVICE_ID = sys.argv[2]
cloud_api = NatureRemoCloud(TOKEN)

def rar8p2_msg(**state):
  power = state.get('power', True)
  save = state.get('save', False)
  mode = state.get('mode')
  speed = state.get('speed', 0) # 0: auto
  temp = state.get('temperature')
  clean = state.get('clean', False)
  change_dir = state.get('change_direction', False)
  
  if mode not in ['warm', 'cool', 'dry', 'blow']:
    raise ValueError(f'Illegal mode: {mode}.')
  if mode == 'dry' and speed > 2:
    raise ValueError(f'When mode==dry, wind speed must be either 0(auto), 1, or 2 not {speed}.')
  if temp not in range(16,33):
    raise ValueError(f'Illegal temperature: {temp}.')

  bytes_ = [0x01, 0x10, 0x00]
  def append(val):
    bytes_.append(val)
    bytes_.append(0xff-val)
  append(0x40)
  append(0xff)
  append(0xcc)

  # offset 9
  if speed == 1:
    append(0x98)
  elif speed == 5:
    append(0xa9)
  else:
    append(0x92)

  # offset 11
  if change_dir:
    append(0x81)
  else:
    append(0x13)

  # offset 13
  append(temp*4)
  # offset 15-24
  append(0)
  append(0)
  append(0)
  append(0)
  append(0)

  # offset 25
  if speed == 0:
    speed_code = 0x50
  elif speed == 5:
    speed_code = 0x60
  else:
    speed_code = speed * 0x10
  mode_code = {
    'warm': 6,
    'cool': 3,
    'dry': 5,
    'blow': 1
  }[mode]
  append(speed_code+mode_code)

  # offset 27
  power_code = 0xe0
  if power:
    power_code += 0x10
  if not save:
    power_code += 0x01
  append(power_code)

  # offset 29
  if speed == 5:
    append(0x30)
  else:
    append(0x00)

  # offset 31
  append(0)

  # offset 33
  if clean:
    append(0x88)
  else:
    append(0x80)

  # offset 35-
  append(0x03)
  append(0x01)
  append(0x88)
  append(0)
  append(0)
  append(0xff)
  append(0xff)
  append(0xff)
  append(0xff)

  bits = bytes_to_bits(bytes_)

  data = [30000, 50000, 3400, 1600]
  for bit in bits:
    if bit:
      data += [440, 1200]
    else:
      data += [440, 400]
  data.append(440)

  print(data)
  return {
    'freq': 38,
    'format': 'us',
    'data': data
  }

msg = rar8p2_msg(
    mode = 'cool',
    temperature = 25,
    speed = 1,
    power = True)
#local_api.send_signal(msg)

APPLIANCE_NAME = 'living_aircon'
SIGNAL_NAME = 'on_cool_25_1'

res = cloud_api.get_appliances()
for app in res:
  if app['nickname'] == APPLIANCE_NAME:
    appliance_id = app['id']
    break
else:
  cloud_api.create_appliance(
      nickname = APPLIANCE_NAME,
      device = DEVICE_ID,
      model_type = 'AC',
      image = 'ico_ac_1')
  appliance_id = res['id']

res = cloud_api.get_signals(appliance_id)
for signal in res:
  if signal['name'] == SIGNAL_NAME:
    signal_id = signal['id']
    break
else:
  res = cloud_api.create_signal(
      appliance_id,
      name = SIGNAL_NAME,
      image = 'ico_io',
      message = msg)
  signal_id = res['id']

cloud_api.send_signal(signal_id)

"""
def to_hex(arr):
  hex = lambda x: f'{x:02x}'
  return '0x '+' '.join(map(hex, arr))

signal = local_api.capture_signal(decode=False)
data = signal['data']
assert abs(data[0] - 30000) < 1000
assert abs(data[1] - 50000) < 1000
data = data[4:-1]

assert all(x < 2000 for x in data)

print(len(data))
bits = [1 if x > 800 else 0 for x in data[1::2]]
bytes_ = bits_to_bytes(bits)
print(to_hex(bytes_))

assert bytes_[0] == 0x01
assert bytes_[1] == 0x10
assert bytes_[2] == 0x00

def gethex(offset):
  x = bytes_[offset]
  parity = bytes_[offset+1]
  assert x+parity == 0xff
  return f'{x:02x}'

assert gethex(3) == '40'
assert gethex(5) == 'ff'
assert gethex(7) == 'cc'
#print(to_hex(bytes_[3:9]))

print('Fan:', gethex(9))
print('Action:', gethex(11))
print('Temp:', str(int(gethex(13),16)/4) + 'degc')

assert gethex(15) == '00'
assert gethex(17) == '00' # off timer
assert gethex(19) == '00' # off timer
assert gethex(21) == '00' # on timer
assert gethex(23) == '00' # timer?

print('Fan:', gethex(25))
print('Power:', gethex(27))
print('PowerFun:', gethex(29))

assert gethex(31) == '00'
assert gethex(33) == '80', gethex(33)
#assert gethex(33) == '88', gethex(33) #clean
assert gethex(35) == '03', gethex(35)
assert gethex(37) == '01', gethex(37)
assert gethex(39) == '88', gethex(39)
assert gethex(41) == '00', gethex(41)
assert gethex(43) == '00', gethex(43)
assert gethex(45) == 'ff', gethex(45)
assert gethex(47) == 'ff', gethex(47)
assert gethex(49) == 'ff', gethex(49)
assert gethex(51) == 'ff', gethex(51)
"""
