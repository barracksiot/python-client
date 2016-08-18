from package_download_helper import package_download_helper
from update_check_helper import update_check_helper


class barracks_helper:
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

        self.packageDownloadHelper = package_download_helper(api_key)
        self.updateCheckerHelper = update_check_helper(api_key, self._baseUrl)

    def get_api_key(self):
        return self._apiKey
