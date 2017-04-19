class UpdateDetailRequest:
    version_id = None
    unit_id = None
    custom_client_data = None

    def __init__(self, version_id, unit_id, custom_client_data):
        self.version_id = version_id
        self.unit_id = unit_id
        self.custom_client_data = custom_client_data
