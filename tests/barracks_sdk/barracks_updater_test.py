import unittest
from mock import patch, Mock
import json
import requests_mock
from barracks_sdk import BarracksUpdater, DeviceInfo, JsonSerializer

class BarrackUpdaterTest(unittest.TestCase):

  default_base_url = 'https://app.barracks.io'
  base_url = 'https://not.barracks.io'
  api_key = 'qwertyuiop'
  unit_id = 'my_unit'
  json_serializer_mock = Mock()

  def test__constructor__when__only_api_key(self):
    # When
    barracks_updater = BarracksUpdater(self.api_key)

    # Then
    self.assertEquals(barracks_updater._api_key, self.api_key)
    self.assertEquals(barracks_updater._base_url, self.default_base_url)
    self.assertFalse(barracks_updater._allow_self_signed)

  def test__constructor__when__api_key_and_base_url(self):
    # When
    barracks_updater = BarracksUpdater(self.api_key, self.base_url)

    # Then
    self.assertEquals(barracks_updater._api_key, self.api_key)
    self.assertEquals(barracks_updater._base_url, self.base_url)
    self.assertFalse(barracks_updater._allow_self_signed)

  def test__constructor__when__all_arguments(self):
    # When
    barracks_updater = BarracksUpdater(self.api_key, self.base_url, True)

    # Then
    self.assertEquals(barracks_updater._api_key, self.api_key)
    self.assertEquals(barracks_updater._base_url, self.base_url)
    self.assertTrue(barracks_updater._allow_self_signed)

  @requests_mock.mock()
  @patch.object(BarracksUpdater, '_handle_response')
  @patch.object(JsonSerializer, 'serialize')
  def test__get_device_packages__should__post_device_info(self, requests, json_serializer_mock, handle_response_mock):
    # Given
    device_packages = []
    device_info = DeviceInfo(self.unit_id, device_packages)
    api_response = {
      'available': [],
      'changed': [],
      'unchanged': [],
      'unavailable': []
    }
    json_serializer_mock.return_value = '{"aJson":"withValue"}'
    handle_response_mock.return_value = None
    requests.post(
      self.default_base_url + '/api/device/resolve',
      additional_matcher=lambda request: json_serializer_mock.return_value in (request.text or ''),
      json=api_response
    )

    # When
    barracks_updater = BarracksUpdater(self.api_key)
    result = barracks_updater.get_device_packages(device_info)

    # Then
    handle_response_mock.assert_called_once_with(api_response)
    json_serializer_mock.assert_called_once_with(device_info)
    self.assertEquals(result, handle_response_mock.return_value)


  # def test__get_headers(self):
  #   # Given
  #   barracks_updater = BarracksUpdater(self.api_key)
  #   expected = {
  #     'Authorization': api_key,
  #     'Content-Type': 'application/json'
  #   }

  #   # When
  #   headers = barracks_updater._BarracksUpdater__get_headers()

  #   # Then
  #   self.assertEquals(headers, expected)

  # def test__build_payload_when_no_package_in_device_info(self):
  #   # Given
  #   barracks_updater = BarracksUpdater(api_key)
  #   device_info = DeviceInfo(unit_id, [])
  #   expected = {
  #     'unitId': unit_id,
  #     'components': []
  #   }

  #   # When
  #   payload = barracks_updater._BarracksUpdater__build_payload(device_info)

  #   # Then
  #   self.assertEquals(payload, expected)

  # def test__build_payload_when_packages_in_device_info(self):
  #   self.assertTrue(False)

  # def test__build_payload_when_packages_and_custom_client_data_in_device_info(self):
  #   self.assertTrue(False)
