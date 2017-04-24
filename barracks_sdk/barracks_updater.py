import requests
from device_info import DeviceInfo
from json_serializer import JsonSerializer

class BarracksUpdater:

  DEFAULT_BASE_URL = 'https://app.barracks.io'
  GET_DEVICE_PACKAGES_ENDPOINT = '/api/device/resolve'

  def __init__(self, api_key, base_url=DEFAULT_BASE_URL, allow_self_signed=False):
    self._api_key = api_key
    self._base_url = base_url
    self._allow_self_signed = allow_self_signed
    self._json_serializer = JsonSerializer()

  def get_device_packages(self, device_info):
    """
    :type device_info: DeviceInfo
    """
    response = requests.post(
      self._base_url + BarracksUpdater.GET_DEVICE_PACKAGES_ENDPOINT,
      headers=self._get_headers(),
      data=self._json_serializer.serialize(device_info),
      verify=self._allow_self_signed
    )
    return self._handle_response(response.json())

  def _get_headers(self):
    return {
      'Authorization': self._api_key,
      'Content-Type': 'application/json'
    }

  def _handle_response(self, response):
    if response.status_code == 200:
      if response.json is not None:
        print response.json()
    else:
      # TODO build custom exception class
      raise Exception('Request to get device packages failed')
      
