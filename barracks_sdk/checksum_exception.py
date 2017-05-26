class BarracksChecksumException(Exception):

  def __init__(self, calculatedChecksum, expectedChecksum):
    super(BarracksChecksumException, self).__init__('Checksum verification failed: found=%s, expected %s' % (calculatedChecksum, expectedChecksum))
