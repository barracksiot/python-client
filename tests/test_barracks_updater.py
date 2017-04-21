import unittest
import mock
import requests_mock
from barracks_sdk import BarracksUpdater, DeviceInfo

default_base_url = 'https://app.barracks.io'
base_url = 'https://not.barracks.io'
api_key = 'qwertyuiop'
unit_id = 'my_unit'

class BarrackUpdaterTest(unittest.TestCase):

  def test_constructor_when_only_api_key(self):
    # When
    barracks_updater = BarracksUpdater(api_key)

    # Then
    self.assertEquals(barracks_updater._api_key, api_key)
    self.assertEquals(barracks_updater._base_url, default_base_url)
    self.assertFalse(barracks_updater._allow_self_signed)

  def test_constructor_when_api_key_and_base_url(self):
    # When
    barracks_updater = BarracksUpdater(api_key, base_url)

    # Then
    self.assertEquals(barracks_updater._api_key, api_key)
    self.assertEquals(barracks_updater._base_url, base_url)
    self.assertFalse(barracks_updater._allow_self_signed)

  def test_constructor_when_all_arguments(self):
    # When
    barracks_updater = BarracksUpdater(api_key, base_url, True)

    # Then
    self.assertEquals(barracks_updater._api_key, api_key)
    self.assertEquals(barracks_updater._base_url, base_url)
    self.assertTrue(barracks_updater._allow_self_signed)

  # @requests_mock.mock()
  def test_get_device_packages_when_minimum_device_info(self):
    # Given
    device_info = DeviceInfo(unit_id, [])
    response = {
      'available': [],
      'changed': [],
      'unchanged': [],
      'unavailable': []
    }
    barracks_updater = BarracksUpdater(api_key)
    # mock_req.post(default_base_url + '/api/device/resolve', json=response)

    with mock.patch.object(barracks_updater, '_BarracksUpdater__handle_response', return_value=None) as handle_response:

      # When
      result = barracks_updater.get_device_packages(device_info)

      # Then
      handle_response.assert_called_once_with(response)
      self.assertEquals(result, None)

  def test__get_headers(self):
    # Given
    barracks_updater = BarracksUpdater(api_key)
    expected = {
      'Authorization': api_key,
      'Content-Type': 'application/json'
    }

    # When
    headers = barracks_updater._BarracksUpdater__get_headers()

    # Then
    self.assertEquals(headers, expected)

  def test__build_payload_when_no_package_in_device_info(self):
    # Given
    barracks_updater = BarracksUpdater(api_key)
    device_info = DeviceInfo(unit_id, [])
    expected = {
      'unitId': unit_id,
      'components': []
    }

    # When
    payload = barracks_updater._BarracksUpdater__build_payload(device_info)

    # Then
    self.assertEquals(payload, expected)

  def test__build_payload_when_packages_in_device_info(self):
    self.assertTrue(False)

  def test__build_payload_when_packages_and_custom_client_data_in_device_info(self):
    self.assertTrue(False)
