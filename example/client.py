import argparse
import os
import sys
import imp

from barracks_sdk import BarracksUpdater, DeviceInfo, BarracksRequestException, BarracksDownloadException, BarracksChecksumException

def main():
    parser = argparse.ArgumentParser(
        description='This is an implementation example of the BarracksUpdater.'
    )
    group = parser.add_argument_group('authentication')
    group.add_argument('-a', '--api_key', help='Your Barracks API key')
    
    args = parser.parse_args()

    api_key = args.api_key

    if api_key is None:
        print('client.py -a <your_api_key>')
        sys.exit(2)
    else:
        # Let's initialise the SDK with the API key and the base URL
        try:
            updater = BarracksUpdater(api_key, 'https://barracks.ddns.net', True)
            packages = updater.get_device_packages(DeviceInfo('unitId', []))
            print 'Barracks response: ', packages
            downloadAndInstallPackages(packages['availablePackages'])
            downloadAndInstallPackages(packages['changedPackages'])
            uninstallPackages(packages['unavailableReferences'])
        except (BarracksRequestException, BarracksDownloadException, BarracksChecksumException) as e:
            print e.message

def downloadAndInstallPackages(packages):
    for package in packages:
        print 'Downloading ', package.reference, '...'
        package_file = package.download()
        installPackage(package_file)

def installPackage(package_file):
    print 'Package ', package_file.package.reference, ' is here: ', package_file.file_path

def uninstallPackages(references):
    for reference in references:
        print 'Reference ', reference, ' should be uninstall'

if __name__ == '__main__':
    main()
