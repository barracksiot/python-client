class BarracksRequestException(Exception):

  def __init__(self, request, response):
    super(BarracksRequestException, self).__init__('Request %s failed with response %s' % (request, response))