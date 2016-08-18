Barracks SDK for Python #
The Python SDK to interact with the [Barracks](https://barracks.io/) API

## Set up ##

* Summary of set up
* Configuration
* Dependencies
* Deployment instructions

## Usage ##

### BarracksHelper ###
First you need to init a BarracksHelper with you API key 
```
#!python

barracksHelper = BarracksHelper.BarracksHelper("YOUR_API_KEY")

```

### Check for Updates ###
Check for new available updates with the UpdateCheckerHelper
```
#!python

# Perform a simple check
request = UpdateDetailRequest.UpdateDetailRequest("v1", "MyDevice", "{\"AnyCustomData\":\"any_value\"}")
checkHelper = barracksHelper.updateCheckerHelper
checkHelper.check_update(request, check_update_callback)

```

### Download Update ###
Download the package linked to an UpdateDetail with the PackageDownloadHelper
```
#!python
packageDownloadHelper = PackageDownloadHelper.PackageDownloadHelper(bh.apiKey)
packageDownloadHelper.download_package("./myUpdate", updateDetail, download_package_callback)

```

### Full example using Callbacks ###
Check & download update using callbacks 
```
#!python

def download_package_callback(*args):
    """
    Callback to handle the downloaded file from PackageDownloadHelper.download_package
    """
    if args:

        # We've got an ApiError"
        if isinstance(args[0], ApiError.ApiError):
            print "Message : " + args[0].get_message()

        # We've got the downloaded file path
        else:
            file_path = args[0].__str__()
            if os.path.isfile(file_path):
                print "File downloaded at " + file_path.__str__()
            else:
                print "File Error"

def check_update_callback(*args):
    """
    My callback to handle new update from UpdateCheckerHelper.check_update
    """
    if args:  # If args is not empty.

        # We've got an UpdateDetail
        if isinstance(args[0], UpdateDetail.UpdateDetail):
            
            # Download the file linked to this UpdateDetail
            ph = PackageDownloadHelper.PackageDownloadHelper(bh.apiKey)
            ph.download_package("./myUpdate", args[0], download_package_callback)

        # We've got an ApiError
        elif isinstance(args[0], ApiError.ApiError):
            print "Error message : " + args[0].get_message()

        else:
            print args[0].__str__()


# Call Helpers to check & download for new update
barracksHelper = BarracksHelper.BarracksHelper("YOUR_API_KEY")
request = UpdateDetailRequest.UpdateDetailRequest("v1", "MyDevice", "{\"AnyCustomData\":\"any_value\"}")
checkHelper = barracksHelper.updateCheckerHelper
checkHelper.check_update(request, check_update_callback)

```
