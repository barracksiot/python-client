[![Build Status](https://travis-ci.org/barracksiot/python-client.svg?branch=v2)](https://travis-ci.org/barracksiot/python-client) [![Coverage Status](https://coveralls.io/repos/github/barracksiot/python-client/badge.svg?branch=v2)](https://coveralls.io/github/barracksiot/python-client?branch=v2)

# Barracks Updater SDK for Python #
The Python SDK to interact with the [Barracks](https://barracks.io/) API

## Installation
```bash
pip install -e git://github.com/barracksiot/python-client.git@v2#egg=barracks_sdk
```

## Usage

### Create a Barracks SDK instance:
Get your user api key from the Account page of the [Barracks application](https://app.barracks.io/account).

#### Default Barracks SDK instance :
```python
updater = BarracksUpdater(api_key)
```

#### Custom Barracks SDK instance :
You can specify two optionnals attributes to the Barracks SDK if you want to use a proxy for your devices.
With ```base_url``` you can give the address of your proxy that use to contact Barracks, and the ```allow_self_signed``` boolean allow you to have a self signed SSL certificate on your proxy server.
Default value of ```base_url``` is ```https://app.barracks.io```.
Default value of ```allow_self_signed``` is ```false```.

```python
updater = BarracksUpdater(api_key, 'https://mycustom.domain.com', True)
```

### Check for new packages and package updates:
```python
packages = updater.get_device_packages(
    DeviceInfo(
        unit_id, 
        [ Package('com.mycompany.myapp1', '0.0.1') ], # Packages installed on the device
        { "prop1": "Value 1" } # Custom device data
    )
)
```

The return dictionary is always as follow :

```python
{
  'availablePackages': [DownloadablePackage, ...],
  'changedPackages': [DownloadablePackage, ...],
  'unchangedPackages': [Package, ...],
  'unavailableReferences': [String, ...]
}
```

### Download a package

Once you have the response from get_device_packages, you'll be able to download file for all packages that are available for the device (packages that are in the ```available```, and ```changed``` lists of the response).

The ```destination``` argument of the download function is optionnal. The default value will be as follow:
```<random-uuid>_<original-filename>```

```python
package_file = package.download(destination)
```

or

```python
package_file = updater.download_package(package, destination)
```

Error type can be one of the the following:

* `BarracksRequestException`, is returned by `BarracksUpdater.get_device_packages()` method if the HTTP response code is not `200`.
* `BarracksDownloadException`, by both `BarracksUpdater.download_package()` and `DownloadablePackage.download()` methods if the download request fails.
* `BarracksChecksumException`, is returned by both `BarracksUpdater.download_package()` and `DownloadablePackage.download()` methods if the checksum of the downloaded package is invalid.

## Docs & Community

* [Website and Documentation](https://barracks.io/)
* [Github Organization](https://github.com/barracksiot) for other official SDKs and tools

## License

  [Apache License, Version 2.0](LICENSE)
