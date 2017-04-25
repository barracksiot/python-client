from barracks_sdk import DeviceInfo, Package, JsonSerializer
import unittest
import mock
import json

class JsonSerializerTest(unittest.TestCase):

  def test__serialize_device_info_with_unit_id_only(self):
    # Given
    json_serializer = JsonSerializer()
    device_info = DeviceInfo('unit_id', [])
    expected_json = '{"customClientData": {}, "packages": [], "unitId": "%s"}' % (device_info.unitId)

    # When
    result = json_serializer.serialize(device_info)

    # Then
    self.assertEqual(result, expected_json)

  def test__serialize_device_info_with_unit_id_and_packages(self):
    # Given
    json_serializer = JsonSerializer()
    package = Package('app1', 'v1')
    device_info = DeviceInfo('unit_id', [ package ])
    expected_json = '{"customClientData": {}, "packages": [{"reference": "%s", "version": "%s"}], "unitId": "%s"}' % (package.reference, package.version, device_info.unitId)

    # When
    result = json_serializer.serialize(device_info)

    # Then
    self.assertEqual(result, expected_json)

  def test__serialize_device_info_with_unit_id_and_packages_and_custom_client_data(self):
    # Given
    json_serializer = JsonSerializer()
    package = Package('app1', 'v1')
    custom_client_data = '{"data": "value"}'
    device_info = DeviceInfo('unit_id', [ package ], json.loads(custom_client_data))
    expected_json = '{"customClientData": %s, "packages": [{"reference": "%s", "version": "%s"}], "unitId": "%s"}' % (custom_client_data, package.reference, package.version, device_info.unitId)

    # When
    result = json_serializer.serialize(device_info)

    # Then
    self.assertEqual(result, expected_json)
