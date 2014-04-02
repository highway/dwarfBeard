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



def CheckSection(CFG, sec):
	""" Check if INI section exists, if not create it """
	try:
		CFG[sec]
		return True
	except:
		CFG[sec] = {}
		return False


def check_setting_str(config, cfg_name, item_name, def_val, log=True):
	try:
		my_val = config[cfg_name][item_name]
	except:
		my_val = def_val
		try:
			config[cfg_name][item_name] = my_val
		except:
			config[cfg_name] = {}
			config[cfg_name][item_name] = my_val

	return my_val
	
def check_setting_int(config, cfg_name, item_name, def_val):
    try:
        my_val = int(config[cfg_name][item_name])
    except:
        my_val = def_val
        try:
            config[cfg_name][item_name] = my_val
        except:
            config[cfg_name] = {}
            config[cfg_name][item_name] = my_val
    
    return my_val
	