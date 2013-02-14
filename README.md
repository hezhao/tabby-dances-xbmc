tabby-dances
============

an XBMC service addon to stream music from GrooveShark by twitting command

### Usage
1. Download and put the folder *script.service.tabbydances* under *addons* folder of your XBMC installation directory
2. Fill in the key and secrete of your twitter app as well as user token
3. Write a tweet as `"@user play <song/artist name>"`

### Notes
This is a service addon, meaning that it is executed upon XBMC starting up. You may disable this addon by

`System -> Addons -> Disabled Addons -> Service -> tabbydances -> Disable`


### Acknowledgement
Here are the libraries used, they are **already included** in the source code.
Since XBMC has its own library search path, these libraries are provided for ease of use.

- [`python-twitter`](https://github.com/bear/python-twitter) - version 2012-11-04 (Twitter API v1 support only)
- [`groove-dl`](https://github.com/jacktheripper51/groove-dl) - modified version


### License
BSD License


### Disclaimer
THIS SOFTWARE IS PROVIDED FOR PROOF OF CONCEPT PURPOSE ONLY. BY CONCEPT I MEAN ONE IS ABLE TO STEAM MUSIC FROM 
GROOVESHARK BY COMPOSE A MESSAGE ON TWITTER. I CANNOT BE HELD RESPONSIBLE FOR ANYTHING YOU DO WITH THE SOFTWARE
OR ANY CONSEQUENCES THEREOF. I DO NOT CONDONE COPYRIGHT INFRINGEMENT OR ANY OTHER ACTIVITIES WHICH VIOLATE
GROOVESHARK'S TERMS OF SERVICES.
