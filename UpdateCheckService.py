import requests


class UpdateCheckService:

	def __init__(self):


	def checkUpdate(apikey, baseUrl, request):

		headers = {'Authorization': apiKey,'Content-Type': 'application/json'}
    
    checkUpdateData = {
      'unitId': request._unitId,
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
