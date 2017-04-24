# from barracks_sdk import DeviceInfo, Package
# import unittest
# import mock
# import json

# unit_id = 'my_unit'
# package1 = Package('app1', 'v1')
# package2 = Package('app2', 'v3')
# packages = [ package1, package2 ]
# custom_client_data = {
#   'aKey': 'A value',
#   'anotherKey': 34,
#   'aBooleanKey': True
# }

# class DeviceInfoTest(unittest.TestCase):

# # def test__device_info_constructor_with_minimum_argument():
# #   device_info = DeviceInfo(unit_id, [])
# #   assert isinstance(device_info, DeviceInfo)
# #   assert device_info.unit_id == unit_id
# #   assert device_info.packages == []
# #   assert device_info.custom_client_data is None

# # def test__device_info_constructor_with_packages():
# #   device_info = DeviceInfo(unit_id, packages)
# #   assert isinstance(device_info, DeviceInfo)
# #   assert device_info.unit_id == unit_id
# #   assert device_info.packages == packages
# #   assert device_info.custom_client_data is None

# # def test__device_info_constructor_with_custom_client_data():
# #   device_info = DeviceInfo(unit_id, packages, custom_client_data)
# #   assert isinstance(device_info, DeviceInfo)
# #   assert device_info.unit_id == unit_id
# #   assert device_info.packages == packages
# #   assert device_info.custom_client_data == custom_client_data

#   def test__serialize_device_info(self):
#     device_info = DeviceInfo(unit_id, packages, custom_client_data)
#     print device_info.as_json()

# # def test__deserialize_device_info():
# #   device_info = DeviceInfo(unit_id, packages, custom_client_data)
# #   assert isinstance(device_info, DeviceInfo)
# #   assert device_info.unit_id == unit_id
# #   assert device_info.packages == packages
# #   assert device_info.custom_client_data == custom_client_data

