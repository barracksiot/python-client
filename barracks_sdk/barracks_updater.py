import json
import requests
from device_info import DeviceInfo

class BarracksUpdater:

  DEFAULT_BASE_URL = 'https://app.barracks.io'
  GET_DEVICE_PACKAGES_ENDPOINT = '/api/device/resolve'

  def __init__(self, api_key, base_url=DEFAULT_BASE_URL, allow_self_signed=False):
    self._api_key = api_key
    self._base_url = base_url
    self._allow_self_signed = allow_self_signed

  def get_device_packages(self, device_info):
    """
    :type device_info: DeviceInfo
    """
    request = requests.Request(
      method='POST',
      url=self._baseUrl + GET_DEVICE_PACKAGES_ENDPOINT,
      headers=self.__get_headers(),
      data=json.dumps(self.__build_payload(device_info))
    )
    response = requests.session().send(request, verify=self._allow_self_signed)
    return self.__handle_response(response)

  def __get_headers(self):
    return {
      'Authorization': self._api_key,
      'Content-Type': 'application/json'
    }

  def __build_payload(self, device_info):
    """
    :type device_info: DeviceInfo
    """
    payload = {
      'unitId': device_info.unit_id,
      'components': []
    }

    if device_info.custom_client_data is not None:
      payload['customClientData'] = update_detail_request.custom_client_data

    return payload

  def __handle_response(self, response):
    if response.status_code == 200:
      if response.json is not None:
        print response.json()
    else:
      # TODO build custom exception class
      raise Exception('Request to get device packages failed')
      
