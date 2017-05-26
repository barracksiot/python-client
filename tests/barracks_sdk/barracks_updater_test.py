from barracks_sdk import *
import unittest
from mock import patch, Mock, ANY, MagicMock, mock_open
import hashlib
from package_utils import build_package, build_downloadable_package
import uuid
import json
import requests_mock

class BarrackUpdaterTest(unittest.TestCase):

  default_base_url = 'https://app.barracks.io'
  base_url = 'https://not.barracks.io'
  api_key = 'qwertyuiop'
  unit_id = 'my_unit'
  json_serializer_mock = Mock()
  file_content = """
    GYUGUYFUY67867tGGUYGFYTF676t76gfHGFVYFYTF6768t7TGUGFFYFYr76r7tguyghjgvYRO
    &^^&gfvugf76tr7GJVGU&&^Tfguvuy76rtuyGVJGU&T&^ghjvuyt76fhvuyF&^TUYGUYT&UGV
    JVUYFUYVJUF&^fuyfg7fhvFU&^RUYFU&rUG*ugbvjhbvGVUYFG&^76fghjvytfd6E^YTFCVY5
    HGI&*YIUhbhjg78tgyiugBI*T&giygutyd456eDYFVJKNBJCXsterd6yufygjvhhcytDY&FYt
    GYUT^&Gjgfty5665rftyvgTSEVTdtryftugjuHGUYTE^dDFYTJHGCVFYJTykugi76UYKFVKYT
  """

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
  @patch.object(BarracksUpdater, '_convert_to_packages')
  @patch.object(JsonSerializer, 'serialize')
  def test__get_device_packages__should__post_device_info_and_return_packages(self, requests, serialize_mock, convert_to_package_mock):
    # Given
    device_packages = []
    device_info = DeviceInfo(self.unit_id, device_packages)
    api_response = {
      'available': [],
      'changed': [],
      'unchanged': [],
      'unavailable': []
    }
    serialize_mock.return_value = '{"aJson":"withValue"}'
    convert_to_package_mock.return_value = { 'availablePackages': list() }
    requests.post(
      self.default_base_url + '/api/device/resolve',
      headers={ 
        'Authorization': self.api_key, 
        'Content-type': 'application/json', 
        'Accept': 'application/json' 
      },
      additional_matcher=lambda request: serialize_mock.return_value in (request.text or ''),
      json=api_response
    )

    # When
    barracks_updater = BarracksUpdater(self.api_key)
    result = barracks_updater.get_device_packages(device_info)

    # Then
    serialize_mock.assert_called_once_with(device_info)
    convert_to_package_mock.assert_called_once_with(api_response)
    self.assertEquals(result, convert_to_package_mock.return_value)

  @requests_mock.mock()
  @patch.object(BarracksUpdater, '_convert_to_packages')
  @patch.object(JsonSerializer, 'serialize')
  def test__get_device_packages__should__raise_an_exception__when__http_request_fails(self, requests, serialize_mock, convert_to_package_mock):
    # Given
    device_packages = []
    device_info = DeviceInfo(self.unit_id, device_packages)
    serialize_mock.return_value = '{"aJson":"withValue"}'
    requests.post(
      self.default_base_url + '/api/device/resolve',
      headers={ 
        'Authorization': self.api_key, 
        'Content-type': 'application/json', 
        'Accept': 'application/json' 
      },
      additional_matcher=lambda request: serialize_mock.return_value in (request.text or ''),
      status_code=400
    )

    # When / Then
    barracks_updater = BarracksUpdater(self.api_key)
    with self.assertRaises(BarracksRequestException):
      barracks_updater.get_device_packages(device_info)

    serialize_mock.assert_called_once_with(device_info)
    convert_to_package_mock.assert_not_called

  @patch.object(BarracksUpdater, 'download_package')
  def test__convert_to_packages__should__transform_available_packages_in_json_response_in_array_of_downloadable_packages(self, download_package_mock):
    # Given
    device_packages = []
    device_info = DeviceInfo(self.unit_id, device_packages)
    available_package1 = build_downloadable_package(download_package_mock)
    available_package2 = build_downloadable_package(download_package_mock)
    json_response = {
      "available": [
        {
          "reference": available_package1.reference,
          "version": available_package1.version,
          "url": available_package1.url,
          "filename": available_package1.filename,
          "size": available_package1.size,
          "md5": available_package1.md5
        },
        {
          "reference": available_package2.reference,
          "version": available_package2.version,
          "url": available_package2.url,
          "filename": available_package2.filename,
          "size": available_package2.size,
          "md5": available_package2.md5
        }
      ],
      "changed": [],
      "unchanged": [],
      "unavailable": []
    }

    # When
    barracks_updater = BarracksUpdater(self.api_key)
    result = barracks_updater._convert_to_packages(json_response)

    # Then
    self.assertListEqual([ available_package1, available_package2 ], result['availablePackages'])
    self.assertFalse(result['changedPackages'])
    self.assertFalse(result['unchangedPackages'])
    self.assertFalse(result['unavailableReferences'])

  @patch.object(BarracksUpdater, 'download_package')
  def test__convert_to_packages__should__transform_changed_packages_in_json_response_in_array_of_downloadable_packages(self, download_package_mock):
    # Given
    device_packages = []
    device_info = DeviceInfo(self.unit_id, device_packages)
    changed_package1 = build_downloadable_package(download_package_mock)
    changed_package2 = build_downloadable_package(download_package_mock)
    json_response = {
      "changed": [
        {
          "reference": changed_package1.reference,
          "version": changed_package1.version,
          "url": changed_package1.url,
          "filename": changed_package1.filename,
          "size": changed_package1.size,
          "md5": changed_package1.md5
        },
        {
          "reference": changed_package2.reference,
          "version": changed_package2.version,
          "url": changed_package2.url,
          "filename": changed_package2.filename,
          "size": changed_package2.size,
          "md5": changed_package2.md5
        }
      ],
      "available": [],
      "unchanged": [],
      "unavailable": []
    }

    # When
    barracks_updater = BarracksUpdater(self.api_key)
    result = barracks_updater._convert_to_packages(json_response)

    # Then
    self.assertListEqual([ changed_package1, changed_package2 ], result['changedPackages'])
    self.assertFalse(result['availablePackages'])
    self.assertFalse(result['unchangedPackages'])
    self.assertFalse(result['unavailableReferences'])

  def test__convert_to_packages__should__transform_unchanged_packages_in_json_response_in_array_of_packages(self):
    # Given
    device_packages = []
    device_info = DeviceInfo(self.unit_id, device_packages)
    unchanged_package1 = build_package()
    unchanged_package2 = build_package()
    json_response = {
      "unchanged": [
        {
          "reference": unchanged_package1.reference,
          "version": unchanged_package1.version
        },
        {
          "reference": unchanged_package2.reference,
          "version": unchanged_package2.version
        }
      ],
      "available": [],
      "changed": [],
      "unavailable": []
    }

    # When
    barracks_updater = BarracksUpdater(self.api_key)
    result = barracks_updater._convert_to_packages(json_response)

    # Then
    self.assertListEqual([ unchanged_package1, unchanged_package2 ], result['unchangedPackages'])
    self.assertFalse(result['availablePackages'])
    self.assertFalse(result['changedPackages'])
    self.assertFalse(result['unavailableReferences'])

  def test__convert_to_packages__should__transform_unavailable_references_in_json_response_in_array_of_strings(self):
    # Given
    device_packages = []
    device_info = DeviceInfo(self.unit_id, device_packages)
    unavailable_package1 = str(uuid.uuid1())
    unavailable_package2 = str(uuid.uuid1())
    json_response = {
      "unavailable": [
        {
          "reference": unavailable_package1
        },
        {
          "reference": unavailable_package2
        }
      ],
      "available": [],
      "changed": [],
      "unchanged": []
    }

    # When
    barracks_updater = BarracksUpdater(self.api_key)
    result = barracks_updater._convert_to_packages(json_response)

    # Then
    self.assertListEqual([ unavailable_package1, unavailable_package2 ], result['unavailableReferences'])
    self.assertFalse(result['availablePackages'])
    self.assertFalse(result['changedPackages'])
    self.assertFalse(result['unchangedPackages'])

  @requests_mock.mock()
  @patch.object(BarracksUpdater, '_create_file_and_verify_checksum')
  def test__download_package__should__return_PackageFile__when__download_request_and_checksum_are_successful(self, requests, create_file_mock):
    # Given
    destination = '/tmp/plop'
    package = build_downloadable_package(Mock())
    expectedResult = PackageFile(destination, package)
    response = requests.get(
      package._url,
      status_code=200,
      headers={ 'Authorization': self.api_key },
      text=self.file_content
    )

    # When
    barracks_updater = BarracksUpdater(self.api_key)
    result = barracks_updater.download_package(package, destination)

    # Then
    self.assertEquals(result, expectedResult)
    create_file_mock.assert_called_once_with(ANY, destination, package._md5)

  @requests_mock.mock()
  @patch.object(BarracksUpdater, '_create_file_and_verify_checksum')
  def test__download_package__should__raise_exception__when__http_request_is_not_successful(self, requests, create_file_mock):
    # Given
    destination = '/tmp/plop'
    package = build_downloadable_package(Mock())
    expectedResult = PackageFile(destination, package)
    response = requests.get(
      package._url,
      status_code=401,
      headers={ 'Authorization': self.api_key }
    )

    # When # Then
    barracks_updater = BarracksUpdater(self.api_key)
    with self.assertRaises(BarracksDownloadException):
      barracks_updater.download_package(package, destination)

    # Then
    create_file_mock.assert_not_called()

  @patch('__builtin__.open', new_callable=mock_open())
  def test__create_file_and_verify_checksum__should__create_file__when_checksum_is_valid(self, open_mock):
    # Given
    response_content = '123'
    http_response = Mock()
    http_response.iter_content = Mock(return_value=iter([response_content]))
    destination = '/tmp/plop'
    checksum = hashlib.md5(response_content).hexdigest()

    # When
    barracks_updater = BarracksUpdater(self.api_key)
    barracks_updater._create_file_and_verify_checksum(http_response, destination, checksum)

    # Then
    open_mock.assert_called_once_with(destination, 'wb')

  def test__create_file_and_verify_checksum__should__raise_an_exception__when_checksum_is_invalid(self):
    # Given
    response_content = '123'
    http_response = Mock()
    http_response.iter_content = Mock(return_value=iter([response_content]))
    destination = '/tmp/plop'
    checksum = 'BaDch3Cksum'

    # When # Then
    barracks_updater = BarracksUpdater(self.api_key)
    with self.assertRaises(BarracksChecksumException):
      barracks_updater._create_file_and_verify_checksum(http_response, destination, checksum)

