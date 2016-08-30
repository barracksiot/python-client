class UpdateDetailRequest:
    versionId = None
    unitId = None
    customClientData = None

    def __init__(self, versionId, unitId, customClientData):
        self.versionId = versionId
        self.unitId = unitId
        self.customClientData = customClientData
