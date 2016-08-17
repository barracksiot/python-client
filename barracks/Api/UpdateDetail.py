from PackageInfo import PackageInfo


class UpdateDetail:
    _packageInfo = None
    _versionId = None
    _properties = None

    def __init__(self, json=None):
        if json is not None:
            _versionId = json['version_id']
            _packageInfo = PackageInfo(json['packageInfo'])
            _properties = json['properties']