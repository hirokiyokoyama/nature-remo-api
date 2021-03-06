def xor_parity(data_bits):
  assert(len(data_bits) % 4 == 0)
  n = len(data_bits) // 4

  parity_bits = []
  for i in range(n):
    parity_bits.append(sum(data_bits[i*4:i*4+4]) % 2)
  return parity_bits

def bits_to_bytes(bits, lsb_first=True):
  n = len(bits)
  assert n % 8 == 0, n
  bytes = []
  for i in range(n//8):
    byte = 0
    if lsb_first:
      for j in range(8):
        byte += bits[i*8+j] << j
    else:
      for j in range(8):
        byte += bits[i*8+(7-j)] << j
    bytes.append(byte)
  return bytes

def bytes_to_bits(bytes, lsb_first=True):
  n = len(bytes)
  bits = []
  for i in range(n):
    byte = bytes[i]
    if lsb_first:
      for j in range(8):
        bits.append(byte % 2)
        byte >>= 1
    else:
      for j in range(8):
        bits.append(byte % 0x80)
        byte <<= 1
  return bits

def decode(message):
  assert(message['format'] == 'us')

  result = {}
  result['freq'] = message['freq']

  data = message['data']
  # extract first frame
  for j in range(len(data)):
    if data[j] <= 10000:
      break
  for i in range(j+1, len(data)):
    if data[i] > 6000:
      break
  frame = data[j:i-1]
  #print(frame[:20])
  #assert len(frame) % 2 == 0
  if len(frame) % 2 != 0:
    frame = frame[:-1]
  assert len(frame) % 2 == 0    

  ons = frame[2::2]
  offs = frame[3::2]
  print(frame, ons, offs)
  frame_bits = [1 if off/on > 2. else 0 \
                for on, off in zip(ons, offs)]

  T = sum(ons)/len(ons)
  result['T'] = T

  if frame[0]+frame[1] > T*18:
    result['format'] = 'NEC'
    custom_bits = frame_bits[:16]
    data_bits = frame_bits[16:]
    assert len(data_bits) == 16, len(data_bits)
  else:
    result['format'] = 'AEHA'
    custom_bits = frame_bits[:16]
    custom_parity_bits = frame_bits[16:20]
    #assert xor_parity(custom_bits) == custom_parity_bits, (custom_bits, custom_parity_bits)
    data_code_bits = frame_bits[20:24]
    data_bits = frame_bits[24:]
    
  result['custom'] = bits_to_bytes(custom_bits)
  result['data'] = bits_to_bytes(data_bits)
  if result['format'] == 'AEHA':
    result['data_code'] = bits_to_bytes(data_code_bits+[0]*4)[0]

  return result

def encode(remo):
  result = {}
  result['freq'] = remo['freq']
  result['format'] = 'us'
  
  T = remo['T']
  data = []
  
  if remo['format'] == 'NEC':
    data.append(int(16*T))
    data.append(int(8*T))
  else:
    data.append(int(8*T))
    data.append(int(4*T))

  bits = bytes_to_bits(remo['custom'])
  if remo['format'] == 'AEHA':
    bits += xor_parity(bits)
    bits += bytes_to_bits([remo['data_code']])[:4]
  bits += bytes_to_bits(remo['data'])

  for bit in bits:
    data.append(int(T))
    data.append(int(T*3) if bit else int(T))
  data.append(int(T)) # stop bit
  result['data'] = data
  
  return result
