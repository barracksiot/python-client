import os

from Api import ApiError, UpdateDetail, UpdateDetailRequest
from Helper import BarracksHelper, PackageDownloadHelper

# Let's initialise the SDK with the API key and the base URL
bh = BarracksHelper.BarracksHelper("eafeabd7a13bacf44a8122ed4f7093c5c7b356a4f567df2654984fffef2a67be",
                                   "https://barracks.ddns.net/")


def download_package_callback(*args):
    """
    MY download package callback to handle the downloaded file
    """
    if args:  # If args is not empty.
        # args[0] is UpdateDetail"
        if isinstance(args[0], ApiError.ApiError):

            error_code = args[0].get_error_code()
            message = args[0].get_message()
            print "Error code : " + error_code if error_code is not None else ""
            print "Message : " + message if message is not None else " Error"

        else:
            # Got file path
            file_path = args[0].__str__()
            if os.path.isfile(file_path):
                print "File downloaded at " + file_path.__str__()
            else:
                print "File Error"


def check_update_callback(*args):
    """
    My check_update call back to handle new available update
    """
    if args:  # If args is not empty.
        # args[0] is UpdateDetail"
        if isinstance(args[0], UpdateDetail.UpdateDetail):
            update = args[0]
            ph = PackageDownloadHelper.PackageDownloadHelper(bh.apiKey)
            ph.download_package("./dafile", update, download_package_callback)

        # No update available or Error
        elif isinstance(args[0], ApiError.ApiError):
            error_code = args[0].get_error_code()
            message = args[0].get_message()
            print "Error code : " + error_code if error_code is not None else ""
            print "Message : " + message if message is not None else "Error without message"

        else :
            print args[0].__str__()


# Perform a simple check
request = UpdateDetailRequest.UpdateDetailRequest("v1", "MyDevice", "{\"AnyCustomData\":\"any_value\"}")
checkHelper = bh.updateCheckerHelper
checkHelper.check_update(request, check_update_callback)
