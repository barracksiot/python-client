from barracks_sdk import BarracksUpdater

default_base_url = 'https://app.barracks.io'
base_url = 'https://not.barracks.io'
api_key = 'qwertyuiop'

def test_barracks_updater_constructor():
  barracks_updater = BarracksUpdater(api_key)
  assert barracks_updater._api_key == api_key
  assert barracks_updater._base_url == default_base_url
  assert barracks_updater._allow_self_signed is False

def test_barracks_updater_constructor_with_base_url():
  barracks_updater = BarracksUpdater(api_key, base_url)
  assert barracks_updater._api_key == api_key
  assert barracks_updater._base_url == base_url
  assert barracks_updater._allow_self_signed is False

def test_barracks_updater_constructor_with_all_parameters():
  barracks_updater = BarracksUpdater(api_key, base_url, True)
  assert barracks_updater._api_key == api_key
  assert barracks_updater._base_url == base_url
  assert barracks_updater._allow_self_signed is True

def test_barracks_updater_get_device_packages():
  assert False