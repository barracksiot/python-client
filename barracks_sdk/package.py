class Package:

  def __init__(self, reference, version):
    self.reference = reference
    self.version = version

  def __eq__(self, other):
    return self.__dict__ == other.__dict__
