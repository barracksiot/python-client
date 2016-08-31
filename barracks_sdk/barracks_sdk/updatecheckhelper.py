import json
import requests
from apiresponse import ApiResponse
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

        prepared_request = self.build_request(request)
        response = requests.session().send(prepared_request, verify=False)

        if response.status_code == 200:
            if response.json is not None:
                self._update = UpdateDetail(response.json())
                callback(UpdateDetail(response.json()))
                return response.json()
            else:
                callback(ApiResponse(' > Error: Response 200 without json'), response.status_code)
                return None
        else:
            if response.status_code == '204':
                callback(ApiResponse('No update available', response.status_code))
            else:
                callback(ApiResponse('Error', response.status_code))
            return None

    def get_update(self):
        return self._update

    def build_request(self, request):

        headers = {'Authorization': self._apiKey, 'Content-Type': 'application/json'}

        check_update_data = {
            'unitId': request.unitId,
            'versionId': request.versionId,
            'customClientData': request.customClientData
        }

        req = requests.Request(method='POST', url=self._baseUrl, headers=headers, data=json.dumps(check_update_data))

        return req.prepare()
