class UpdateDetail:

	_packegeInfo = None
	_versionId = None
	_properties = None

	def __init__(self, json = None):
		if(json is not None):
			_versionId = json['version_id']
			_packegeInfo = PackageInfo(json['packageInfo'])
			_properties = json['properties']