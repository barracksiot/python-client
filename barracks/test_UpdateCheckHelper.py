import json

import pytest

from Api import UpdateDetail, UpdateDetailRequest
from Helper import BarracksHelper, PackageDownloadHelper
from mock import MagicMock


@pytest.fixture()
def init_helpers_and_mocks():
    callback_fake = MagicMock()
    bh = BarracksHelper.BarracksHelper("eafeabd7a13bacf44a8122ed4f7093c5c7b356a4f567df2654984fffef2a67be",
                                       "https://barracks.ddns.net/")
    return callback_fake, bh


def test_check_update_properly_calls_callback(init_helpers_and_mocks):
    callback_fake = init_helpers_and_mocks[0]
    bh = init_helpers_and_mocks[1]

    request = UpdateDetailRequest.UpdateDetailRequest("v1", "MyDevice", "{\"AnyCustomData\":\"any_value\"}")
    helper = bh.updateCheckerHelper
    helper.check_update(request, callback_fake)
    callback_fake.assert_called()


def test_download_package_properly_calls_callback(init_helpers_and_mocks):
    callback_fake = init_helpers_and_mocks[0]
    bh = init_helpers_and_mocks[1]

    upd_response = '{"packageInfo": {"size": 1925, "md5": "21fd9b37d2b458b42dc2e450699075ef", "url": "https://barracks.ddns.net/api/device/update/download/b640d7f2-31fd-4502-a8e1-bcf7df343f92"}, "properties": {"config": "QWERTYkeyboard"}, "versionId": "ft"}'
    update_fake = UpdateDetail.UpdateDetail(json.loads(upd_response))

    ph = PackageDownloadHelper.PackageDownloadHelper(bh.apiKey)
    ph.download_package("./anyfile", update_fake, callback_fake)
    callback_fake.assert_called()


def test_download_package_properly_calls_callback_with_good_params(init_helpers_and_mocks):
    callback_fake = init_helpers_and_mocks[0]
    bh = init_helpers_and_mocks[1]

    upd_response = '{"packageInfo": {"size": 1925, "md5": "21fd9b37d2b458b42dc2e450699075ef", "url": "https://barracks.ddns.net/api/device/update/download/b640d7f2-31fd-4502-a8e1-bcf7df343f92"}, "properties": {"config": "QWERTYkeyboard"}, "versionId": "ft"}'
    update_fake = UpdateDetail.UpdateDetail(json.loads(upd_response))

    ph = PackageDownloadHelper.PackageDownloadHelper(bh.apiKey)
    result = ph.download_package("./anyfile", update_fake, callback_fake)

    callback_fake.assert_called_with("./anyfile")
    assert result == True


def test_download_package_properly_calls_callback_with_error(init_helpers_and_mocks):
    callback_fake = init_helpers_and_mocks[0]
    bh = init_helpers_and_mocks[1]

    upd_response = '{"packageInfo": {"size": 1925, "md5": "badmd5", "url": "https://barracks.ddns.net/api/device/update/download/b640d7f2-31fd-4502-a8e1-bcf7df343f92"}, "properties": {"config": "QWERTYkeyboard"}, "versionId": "ft"}'
    update_fake = UpdateDetail.UpdateDetail(json.loads(upd_response))

    ph = PackageDownloadHelper.PackageDownloadHelper(bh.apiKey)
    obj = ph.download_package("./anyfile", update_fake, callback_fake)

    callback_fake.assert_called_with(obj)
