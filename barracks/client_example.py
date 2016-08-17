from Api import *
from Helper import BarracksHelper

bh = BarracksHelper.BarracksHelper("eafeabd7a13bacf44a8122ed4f7093c5c7b356a4f567df2654984fffef2a67be", "https://barracks.ddns.net/")
request = UpdateDetailRequest.UpdateDetailRequest("v1", "pod", "{}")

checkHelper = bh.updateCheckerHelper
checkHelper.check_update(request, None)
