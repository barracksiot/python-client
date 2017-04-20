class Package:

  def __init__(self, reference, version):
    self._reference = reference
    self._version = version

  @property
  def reference(self):
    """Get the package reference"""
    return self._reference;

  @property
  def version(self):
    """Get the package version"""
    return self._version;