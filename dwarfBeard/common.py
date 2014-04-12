#
# This file is part of dwarfBeard.
#
# dwarfBeard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dwarfBeard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See <http://www.gnu.org/licenses/> for license information.


import os.path
import operator
import platform
import re


### Notification Types
NOTIFY_LEVELUP = 1
NOTIFY_RARETASK = 2

notifyStrings = {}
notifyStrings[NOTIFY_LEVELUP] = "A profession just levelled up"
notifyStrings[NOTIFY_RARETASK] = "Just completed another rare task"


# Get our xml namespaces correct for lxml
XML_NSMAP = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
             'xsd': 'http://www.w3.org/2001/XMLSchema'}


countryList = {'Australia': 'AU',
               'Canada': 'CA',
               'USA': 'US'
               }
