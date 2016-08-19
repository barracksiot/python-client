import json
import requests
from apierror import ApiError
from updatedetail import UpdateDetail


class UpdateCheckHelper:
    _apiKey = None
    _baseUrl = None

    def __init__(self, api_key, base_url):
        self._apiKey = api_key
        self._baseUrl = base_url + "api/device/update/check"

    def check_update(self, request, callback):
        """

        :type callback: function
        :type request: updatedetailrequest.UpdateDetailRequest
        """
        headers = {'Authorization': self._apiKey, 'Content-Type': 'application/json'}

        check_update_data = {
            'unitId': request.unitId,
            'versionId': request.versionId
        }
        print(self._baseUrl)
        rep = requests.post(self._baseUrl, data=json.dumps(check_update_data), headers=headers, verify=False)
        print("json %s" % rep.json)

        if rep.status_code == 200:
            if rep.json is not None:
                callback(UpdateDetail(rep.json()))
                return rep.json()
            else:
                callback(ApiError(" > Error: Response 200 without json"), rep.status_code)
                return rep.json()
        else:
            callback(ApiError("Error", rep.status_code))
            return rep.json()
