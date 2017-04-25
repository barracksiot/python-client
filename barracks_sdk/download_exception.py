class BarracksDownloadException(Exception):

  def __init__(self, request, response):
    super(BarracksDownloadException, self).__init__('Request %s failed with response %s' % (request, response))