import requests
import uuid
import os
import md5
import hashlib
from device_info import DeviceInfo
from package import Package
from downloadable_package import DownloadablePackage
from package_file import PackageFile
from request_exception import BarracksRequestException
from download_exception import BarracksDownloadException
from checksum_exception import BarracksChecksumException
from json_serializer import JsonSerializer

class BarracksUpdater:

  DEFAULT_BASE_URL = 'https://app.barracks.io'
  GET_DEVICE_PACKAGES_ENDPOINT = '/api/device/resolve'

  def __init__(self, api_key, base_url = DEFAULT_BASE_URL, allow_self_signed = False):
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
      headers = {
        'Authorization': self._api_key,
        'Content-type': 'application/json',
        'Accept': 'application/json'
      },
      data = self._json_serializer.serialize(device_info),
      verify = not self._allow_self_signed
    )
    if response.status_code == 200:
      return self._convert_to_packages(response.json())
    else:
      raise BarracksRequestException(response.request.body, response.text)

  def _convert_to_packages(self, json_response):
    return {
      'availablePackages': list(map(lambda item: self._build_downloadable_package(item), json_response['available'])),
      'changedPackages': list(map(lambda item: self._build_downloadable_package(item), json_response['changed'])),
      'unchangedPackages': list(map(lambda item: self._build_package(item), json_response['unchanged'])),
      'unavailableReferences': list(map(lambda item: item['reference'], json_response['unavailable']))
    }

  def _build_downloadable_package(self, dictionary):
    return DownloadablePackage(
      dictionary['reference'],
      dictionary['version'],
      dictionary['url'],
      dictionary['filename'],
      dictionary['size'],
      dictionary['md5'],
      self.download_package
    )

  def _build_package(self, dictionary):
    return Package(
      dictionary['reference'],
      dictionary['version']
    )

  def download_package(self, package, destination = None):
    destination = destination or (str(uuid.uuid1()) + package._filename)
    response = requests.get(
      package._url,
      headers = {
        'Authorization': self._api_key
      },
      verify = not self._allow_self_signed,
      stream = True
    )
    if response.status_code == 200:
      self._create_file_and_verify_checksum(response, destination, package._md5)
      return PackageFile(destination, package)
    else:
      raise BarracksDownloadException(response.request.body, response.text)

  def _create_file_and_verify_checksum(self, http_response, destination, checksum):
    hash_md5 = hashlib.md5()
    with open(destination, 'wb') as f:
      for chunk in http_response.iter_content(1024):
        f.write(chunk)
        hash_md5.update(chunk)
    if hash_md5.hexdigest() != checksum:
      os.remove(destination)
      raise BarracksChecksumException(hash_md5.hexdigest(), checksum)
