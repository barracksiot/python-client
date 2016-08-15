class PackageInfo:

	def __init__(self, json = None):
		if(json is not None):
			self.url = json['packageInfo']
			self.md5 = json['md5']
			self.size = json['size']



