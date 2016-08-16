class PackageInfo:
    _url = None
    _md5 = None
    _size = None

    def __init__(self, json=None):
        if json is not None:
            _url = json['packageInfo']
            _md5 = json['md5']
            _size = json['size']
