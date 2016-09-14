import hashlib
import os
import sys
import requests
from apiresponse import ApiResponse


class PackageDownloadHelper:

    CHUNK_SIZE = 1024
    DEFAULT_TEMPORARY_PATH = '/tmp/update.tmp'

    _apiKey = None

    def __init__(self, api_key):
        self._apiKey = api_key

    def download_package(self, temporary_path, update_detail, callback):
        """
        :type callback: function
        :type temporary_path: string
        :type update_detail: UpdateDetail
        """
        temporary_path = self.DEFAULT_TEMPORARY_PATH if temporary_path is None else temporary_path

        # Download the file
        url = update_detail.get_package_info().get_url()
        downloaded_file = self.download_file(url, temporary_path)
        full_path = os.path.realpath(downloaded_file)

        # Check integrity of the downloaded file
        callback_arg = self.check_file_integrity(full_path, update_detail.get_package_info().get_md5())

        callback(callback_arg)
        return callback_arg

    def download_file(self, url, tmp_path):

        prepared_request = self.build_download_request(url)

        # Accept certificate even if another domain than the Barracks one is used
        response = requests.session().send(prepared_request, verify=False, stream=True)

        with open(tmp_path, 'wb') as tmp_file:
            sys.stdout.flush()
            for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    tmp_file.write(chunk)
        return tmp_path

    def build_download_request(self, url):
        """
        :type url: string
        """
        headers = {
            'Authorization': self._apiKey,
            'Content-Type': 'application/json'
        }
        req = requests.Request(method='GET', url=url, headers=headers)

        return req.prepare()

    @staticmethod
    def check_file_integrity(file_path, md5):
        """
        :type file_path: string
        :type md5: string
        """
        integrity = md5 == hashlib.md5(open(file_path, 'rb').read()).hexdigest()

        if integrity:
            return file_path
        else:
            os.remove(file_path)
            error = ApiResponse('MD5 does not match - file removed at %s' % file_path)
            return error
