#!/usr/bin/env python3

import sys
from nature_remo import NatureRemoCloud

TOKEN = sys.argv[1]
cloud_api = NatureRemoCloud(TOKEN)

# find TV
appliances = cloud_api.get_appliances()
for appliance in appliances:
  if appliance['type'] == 'TV':
    break
else:
  raise Exception('Could not find TV.')

# turn on the first TV
button_name = 'power'
cloud_api.push_button(appliance['id'], 'TV', button_name)
