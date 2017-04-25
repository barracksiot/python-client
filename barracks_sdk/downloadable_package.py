from package import Package

class DownloadablePackage(Package):

  def __init__(self, reference, version, url, filename, size, md5, download_handler):
    Package.__init__(self, reference, version)
    self._url = url
    self._filename = filename
    self._size = size
    self._md5 = md5
    self._download_handler = download_handler

  @property
  def url(self):
    """Get the url to download the package file"""
    return self._url;

  @property
  def filename(self):
    """Get the original filename of the package"""
    return self._filename;

  @property
  def size(self):
    """Get the package's file size"""
    return self._size;

  @property
  def md5(self):
    """Get the md5 checksum of the pacakge file"""
    return self._md5;

  def download(self, destination = None):
    """Download the file available for the package"""
    return self._download_handler(self, destination)

  def __eq__(self, other): 
    return Package.__eq__(self, other)
