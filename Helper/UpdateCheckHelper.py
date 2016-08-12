class UpdateCheckerHelper:

	_apiKey = None
	_baseUrl = None
	_service = UpdateCheckService()

	def __init__(apiKey, baseUrl):
		self.apiKey = apiKey
		self._baseUrl = baseUrl 

	
	def checkUpdate(updateDetailRequest):

		_service.checkUpdate(apiKey,baseUrl,updateDetailRequest)