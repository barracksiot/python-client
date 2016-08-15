class PackageDownloadHelper: 

	def __init__(apiKey):
		self.apiKey = apiKey
		

	def downloadPackage(tmpPath, finalPath, updateDetail, callBack):
   	
    url = updateDetail.packageInfo.url

    f = self.download_file(url, tmpPath)
    fullPath = os.path.realpath(f)

    callBack(f)


  def download_file(url, tmpPath):
  	
    headers = {'Authorization': self.apiKey,'Content-Type': 'application/json'}

    r = requests.get(url, stream=True, headers=headers)

    with open(tmpPath, 'wb') as f:
        print 'Start downloading'
        sys.stdout.flush()
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    
    return tmpPath	