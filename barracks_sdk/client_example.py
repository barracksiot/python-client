import argparse
import os
import sys

import barracks_sdk

from barracks_sdk import UpdateDetail, UpdateDetailRequest, PackageDownloadHelper, BarracksHelper, ApiResponse


def main():
    parser = argparse.ArgumentParser(
        description='This will make a request to Barracks to check if an update is available. If yes, it will be downloaded.')
    group = parser.add_argument_group('authentication')
    group.add_argument('-a', '--api_key', help='Your Barracks API key')
    parser.add_argument('-d', '--destination', help='Destination for the downloaded package. Default: ./', default='./update_package')
    parser.add_argument('-u', '--base_url', help='Alternative URL for Barracks API. Default: http://app.barracks.io')

    args = parser.parse_args()

    api_key = args.api_key
    base_url = args.base_url
    destination = args.destination

    if api_key is None:
        print('client_example.py -a <your_api_key> -u <optionnal_alternative_base_url>')
        sys.exit(2)
    else:
        # Let's initialise the SDK with the API key and the base URL
        client = Client(api_key, base_url, destination)
        client.check_for_updates()


class Client:
    _api_key = None
    _base_url = 'http://app.barracks.io/'
    _destination = './update_package'
    _bh = None

    def __init__(self, api_key, base_url, destination):
        self._api_key = api_key
        self._base_url = base_url
        self._destination = destination
        self._bh = BarracksHelper(api_key, base_url)

    def check_for_updates(self):
        # Perform a simple check
        request = UpdateDetailRequest('Python SDK %s' % barracks_sdk.__version__, 'A device example',
                                        '{"AnyCustomData":"any_value"}')
        ch = self._bh.updateCheckerHelper
        ch.check_update(request, self.check_update_callback)

    def check_update_callback(self, *args):
        """
        Callback to handle new update from UpdateCheckerHelper.check_update
        """
        if args:
            # args[0] is an UpdateDetail
            if isinstance(args[0], UpdateDetail):
                update = args[0]
                print('downloading from %s' % update.get_package_info().get_url())
                ph = PackageDownloadHelper(self._api_key)
                ph.download_package(self._destination, update, self.download_package_callback)
                print('%s (%s bytes) has been downloaded in %s - checksum: %s'
                      % (update.get_version_id(), update.get_package_info().get_size(), self._destination, update.get_package_info().get_md5()))

            # args[0] is an ApiError
            elif isinstance(args[0], ApiResponse):
                print('Message : ' + args[0].get_message())

            else:
                print(args[0].__str__())

    def download_package_callback(*args):
        """
        Callback to handle the downloaded file
        """
        if args:
            # ApiError
            if isinstance(args[0], ApiResponse):
                print('Message : ' + args[0].get_message())

            # Got file path
            else:
                file_path = args[1].__str__()
                if os.path.isfile(file_path):
                    print('File downloaded at ' + file_path.__str__())
                else:
                    print('File Error')


if __name__ == '__main__':
    main()
