import hashlib
import os
import sys
import requests
from apierror import ApiError


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
        # Download the file
        url = update_detail.get_package_info().get_url()
        file = self.download_file(url, temporary_path)
        full_path = os.path.realpath(file)

        if check_md5(full_path, update_detail.get_package_info().get_md5()):
            callback(file)
            return True
        else:
            error = ApiError('MD5 does not match')
            callback(error)
            return error

    def download_file(self, url, tmp_path):
        headers = {'Authorization': self._apiKey, 'Content-Type': 'application/json'}
        response = requests.get(url, stream=True, headers=headers, verify=False)
        with open(tmp_path, 'wb') as file:
            sys.stdout.flush()
            for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
        return tmp_path
