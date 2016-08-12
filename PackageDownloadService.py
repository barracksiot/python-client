class PackageDownloadService:

	def dowloadPackage(apiKey, tmpDest, finalDest, update, callback):

		local_filename = "update.tar"
	  r = requests.get(url, stream=True, headers=h)
	  
	  with open(local_filename, 'wb') as f:
      print 'Start downloading'
      sys.stdout.flush()
      for chunk in r.iter_content(chunk_size=1024):
          if chunk: # filter out keep-alive new chunks
              f.write(chunk)

	