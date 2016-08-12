class BarracksHelper:


	_apiKey = None
	_baseUrl = None


	def __init__( apiKey, baseUrl = None):

		self.apiKey = apiKey
		self._baseUrl = baseUrl if baseUrl is not None else "gochercherlabaseurlqqpart" 


	