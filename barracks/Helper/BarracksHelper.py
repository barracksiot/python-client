import Helper


class BarracksHelper:
    _apiKey = None
    _baseUrl = None

    packageDownloadHelper = None
    updateCheckerHelper = None

    def __init__(self, apiKey, baseUrl=None):
        """

        :type apiKey: basestring
        """
        self.apiKey = apiKey
        self._baseUrl = baseUrl if baseUrl is not None else "goChercherLaBaseUrlQqpart"

        self.packageDownloadHelper = Helper.PackageDownloadHelper(apiKey)
        self.updateCheckerHelper = Helper.UpdateCheckerHelper(apiKey, self._baseUrl)
