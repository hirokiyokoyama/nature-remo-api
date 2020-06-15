import json
import urllib.request
from . import signal

class NatureRemoBase(object):
  def __init__(self, base_url, post_json=True, get_header={}, post_header={}):
    super().__init__()
    self._base_url = base_url
    self._post_json = post_json
    header = {'accept': 'application/json'}
    self._get_header = dict(header)
    self._get_header.update(get_header)
    self._post_header = dict(header)
    if not post_json:
      self._post_header['Content-Type'] = 'application/x-www-form-urlencoded'
    self._post_header.update(get_header)
    
  def _get(self, query):
    url = self._base_url + query
    req = urllib.request.Request(
        url, headers=self._get_header)

    with urllib.request.urlopen(req) as res:
      return json.loads(res.read().decode())

  def _post(self, query, **args):
    url = self._base_url + query
    if self._post_json:
      data = json.dumps(args).encode()
    else:
      quote = urllib.parse.quote
      data = urllib.parse.urlencode(args, quote_via=quote).encode()
    req = urllib.request.Request(
        url, method='POST', headers=self._post_header, data=data)

    with urllib.request.urlopen(req) as res:
      return json.loads(res.read().decode())
    
class NatureRemoCloud(NatureRemoBase):
  def __init__(self, token):
    header = {'Authorization': 'Bearer '+token}
    super().__init__('https://api.nature.global', False, header, header)

  def get_user(self):
    return self._get('/1/users/me')
  def get_devices(self):
    return self._get('/1/devices')
  def get_appliances(self):
    return self._get('/1/appliances')

class NatureRemoLocal(NatureRemoBase):
  def __init__(self, hostname):
    header = {'accept': 'application/json', 'X-Requested-With' : 'curl'}
    super().__init__('http://'+hostname, True, header, header)

  def capture_signal(self, decode=True):
    msg = self._get('/messages')
    if decode:
      msg = signal.decode(msg)
    return msg

  def send_signal(self, msg):
    if msg['format'] != 'us':
      msg = signal.encode(msg)
    return self._post('/messages', **msg)
