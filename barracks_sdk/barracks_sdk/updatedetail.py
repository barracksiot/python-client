from packageinfo import PackageInfo


class UpdateDetail:
    _package_info = None
    _version_id = None
    _custom_update_data = None

    def __init__(self, json=None):
        if json is not None:
            self._version_id = json['versionId']
            self._package_info = PackageInfo(json['packageInfo'])
            self._custom_update_data = json['customUpdateData'] if 'customUpdateData' in json else None

    def get_package_info(self):
        return self._package_info

    def get_custom_update_data(self):
        return self._custom_update_data

    def get_version_id(self):
        return self._version_id
