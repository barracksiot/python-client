import json
import hashlib
import os

from mock import MagicMock
import requests_mock

from barracks_sdk import UpdateDetail, UpdateDetailRequest, PackageDownloadHelper, BarracksHelper, ApiResponse

_base_url = 'https://app.barracks.io/'
_check_update_endpoint = '/api/device/update/check'
_json_update_response = '{"packageInfo": {"size": 1925, "md5": "21fd9b37d2b458b42dc2e450699075ef", "url": "https://app.barracks.io/api/device/update/download/b640d7f2-31fd-4502-a8e1-bcf7df343f92"}, "customUpdateData": {"config": "QWERTYkeyboard"}, "versionId": "ft"}'
_helper = BarracksHelper('eafeabd7a13bacf44a8122ed4f7093c5c7b356a4f567df2654984fffef2a67be', _base_url)


def update_available_callback(result):
    assert isinstance(result, UpdateDetail) is True


def no_update_available_callback(result):
    assert isinstance(result, ApiResponse) is True
    assert result.get_error_code() is 204


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
    api_key = 'some_api_key'
    helper = BarracksHelper(api_key)
    assert helper.get_api_key() == api_key
    assert helper.get_base_url() == BarracksHelper.DEFAULT_BASE_URL


def test_init_barracks_helper_succeed_when_api_key_and_base_url_given():
    """
    Tests that the barracks helper is correctly built with an api_key and no base_url
    """
    api_key = 'some_api_key'
    base_url = 'http://some.url'
    helper = BarracksHelper(api_key, base_url)
    assert helper.get_api_key() == api_key
    assert helper.get_base_url() == base_url


def test_check_update_properly_build_request_when_no_custom_data_given():
    """
    Tests that the request is build and send with appropriate parameters and headers
    """
    request = UpdateDetailRequest('v1', 'MyDevice', None)
    update_helper = _helper.updateCheckerHelper
    built_request = update_helper.build_request(request)
    body = json.loads(built_request.body)

    assert body['unitId'] == request.unitId
    assert body['versionId'] == request.versionId
    assert 'customClientData' not in body

    headers = built_request.headers
    assert headers['Authorization'] == _helper.get_api_key()
    assert headers['Content-Type'] == 'application/json'


def test_check_update_properly_build_request_when_custom_data_given():
    """
    Tests that the request is build and send with appropriate parameters and headers
    """
    request = UpdateDetailRequest('v1', 'MyDevice', '{"AnyCustomData":"any_value"}')
    update_helper = _helper.updateCheckerHelper
    built_request = update_helper.build_request(request)
    body = json.loads(built_request.body)

    assert body['unitId'] == request.unitId
    assert body['versionId'] == request.versionId
    assert body['customClientData'] == request.customClientData

    headers = built_request.headers
    assert headers['Authorization'] == _helper.get_api_key()
    assert headers['Content-Type'] == 'application/json'


@requests_mock.mock()
def test_check_update_calls_callback_when_update_available(mocked_server):
    """
    Tests that the client ''check'' callback is called with UpdateDetail when status code is available
    """
    mocked_server.post(_base_url + _check_update_endpoint, text=_json_update_response, status_code=200)

    request = UpdateDetailRequest('v1', 'MyDevice', '{"AnyCustomData":"any_value"}')
    update_helper = _helper.updateCheckerHelper

    update_helper.check_update(request, update_available_callback)


@requests_mock.mock()
def test_check_update_calls_callback_when_no_update_available(mocked_server):
    """
    Tests that the client ''check'' callback is called with ApiResponse when status code is not available
    """
    mocked_server.post(_base_url + _check_update_endpoint, text='', status_code=204)

    request = UpdateDetailRequest('v1', 'MyDevice', '{"AnyCustomData":"any_value"}')
    update_helper = _helper.updateCheckerHelper

    update_helper.check_update(request, no_update_available_callback)


def test_download_package_properly_build_request_with_good_params():
    """
    Tests that the request is build and send with appropriate parameters and headers
    """
    update_detail = UpdateDetail(json.loads(_json_update_response))
    helper = _helper.packageDownloadHelper
    built_request = helper.build_download_request(update_detail.get_package_info().get_url())

    headers = built_request.headers
    assert headers['Authorization'] == _helper.get_api_key()
    assert built_request.url == update_detail.get_package_info().get_url()


def test_download_package_properly_calls_callback():
    """
    Tests that the client ''download'' callback is called whatever comes from Barracks API
    """
    callback_fake = MagicMock()
    update_fake = UpdateDetail(json.loads(_json_update_response))

    ph = PackageDownloadHelper(_helper.get_api_key())
    ph.download_package("./anyfile", update_fake, callback_fake)
    callback_fake.assert_called()


@requests_mock.mock()
def test_download_package_properly_calls_callback_with_good_params(m):
    """
    Tests that the client ''download'' callback is called with appropriate parameters when success
    """
    path_test = './anyfile'
    final_path = './myfile'
    test_file = open(path_test, 'a')
    test_file.close()
    callback_fake = MagicMock()
    update_fake = UpdateDetail(json.loads(_json_update_response))

    with open(path_test, 'r') as test_file :

        m.get(update_fake.get_package_info().get_url(), raw=test_file.read(), status_code=200)

        ph = PackageDownloadHelper(_helper.get_api_key())
        result = ph.download_package(final_path, update_fake, callback_fake)

        real_file_path = os.path.realpath(final_path)
        callback_fake.assert_called_with(real_file_path)

        assert result == real_file_path


def test_download_package_properly_calls_callback_with_error():
    """
    Tests that the client ''download'' callback is called with error object when fail
    """
    callback_fake = MagicMock()
    update_fake = UpdateDetail(json.loads(_json_update_response))

    ph = PackageDownloadHelper(_helper.get_api_key())
    obj = ph.download_package('./anyfile', update_fake, callback_fake)

    real_file_path = os.path.realpath('./anyfile')
    callback_fake.assert_called_with(real_file_path)


def test_download_fail_without_temporary_path():
    """
    Tests that the client ''download'' callback is called with appropriate parameters when success
    """
    callback_fake = MagicMock()
    update_fake = UpdateDetail(json.loads(_json_update_response))

    ph = PackageDownloadHelper(_helper.get_api_key())

    result = ph.download_package('', update_fake, callback_fake)

    real_file_path = os.path.realpath('/tmp/update.tmp')

    callback_fake.assert_called_with(real_file_path)
    assert result == real_file_path

    result2 = ph.download_package(None, update_fake, callback_fake)
    callback_fake.assert_called_with(real_file_path)
    assert result2 == real_file_path


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

    assert os.path.isfile(test_file_path) == False


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

    assert isinstance(result, ApiResponse) == True
