import json
import hashlib
import os

from mock import MagicMock
import requests_mock

from barracks_sdk import UpdateDetail, UpdateDetailRequest, PackageDownloadHelper, UpdateCheckHelper, BarracksHelper, ApiResponse

_base_url = 'https://app.barracks.io/'
_check_update_endpoint = '/api/device/update/check'
_update_response_url = 'https://app.barracks.io/api/device/update/download/b640d7f2-31fd-4502-a8e1-bcf7df343f92'
_json_update_response = '{"packageInfo": {"size": 1925, "md5": "21fd9b37d2b458b42dc2e450699075ef", "url": "' + _update_response_url + '"}, "customUpdateData": {"config": "QWERTYkeyboard"}, "versionId": "ft"}'
_api_key = 'eafeabd7a13bacf44a8122ed4f7093c5c7b356a4f567df2654984fffef2a67be'
_helper = BarracksHelper(_api_key, _base_url)


def update_available_callback(result):
    assert isinstance(result, UpdateDetail)


def no_update_available_callback(result):
    assert isinstance(result, ApiResponse)
    assert result.get_error_code() is 204


def download_successful_callback(result):
    assert isinstance(result, str)


def test_init_barracks_helper_fail_when_no_api_key_given():
    """
    Tests that the barracks helper cannot be built without api_key argument
    """
    try:
        BarracksHelper(None, _base_url)
        assert False
    except ValueError:
        assert True


def test_init_barracks_helper_succeed_when_api_key_given():
    """
    Tests that the barracks helper is correctly built with an api_key and no base_url
    """
    helper = BarracksHelper(_api_key)
    assert helper.get_api_key() == _api_key
    assert helper.get_base_url() == _base_url

    assert helper.update_checker_helper
    assert helper.update_checker_helper._apiKey == _api_key
    assert helper.update_checker_helper._baseUrl == _base_url + _check_update_endpoint

    assert helper.package_download_helper
    assert helper.package_download_helper._apiKey == _api_key


def test_init_barracks_helper_succeed_when_api_key_and_base_url_given():
    """
    Tests that the barracks helper is correctly built with an api_key and no base_url
    """
    base_url = 'http://some.url'

    helper = BarracksHelper(_api_key, base_url)
    assert helper.get_api_key() == _api_key
    assert helper.get_base_url() == base_url

    assert helper.update_checker_helper
    assert helper.update_checker_helper._apiKey == _api_key
    assert helper.update_checker_helper._baseUrl == base_url + _check_update_endpoint

    assert helper.package_download_helper
    assert helper.package_download_helper._apiKey == _api_key


def test_check_update_properly_build_request_when_no_custom_data_given():
    """
    Tests that the request is build and send with appropriate parameters and headers
    """
    request = UpdateDetailRequest('v1', 'MyDevice', None)
    update_helper = UpdateCheckHelper(_api_key, _base_url)
    built_request = update_helper.build_request(request)
    body = json.loads(built_request.body)

    assert body['unitId'] == request.unit_id
    assert body['versionId'] == request.version_id
    assert 'customClientData' not in body

    headers = built_request.headers
    assert headers['Authorization'] == _api_key
    assert headers['Content-Type'] == 'application/json'


def test_check_update_properly_build_request_when_custom_data_given():
    """
    Tests that the request is build and send with appropriate parameters and headers
    """
    request = UpdateDetailRequest('v1', 'MyDevice', '{"AnyCustomData":"any_value"}')
    update_helper = UpdateCheckHelper(_api_key, _base_url)
    built_request = update_helper.build_request(request)
    body = json.loads(built_request.body)

    assert body['unitId'] == request.unit_id
    assert body['versionId'] == request.version_id
    assert body['customClientData'] == request.custom_client_data

    headers = built_request.headers
    assert headers['Authorization'] == _api_key
    assert headers['Content-Type'] == 'application/json'


@requests_mock.mock()
def test_check_update_calls_callback_when_update_available(mocked_server):
    """
    Tests that the client ''check'' callback is called with UpdateDetail when status code is available
    """
    mocked_server.post(_base_url + _check_update_endpoint, text=_json_update_response, status_code=200)

    request = UpdateDetailRequest('v1', 'MyDevice', '{"AnyCustomData":"any_value"}')
    update_helper = UpdateCheckHelper(_api_key, _base_url)

    update_helper.check_update(request, update_available_callback)


@requests_mock.mock()
def test_check_update_calls_callback_when_no_update_available(mocked_server):
    """
    Tests that the client ''check'' callback is called with ApiResponse when status code is not available
    """
    mocked_server.post(_base_url + _check_update_endpoint, text='', status_code=204)

    request = UpdateDetailRequest('v1', 'MyDevice', '{"AnyCustomData":"any_value"}')
    update_helper = UpdateCheckHelper(_api_key, _base_url)

    update_helper.check_update(request, no_update_available_callback)


def test_download_package_helper_properly_build_request_when_valid_url_given():
    """
    Tests that the download request is built with appropriate parameters and headers
    """
    download_helper = PackageDownloadHelper(_api_key)
    built_request = download_helper.build_download_request(_update_response_url)

    headers = built_request.headers
    assert headers['Authorization'] == _api_key
    assert headers['Content-Type'] == 'application/json'
    assert built_request.url == _update_response_url


def test_file_integrity_remove_file_in_case_of_fail():
    """
    Tests that downloaded the file is removed when the md5 not match
    """
    test_file = open('./testfile.tmp', 'a')
    test_file.close()
    test_file_path = os.path.realpath('./testfile.tmp')
    test_file_md5 = hashlib.md5(open(test_file_path, 'rb').read()).hexdigest()

    bad_md5 = 'some_noise_%s' % test_file_md5

    PackageDownloadHelper.check_file_integrity(test_file_path, bad_md5)

    assert not os.path.isfile(test_file_path)


def test_file_integrity_return_error_in_case_of_bad_md5():
    """
    Tests that error is return if md5 not match
    """
    test_file = open('./testfile.tmp', 'a')
    test_file.close()

    test_file_path = os.path.realpath('./testfile.tmp')
    test_file_md5 = hashlib.md5(open(test_file_path, 'rb').read()).hexdigest()

    bad_md5 = 'some_noise_%s' % test_file_md5

    result = PackageDownloadHelper.check_file_integrity(test_file_path, bad_md5)

    assert isinstance(result, ApiResponse)

