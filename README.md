dwarfBeard
==========

A Neverwinter MMO professions manager web app with some additional features

dwarfBeard is currently an alpha release. There may be severe bugs in it and at any given time it may not work at all. 


## Features

* Multiple character support
* Web interface for management of app settings
* Add any of the standard tasks

## Project Goals

* Will manage any of the professions available
* Task prioritization to include rare tasks
* AD Exchange price trending
* Daily SCA reward collection
* and much more!


## Dependencies

To run from source you will need:

* [python 2.5+][pythonDownloads]
* [splinter][splinterDownlaods]
* [firefox][firefoxDownloads]

If you need help email me.


## Setup

By default the web interface runs at localhost:8083/
It should open automatically on the first run.
During the first run a config.ini file will be created in your dwarfBeard directory.
Before running the tasks you will need to visit the config page as set up the following at a minimum:

* ff_profile_path = "C:\Users\User\AppData\Roaming\Mozilla\Firefox\Profiles\9g8jzsay.default"
 - set this to your user profile info
 - see [FireFox Profile Manager][fireFoxProfileManager]
* nw_user_name = ""
* nw_password = ""
 - input your Neverwinter login info
* nw_account_name = ""
 - this is the account name you see once logged into the site: characterName@accountName
 
Your account information is stored on your local computer in the config.ini file.

Next you will need to choose your tasks.  The choice and priority is completely up to you.
Visit the manage page to add a character and tasks.

 
## Bugs

If you find a bug please report it or it'll never get fixed. Verify that it hasn't [already been submitted][issues] and then log a new bug. Be sure to provide as much information as possible.


## Notes

* Thanks to [midgetSpy][midgetSpy] for the inspiration


[pythonDownloads]:https://www.python.org/downloads/
[splinterDownlaods]:http://splinter.cobrateam.info/docs/
[fireFoxProfileManager]:https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles
[firefoxDownloads]:http://www.mozilla.org/en-US/firefox/new/
[issues]:https://github.com/highway/dwarfBeard/issues
[midgetSpy]:https://github.com/midgetspy
