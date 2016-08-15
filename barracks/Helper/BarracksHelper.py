class BarracksHelper:

	baseUrl = "www.baseurl-de-barracks.io"

	def __init__( apiKey, _baseUrl = None):
		self.apiKey = apiKey
		self.baseUrl = _baseUrl # BarracksHelper.baseUrl should be called if self.baseUrl is None 
		self.packageDownloadHeler = PackageDownloadHeler(apiKey)
		self.updateChekerHelper = UpdateChekerHelper(apiKey, self.baseUrl)