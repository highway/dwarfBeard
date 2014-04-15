dwarfBeard
==========

A Neverwinter MMO professions manager with some additional features.

In case you don't already know dwarfBeard is written in python.  Hosting this project on git hub will allow the community 
to contribute to the future of this app and for anyone to easily update to the latest version with no installation.  If you've 
never run a python web app before I encourage you to take the time to give this a try.  

When you run this app for the first time the interface should open in your web browser automatically.  After configuring your
character info and account settings you can enable the task timer on the home page.  The web interface is bare bones for now.

dwarfBeard is currently an alpha release. There may be severe bugs in it and at any given time it may not work at all. 



## Features

* Multiple character support
* Web interface for management of app settings
* Will manage any of the professions available
* Add any task. You decide the priority order
* AD Exchange price trending
* Decides when to log on again to collect rewards based on task completion time of all characters
* Random pause times for a bit of humanization



## Future Project Goals

* Daily SCA reward collection
* Twitter notifications
* and much more!


## Dependencies

To run from source you will need:

* [python 2.5+][pythonDownloads]
* [cheetah 2.4.4][cheetahDownloads]
* [splinter][splinterDownlaods]
* [firefox][firefoxDownloads]
* [tortisegit][tortisegitHome]

If you need help email me.


## Installation

If you've never used git hub or run a python program I realise this can seem a little daunting but it's worth it.
There is a whole slew of great apps out there just waiting for you to find them. (see below for some suggestions!)

Here is a quick install guide to get you on your way:

* install fire fox
* install tortisegit (actually git for windows and then tortisegit)

* install python 2.5+ (get the latest 2.x version.  Don't get 3.x as it may not work with everything as expected.)
 - make sure python is added to your system path.  Google it to find out how.
 - you must install python before you can install either of the next two python modules listed below
* download cheetah template 
 - extract cheetah to a folder such as C:\cheetah
 - open a command prompt in the folder where you extracted cheetah
 - to be sure you are in the right folder you can type 'dir' to get a list of the folder contents, setup.py should be listed.
 - at the command prompt type: python setup.py install
 - if this doesn't work python may not be in your system path
* download splinter
 - extract splinter to a folder such as C:\splinter
 - open a command prompt in the folder where you extracted splinter
 - to be sure you are in the right folder you can type 'dir' to get a list of the folder contents, setup.py should be listed.
 - at the command prompt type: python setup.py install
 - if this doesn't work python may not be in your system path

Next you'll need to clone this repository to your hard drive.  This will allow you to pull that very latest version any time you wish.
If you installed tortisegit this is really easy to do:
* copy the clone url from this projects main page: https://github.com/highway/dwarfBeard.git
* open a windows explorer to your C: drive (or where ever)
* right click and select: Git Clone
* the copied project url is probably already entered, if not, paste it and go
* thats it! all you have to do now is run dwarfbeard.py

I doubt I've covered every detail of course but this should get you well on your way.

You can email me if you need a bit of help. 
TitaniumAutomaton@gmail.com


## Configuration

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

* Other absolutely amazing projects you should really checkout:
 - [Sick Beard][sickbeardGit]
 - [Couch Potato][couchpotatoGit]
 - [Headphones][headphonesGit]
 - [Sick Beard Anime][sickbeardAnimeGit]
 - [Plex][plexApp]
 
 

[pythonDownloads]:https://www.python.org/downloads/
[cherryPyDownloads]:https://pypi.python.org/pypi/CherryPy/3.2.4
[cheetahDownloads]:http://www.cheetahtemplate.org/download.html
[splinterDownlaods]:http://splinter.cobrateam.info/docs/
[fireFoxProfileManager]:https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles
[firefoxDownloads]:http://www.mozilla.org/en-US/firefox/new/
[tortisegitHome]:https://code.google.com/p/tortoisegit/
[issues]:https://github.com/highway/dwarfBeard/issues
[midgetSpy]:https://github.com/midgetspy
[sickbeardGit]:https://github.com/midgetspy/Sick-Beard
[sickbeardAnimeGit]:https://github.com/lad1337/Sick-Beard
[headphonesGit]:https://github.com/rembo10/headphones
[couchpotatoGit]:https://github.com/RuudBurger/CouchPotatoServer
[plexApp]:https://plex.tv/
