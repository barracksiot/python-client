from package_info import package_info


class update_detail:
    _packageInfo = None
    _versionId = None
    _properties = None

    def __init__(self, json=None):
        if json is not None:
            self._versionId = json['versionId']
            self._packageInfo = package_info(json['packageInfo'])
            self._properties = json['properties']

    def get_package_info(self):
        return self._packageInfo
