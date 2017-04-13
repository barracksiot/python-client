import os
import sched
import barracks_sdk
import time

from barracks_sdk import UpdateDetail, UpdateDetailRequest, PackageDownloadHelper, BarracksHelper, ApiResponse


def main():
    api_key = 'aa89ca0d239a2f54bce88cfa7defe3e9363a6ff181d0395eacbf9e4197420356'
    period = 25

    client = Client(api_key)
    client.check_for_updates()
    s.enter(period, 1, check_for_update, (client, period,))
    s.run()


def check_for_update(client, period):
    print("Doing stuff...")
    # do your stuff
    client.check_for_updates()
    s.enter(period, 1, check_for_update, (client, period,))


class Client:
    _api_key = None
    _base_url = None
    _destination = None
    _bh = None

    def __init__(self, api_key, base_url='https://app.barracks.io/', destination='./update_package'):
        self._api_key = api_key
        self._base_url = base_url
        self._destination = destination
        self._bh = BarracksHelper(api_key, base_url)

    def check_for_updates(self):
        # build customClientData
        custom_client_data = {'AnyCustomData': 'any_value'}

        # Perform a simple check
        request = UpdateDetailRequest('Python SDK %s' % barracks_sdk.__version__, 'unit_id_example',
                                      custom_client_data)
        ch = self._bh.update_checker_helper
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
                      % (update.get_version_id(), update.get_package_info().get_size(), self._destination,
                         update.get_package_info().get_md5()))

            # args[0] is an ApiError
            elif isinstance(args[0], ApiResponse):
                print('Message : {0} ({1})'.format(args[0].get_message(), args[0].get_error_code()))

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
    s = sched.scheduler(time.time, time.sleep)
    main()
