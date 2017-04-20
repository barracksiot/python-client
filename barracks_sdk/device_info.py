class DeviceInfo:

  def __init__(self, unit_id, packages, custom_client_data=None):
    self._unit_id = unit_id
    self._packages = packages
    self._custom_client_data = custom_client_data

  @property
  def unit_id(self):
    """Get the device unit id"""
    return self._unit_id;

  @property
  def packages(self):
    """Get the list of packages installed on the device"""
    return self._packages;

  @property
  def custom_client_data(self):
    """Get the device's custom client data"""
    return self._custom_client_data;