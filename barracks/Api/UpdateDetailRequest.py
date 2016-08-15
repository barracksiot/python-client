class UpdateDetailRequest:

	_versionId = None
	_unitId = None
	_properties = None

	def __init__(versionId, unitId, properties):
		self._versionId = versionId
		self._unitId = unitId
		self._properties = properties 
