import os
import sys

import requests


class PackageDownloadHelper:
    _apiKey = None

    def __init__(self, apiKey):
        self._apiKey = apiKey

    def downloadPackage(self, temporary_path, updateDetail, callBack):
        # Download the file
        url = updateDetail.packageInfo.url
        f = self.download_file(url, temporary_path)
        fullPath = os.path.realpath(f)
        callBack(f)

    def download_file(self, url, tmpPath):
        headers = {'Authorization': self._apiKey, 'Content-Type': 'application/json'}
        r = requests.get(url, stream=True, headers=headers)
        with open(tmpPath, 'wb') as f:
            print('Start downloading')
            sys.stdout.flush()
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        return tmpPath