class DeviceInfo:

  def __init__(self, unit_id, packages, custom_client_data = {}):
    self.unitId = unit_id
    self.packages = packages
    self.customClientData = custom_client_data
