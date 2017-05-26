class PackageFile:

  def __init__(self, file_path, package):
    self.file_path = file_path
    self.package = package

  def __eq__(self, other):
    return self.__dict__ == other.__dict__
