class BarracksChecksumException(Exception):

  def __init__(self, package):
    super(BarracksChecksumException, self).__init__('Checksum verification failed for package %s' % (package.reference))
