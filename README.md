dwarfBeard
==========

A Neverwinter MMO professions manager web app with some additional features.

In case you don't already know dwarfBeard is written in python.  Hosting this project on git hub will allow the community 
to contribute to the future of this app and for anyone to easily update to the latest version with no installation.  
When you run this app for the first time the interface should open in your web browser automatically.  After configuring your
character info and account settings you can enable the task timer on the home page.  The web interface is bare bones for now.


dwarfBeard is currently an alpha release. There may be severe bugs in it and at any given time it may not work at all. 



## Features

* Multiple character support
* Web interface for management of app settings
* Will manage any of the professions available
* Add any task. You decide the priority order
* AD Exchange price trending
* Decides when to log on again to collect rewards
* Random wait times



## Future Project Goals

* Daily SCA reward collection
* Twitter notifications
* and much more!


## Dependencies

To run from source you will need:

* [python 2.5+][pythonDownloads]
* [cherryPy 3+][cherryPyDownloads]
* [cheetah 2.4.4][cheetahDownloads]
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
* Visit the manage page to add a character and tasks.
* Add your character name(s) first
* Add your tasks in the order of priority

 
## Bugs

If you find a bug please report it or it'll never get fixed. Verify that it hasn't [already been submitted][issues] and then log a new bug. Be sure to provide as much information as possible.


## Notes

* Thanks to [midgetSpy][midgetSpy] for the inspiration


[pythonDownloads]:https://www.python.org/downloads/
[cherryPyDownloads]:https://pypi.python.org/pypi/CherryPy/3.2.4
[cheetahDownloads]:http://www.cheetahtemplate.org/download.html
[splinterDownlaods]:http://splinter.cobrateam.info/docs/
[fireFoxProfileManager]:https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles
[firefoxDownloads]:http://www.mozilla.org/en-US/firefox/new/
[issues]:https://github.com/highway/dwarfBeard/issues
[midgetSpy]:https://github.com/midgetspy
