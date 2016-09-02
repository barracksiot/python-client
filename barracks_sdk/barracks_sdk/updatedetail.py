from packageinfo import PackageInfo


class UpdateDetail:
    _packageInfo = None
    _versionId = None
    _customUpdateData = None

    def __init__(self, json=None):
        if json is not None:
            self._versionId = json['versionId']
            self._packageInfo = PackageInfo(json['packageInfo'])
            self._customUpdateData = json['customUpdateData']

    def get_package_info(self):
        return self._packageInfo

    def get_custom_update_data(self):
        return self._customUpdateData

    def get_version_id(self):
        return self._versionId
