# from barracks_sdk import Package, DownloadablePackage

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