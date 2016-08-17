import requests

import Api


class UpdateCheckerHelper:
    _apiKey = None
    _baseUrl = None

    def __init__(self, api_key, base_url):
        self._apiKey = api_key
        self._baseUrl = base_url

    def check_update(self, request, callback):
        """

        :type callback: basestring
        :type request: UpdateDetailRequest
        """
        headers = {'Authorization': self._apiKey, 'Content-Type': 'application/json'}

        check_update_data = {
            'unitId': request.unitId,
            'versionId': request.versionId
        }
        print(self._baseUrl)
        rep = requests.post(self._baseUrl, check_update_data, headers=headers)

        if rep.status_code == 200:
            if rep.json is not None:
                return Api.UpdateDetail(rep.json)
            else:
                print(" > Error : Response 200 without json")
        else:
            print(" > Error : status code $d" % rep.status_code)

        return None
