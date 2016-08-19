from packageinfo import PackageInfo


class UpdateDetail:
    _packageInfo = None
    _versionId = None
    _properties = None

    def __init__(self, json=None):
        if json is not None:
            self._versionId = json['versionId']
            self._packageInfo = PackageInfo(json['packageInfo'])
            self._properties = json['properties']

    def get_package_info(self):
        return self._packageInfo
