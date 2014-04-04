dwarfBeard
==========

A Neverwinter MMO professions manager web app with some possible additional features

dwarfBeard is currently an alpha release. There may be severe bugs in it and at any given time it may not work at all. 
Currently it is only setup to manage Artificing tasks. But it does support multiple characters.

## Future Project Goals

* Web interface for management of app settings using cherrypy and cheetah
* Will manage any of the professions available
* Profession and task prioritization 
* Support for multiple browsers


## Dependencies

To run from source you will need:

* [python 2.5+][pythonDownloads]
* [splinter][splinterDownlaods]
* [firefox][firefoxDownloads]


## Setup

During the first run a config.ini file will be created in your dwarfBeard directory.
Fill in the following info into your new config.ini before attempting to start run the tasks (if you don't it's not a big deal, you just wont get very far):

* ff_profile_path = "C:\Users\User\AppData\Roaming\Mozilla\Firefox\Profiles\9g8jzsay.default"
 - set this to your user profile
 - see [FireFox Profile Manager][fireFoxProfileManager]
* nw_user_name = ""
* nw_password = ""
 - input your Neverwinter login info
* nw_account_name = ""
 - this is the account name you see once logged into the site: characterName@accountName
 
 
!!!I am in the middle of implementing the web interface and database.
If you want to use the current version you will have to manually create lists in place of the database transactions.
character names are pulled at the top of dwarfBeard.py
To change your task priority enter the task name a rank in the list at the top of artificingControl.py

Currently only Artificing tasks are supported and this is soon to change.


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
