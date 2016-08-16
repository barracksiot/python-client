import requests

import Api


class UpdateCheckerHelper:
    _apiKey = None
    _baseUrl = None

    def __init__(self, apiKey, baseUrl):
        self._apiKey = apiKey
        self._baseUrl = baseUrl

    def checkUpdate(self, updateDetailRequest, callBack):
        headers = {'Authorization': self._apiKey, 'Content-Type': 'application/json'}

        checkUpdateData = {
            'unitId': updateDetailRequest.unitId,
            'versionId': updateDetailRequest.versionId
        }
        rep = requests.post(self._baseUrl, json=checkUpdateData, headers=headers)

        if rep.status_code == 200:
            if rep.json is not None:
                return Api.UpdateDetail(rep.json)
            else:
                print(" > Error : Response 200 without json")
        else:
            print(" > Error : status code $d" % rep.status_code)

        return None
