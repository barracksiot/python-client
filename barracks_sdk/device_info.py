import json

class DeviceInfo:

  def __init__(self, unit_id, packages, custom_client_data=None):
    self.unit_id = unit_id
    self.packages = packages
    self.custom_client_data = custom_client_data
