import json
import requests
from apierror import ApiError
from updatedetail import UpdateDetail


class UpdateCheckHelper:
    _apiKey = None
    _baseUrl = None
    _update = None

    def __init__(self, api_key, base_url):
        self._apiKey = api_key
        self._baseUrl = base_url + 'api/device/update/check'

    def check_update(self, request, callback):
        """
        :type callback: function
        :type request: UpdateDetailRequest
        """
        headers = {'Authorization': self._apiKey, 'Content-Type': 'application/json'}

        check_update_data = {
            'unitId': request.unitId,
            'versionId': request.versionId
        }
        response = requests.post(self._baseUrl, data=json.dumps(check_update_data), headers=headers, verify=False)

        if response.status_code == 200:
            if response.json is not None:
                self._update = UpdateDetail(response.json())
                callback(UpdateDetail(response.json()))
                return response.json()
            else:
                callback(ApiError(' > Error: Response 200 without json'), response.status_code)
                return None
        else:
            callback(ApiError('Error', response.status_code))
            return None

    def get_update(self):
        return self._update
