from Api import *
from Helper import BarracksHelper

bh = BarracksHelper.BarracksHelper("apikey", "http://barracks.ddns.net")
request = UpdateDetailRequest.UpdateDetailRequest("v1", "pod", "{}")

checkHelper = bh.updateCheckerHelper
checkHelper.check_update(request, None)
