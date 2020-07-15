#!/usr/bin/env python3

import sys
import time
import datetime
from nature_remo import NatureRemoCloud

TOKEN = sys.argv[1]
cloud_api = NatureRemoCloud(TOKEN)

last_events = {}

def str2datetime(s):
  return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))

while True:
  devices = cloud_api.get_devices()
  new_events = []
  for device in devices:
    events = device['newest_events']
    device_id = device['id']
    for event_type, event in events.items():
      key = device_id+'_'+event_type
      dt = str2datetime(event['created_at'])
      value = event['val']
      if dt == last_events.get(key):
        continue
      last_events[key] = dt
      new_events.append((dt, device_id, event_type, value))
  for event in sorted(new_events, key=lambda x: x[0]):
    event = list(event)
    #event[0] = event[0].isoformat()
    jst = datetime.timezone(datetime.timedelta(hours=9))
    event[0] = event[0].astimezone(jst).isoformat()
    event[3] = str(event[3])
    print(','.join(event))
  time.sleep(10)
