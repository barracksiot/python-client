class UpdateDetail:

	def __init__(self, json = None):
		if(json is not None):
			self.versionId = json['version_id']
			self.packegeInfo = PackageInfo(json['packageInfo'])
			self.properties = json['properties']