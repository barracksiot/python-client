import json

import pytest
from mock import MagicMock

from barracks_sdk import UpdateDetail, UpdateDetailRequest, PackageDownloadHelper, BarracksHelper, ApiResponse


@pytest.fixture()
def init_helpers_and_mocks():
    """
    Create mocked objects and fake data to be used in the tests
    """
    callback_fake = MagicMock()
    bh = BarracksHelper("eafeabd7a13bacf44a8122ed4f7093c5c7b356a4f567df2654984fffef2a67be",
                         "https://barracks.ddns.net/")
    upd_response = '{"packageInfo": {"size": 1925, "md5": "21fd9b37d2b458b42dc2e450699075ef", "url": "https://barracks.ddns.net/api/device/update/download/b640d7f2-31fd-4502-a8e1-bcf7df343f92"}, "properties": {"config": "QWERTYkeyboard"}, "versionId": "ft"}'
    update_fake = UpdateDetail(json.loads(upd_response))

    return callback_fake, bh, update_fake


def test_check_update_properly_calls_callback(init_helpers_and_mocks):
    """
    Tests that the client ''check'' callback is called whatever comes from Barracks API
    """
    callback_fake = init_helpers_and_mocks[0]
    bh = init_helpers_and_mocks[1]

    request = UpdateDetailRequest("v1", "MyDevice", "{\"AnyCustomData\":\"any_value\"}")
    helper = bh.updateCheckerHelper
    helper.check_update(request, callback_fake)
    callback_fake.assert_called()


def test_check_update_properly_build_request_with_good_params(init_helpers_and_mocks):
    """
    Tests that the request is build and send with appropriate parameters
    """
    bh = init_helpers_and_mocks[1]
    request = UpdateDetailRequest("v1", "MyDevice", "{\"AnyCustomData\":\"any_value\"}")
    helper = bh.updateCheckerHelper
    built_request = helper.build_request(request)
    body = json.loads(built_request.body)

    assert body['unitId'] == request.unitId
    assert body['versionId'] == request.versionId
    assert body['customClientData'] == request.customClientData


def test_download_package_properly_calls_callback(init_helpers_and_mocks):
    """
    Tests that the client ''download'' callback is called whatever comes from Barracks API
    """
    callback_fake = init_helpers_and_mocks[0]
    bh = init_helpers_and_mocks[1]
    update_fake = init_helpers_and_mocks[2]

    ph = PackageDownloadHelper(bh.get_api_key())
    ph.download_package("./anyfile", update_fake, callback_fake)
    callback_fake.assert_called()


def test_download_package_properly_calls_callback_with_good_params(init_helpers_and_mocks):
    """
    Tests that the client ''download'' callback is called with appropriate parameters when success
    """
    callback_fake = init_helpers_and_mocks[0]
    bh = init_helpers_and_mocks[1]
    update_fake = init_helpers_and_mocks[2]

    ph = PackageDownloadHelper(bh.get_api_key())
    result = ph.download_package("./anyfile", update_fake, callback_fake)

    callback_fake.assert_called_with("./anyfile")
    assert result == True


def test_download_package_properly_calls_callback_with_error(init_helpers_and_mocks):
    """
    Tests that the client ''download'' callback is called with error object when fail
    """
    callback_fake = init_helpers_and_mocks[0]
    bh = init_helpers_and_mocks[1]
    update_fake = init_helpers_and_mocks[2]

    ph = PackageDownloadHelper(bh.get_api_key())
    obj = ph.download_package("./anyfile", update_fake, callback_fake)

    callback_fake.assert_called_with("./anyfile")
