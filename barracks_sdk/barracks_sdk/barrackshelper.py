from packagedownloadhelper import PackageDownloadHelper
from updatecheckhelper import UpdateCheckHelper


class BarracksHelper:
    _apiKey = None
    _baseUrl = None

    packageDownloadHelper = None
    updateCheckerHelper = None

    def __init__(self, api_key, base_url=None):
        """

        :type base_url: basestring
        :type api_key: basestring
        """
        self.apiKey = api_key
        self._baseUrl = base_url if base_url is not None else "https://app.barracks.io/"

        self.packageDownloadHelper = PackageDownloadHelper(api_key)
        self.updateCheckerHelper = UpdateCheckHelper(api_key, self._baseUrl)

    def get_api_key(self):
        return self._apiKey
