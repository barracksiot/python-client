import json

class JsonSerializer:  

  def serialize(self, obj):
    return json.dumps(obj.__dict__, default=lambda prop: prop.__dict__, sort_keys=True)
