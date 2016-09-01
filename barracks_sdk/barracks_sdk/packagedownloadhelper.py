import hashlib
import os
import sys
import requests
from apiresponse import ApiResponse


def check_md5(file_path, md5):
    return md5 == hashlib.md5(open(file_path, 'rb').read()).hexdigest()


class PackageDownloadHelper:
    _apiKey = None
    CHUNK_SIZE = 1024

    def __init__(self, api_key):
        self._apiKey = api_key

    def download_package(self, temporary_path, update_detail, callback):
        """
        :type callback: function
        :type temporary_path: string
        :type update_detail: UpdateDetail
        """
        temporary_path = "/tmp/update.tmp" if temporary_path is None or temporary_path == "" else temporary_path

        # Download the file
        url = update_detail.get_package_info().get_url()
        file = self.download_file(url, temporary_path)
        full_path = os.path.realpath(file)

        if check_md5(full_path, update_detail.get_package_info().get_md5()):
            callback(file)
            return True
        else:
            error = ApiResponse('MD5 does not match')
            callback(error)
            return error

    def download_file(self, url, tmp_path):

        prepared_request = self.build_download_request(url)

        # Accept certificate even if another domain than the Barracks one is used
        response = requests.session().send(prepared_request, verify=False, stream=True)

        with open(tmp_path, 'wb') as file:
            sys.stdout.flush()
            for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
        return tmp_path

    def build_download_request(self, url):
        """
        :type url: string
        """

        headers = {'Authorization': self._apiKey, 'Content-Type': 'application/json'}
        req = requests.Request(method='GET', url=url, headers=headers)

        return req.prepare()
