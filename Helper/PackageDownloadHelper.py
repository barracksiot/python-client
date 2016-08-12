class PackageDownloadHelper: 

	_apiKey = None

	def __init__(apiKey):
		self.apiKey = apiKey
		

	def downloadPackage():
   	# Download the file
    f = self.download_file(url, headers)
    fullPath = os.path.realpath(f)

    # Get md5
    fileMd5 = hashlib.md5(open(fullPath, 'rb').read()).hexdigest()

    if md5 == fileMd5 :
        self.window.updateLabel('<span size="18000" color="#FFF">New update available for your device</span>\n<span size="14000" color="#FFF">Downloading package...</span>\n<span size="14000" color="#FFF">Package downloaded, restarting...</span>')
        time.sleep(2)

        scriptName = "/home/pi/install_update.sh %s" % fullPath

        # Call shell scrip that will unzip the file install the update
        subprocess.call([scriptName], shell=True)

    else :
        print " > Error : md5 doesn't match"


    def download_file(self, url, h):
    	
	    local_filename = "update.tar"
	    r = requests.get(url, stream=True, headers=h)
	    with open(local_filename, 'wb') as f:
	        print 'Start downloading'
	        sys.stdout.flush()
	        for chunk in r.iter_content(chunk_size=1024):
	            if chunk: # filter out keep-alive new chunks
	                f.write(chunk)

	    return local_filename	


