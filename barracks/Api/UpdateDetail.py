from PackageInfo import PackageInfo


<<<<<<< HEAD
class UpdateDetail:
    _packageInfo = None
    _versionId = None
    _properties = None

    def __init__(self, json=None):
        if json is not None:
            _versionId = json['version_id']
            _packageInfo = PackageInfo(json['packageInfo'])
            _properties = json['properties']
=======
	def __init__(self, json = None):
		if(json is not None):
			self.versionId = json['version_id']
			self.packegeInfo = PackageInfo(json['packageInfo'])
			self.properties = json['properties']
>>>>>>> c16ffe4f6d746ce49fa2515d42f5243e12b525d7
