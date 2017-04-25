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


# reference = 'io.barracks.app';
# version = '1.2.3';
# url = 'https://app.barracks.io/path/to/package/version',
# filename = 'setup.sh'
# size = 9876543
# md5 = 'uhgvcfdszsewe67ygvhuioijnkl'

# def test_downloadable_package_constructor():
#   """
#   Tests that the Package class exposes reference and version property
#   """
#   package = DownloadablePackage(reference, version, url, filename, size, md5)
#   assert isinstance(package, Package)
#   assert isinstance(package, DownloadablePackage)
#   assert package.reference == reference
#   assert package.version == version
#   assert package.url == url
#   assert package.filename == filename
#   assert package.size == size
#   assert package.md5 == md5

# def test_download():
#   # package = DownloadablePackage(reference, version, url, filename, size, md5)
#   # package.download()
#   assert True