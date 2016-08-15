class BarracksHelper:

	_apiKey = None
	_baseUrl = None

	packageDownloadHeler = None
	updateChekerHelper = None

	def __init__( apiKey, baseUrl = None):
		self.apiKey = apiKey
		self._baseUrl = baseUrl if baseUrl is not None else "goChercherLaBaseUrlQqpart" 

		self.packageDownloadHeler = PackageDownloadHeler(apiKey)
		self.updateChekerHelper = UpdateChekerHelper(apiKey, self._baseUrl)