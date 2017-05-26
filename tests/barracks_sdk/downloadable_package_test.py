import unittest
from mock import patch, Mock
from package_utils import build_package, build_downloadable_package
from barracks_sdk import DownloadablePackage

class DownloadablePackageTest(unittest.TestCase):

  def test__download__should__call_the_received_callback(self):
    # Given
    expected_result = 'The result'
    callback = Mock(return_value=expected_result)
    package = build_downloadable_package(callback)
    location = '/tmp/plop.txt'

    # When
    result = package.download(location)

    # Then
    self.assertEquals(result, expected_result)
    callback.assert_called_once_with(package, location)
