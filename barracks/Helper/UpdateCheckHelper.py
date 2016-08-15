import requests
class UpdateCheckerHelper:

	def __init__(apiKey, baseUrl):
		self.apiKey = apiKey
		self.baseUrl = baseUrl 

	
	def checkUpdate(updateDetailRequest, callBack):

		headers = {'Authorization': self._apiKey,'Content-Type': 'application/json'}
    
    checkUpdateData = {
      'unitId': request.unitId,
      'versionId': request.versionId
    }

    rep = requests.post(baseUrl, json=checkUpdateData, headers=headers)

    if rep.status_code == 200 :
        
      if rep.json is not None :

      	return UpdateDetail(rep.json)
        
      else :
          print " > Error : Response 200 without json"

    else :
        print " > Error : status code $d" % rep.status_code

    return None
