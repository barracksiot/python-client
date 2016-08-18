class UpdateDetailRequest:
    versionId = None
    unitId = None
    properties = None

    def __init__(self, versionId, unitId, properties):
        self.versionId = versionId
        self.unitId = unitId
        self.properties = properties
