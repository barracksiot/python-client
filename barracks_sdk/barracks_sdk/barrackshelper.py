from packagedownloadhelper import PackageDownloadHelper
from updatecheckhelper import UpdateCheckHelper


class BarracksHelper:

    DEFAULT_BASE_URL = 'https://app.barracks.io/'

    _apiKey = None
    _baseUrl = None

    package_download_helper = None
    update_checker_helper = None

    def __init__(self, api_key, base_url=None):
        """
        :type base_url: basestring
        :type api_key: basestring
        """

        if api_key is None:
            raise ValueError("Field api_key is required")

        self._apiKey = api_key
        self._baseUrl = base_url if base_url is not None else self.DEFAULT_BASE_URL

        self.package_download_helper = PackageDownloadHelper(api_key)
        self.update_checker_helper = UpdateCheckHelper(api_key, self._baseUrl)

    def get_api_key(self):
        return self._apiKey

    def get_base_url(self):
        return self._baseUrl
