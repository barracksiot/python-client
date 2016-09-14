import json
import requests
from apiresponse import ApiResponse
from updatedetail import UpdateDetail


class UpdateCheckHelper:
    CHECK_UPDATE_ENDPOINT = '/api/device/update/check'

    _apiKey = None
    _baseUrl = None
    _update = None

    def __init__(self, api_key, base_url):
        self._apiKey = api_key
        self._baseUrl = base_url + self.CHECK_UPDATE_ENDPOINT

    def check_update(self, update_detail_request, callback):
        """
        :type callback: function
        :type update_detail_request: UpdateDetailRequest
        """

        prepared_request = self.build_request(update_detail_request)

        # Accept certificate even if another domain than the Barracks one is used
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
            if response.status_code == 204:
                callback(ApiResponse('No update available', response.status_code))
            else:
                callback(ApiResponse('Error', response.status_code))
            return None

    def get_update(self):
        return self._update

    def build_request(self, update_detail_request):
        """
        :type update_detail_request: UpdateDetailRequest
        """
        headers = {
            'Authorization': self._apiKey,
            'Content-Type': 'application/json'
        }

        check_update_data = {
            'unitId': update_detail_request.unit_id,
            'versionId': update_detail_request.version_id,
        }
        if update_detail_request.custom_client_data is not None:
            check_update_data['customClientData'] = update_detail_request.custom_client_data

        req = requests.Request(method='POST', url=self._baseUrl, headers=headers, data=json.dumps(check_update_data))

        return req.prepare()
