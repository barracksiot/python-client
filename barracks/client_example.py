from Api import *
from Helper import BarracksHelper, PackageDownloadHelper

# Let's initialise the SDK with the API key and the base URL
bh = BarracksHelper.BarracksHelper("eafeabd7a13bacf44a8122ed4f7093c5c7b356a4f567df2654984fffef2a67be", "https://barracks.ddns.net/")

# Perform a simple check
request = UpdateDetailRequest.UpdateDetailRequest("v1", "pod", "{}")
checkHelper = bh.updateCheckerHelper
update = checkHelper.check_update(request, None)

# If an update is available, let's download it
if update is not None:
    package_url = update.get_package_info().get_url()
    ph = PackageDownloadHelper.PackageDownloadHelper(bh.apiKey)
    ph.download_file(package_url, "./dafile")

    print("update url = %s" % package_url)
