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

import dwarfBeard

import tweet

from dwarfBeard.common import *


# online
twitter_notifier = tweet.TwitterNotifier()

notifiers = [
    twitter_notifier, 
]


def notify_download(ep_name):
    for n in notifiers:
        n.notify_download(ep_name)


def notify_snatch(ep_name):
    for n in notifiers:
        n.notify_snatch(ep_name)
