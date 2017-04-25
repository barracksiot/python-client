import uuid
from barracks_sdk import DownloadablePackage, Package

def build_downloadable_package(download_callback):
  return DownloadablePackage(
    str(uuid.uuid1()),
    str(uuid.uuid1()),
    str(uuid.uuid1()),
    str(uuid.uuid1()),
    1337,
    str(uuid.uuid1()),
    download_callback
  )

def build_package():
  return Package(
    str(uuid.uuid1()),
    str(uuid.uuid1())
  )