import os

from Api import ApiError, UpdateDetail, UpdateDetailRequest
from Helper import BarracksHelper, PackageDownloadHelper

# Let's initialise the SDK with the API key and the base URL
bh = BarracksHelper.BarracksHelper("eafeabd7a13bacf44a8122ed4f7093c5c7b356a4f567df2654984fffef2a67be",
                                   "https://barracks.ddns.net/")


def download_package_callback(*args):
    """
    Callback to handle the downloaded file
    """
    if args:
        # ApiError
        if isinstance(args[0], ApiError.ApiError):
            print "Message : " + args[0].get_message()

        # Got file path
        else:
            file_path = args[0].__str__()
            if os.path.isfile(file_path):
                print "File downloaded at " + file_path.__str__()
            else:
                print "File Error"


def check_update_callback(*args):
    """
    Callback to handle new update from UpdateCheckerHelper.check_update
    """
    if args:
        # args[0] is an UpdateDetail
        if isinstance(args[0], UpdateDetail.UpdateDetail):
            update = args[0]
            ph = PackageDownloadHelper.PackageDownloadHelper(bh.apiKey)
            ph.download_package("./dafile", update, download_package_callback)

        # args[0] is an ApiError
        elif isinstance(args[0], ApiError.ApiError):
            print "Message : " + args[0].get_message()

        else:
            print args[0].__str__()


# Perform a simple check
request = UpdateDetailRequest.UpdateDetailRequest("v1", "MyDevice", "{\"AnyCustomData\":\"any_value\"}")
checkHelper = bh.updateCheckerHelper
checkHelper.check_update(request, check_update_callback)
