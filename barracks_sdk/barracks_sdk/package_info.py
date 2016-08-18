class package_info:
    _url = None
    _md5 = None
    _size = None

    def __init__(self, json=None):
        if json is not None:
            self._url = json['url']
            self._md5 = json['md5']
            self._size = json['size']

    def get_url(self):
        return self._url

    def get_md5(self):
        return self._md5

    def get_size(self):
        return self._size
