# Torrench - Command-line torrent search tool (testing)
![Build Status](https://travis-ci.org/kryptxy/torrench.svg?branch=master)
[![GitHub release](https://img.shields.io/github/release/kryptxy/torrench.svg)]()
[![PyPI](https://img.shields.io/pypi/v/torrench.svg)](https://pypi.python.org/pypi/torrench/)
[![AUR](https://img.shields.io/aur/version/torrench.svg)](https://aur.archlinux.org/packages/torrench/)
[![PyPI](https://img.shields.io/pypi/pyversions/torrench.svg)]()
[![Dependency Status](https://gemnasium.com/badges/github.com/kryptxy/torrench.svg)](https://gemnasium.com/github.com/kryptxy/torrench)

_(This is a test branch, and is ought to be unstable. All my tests are conducted here, and final 
features are pushed onto master)_
Torrench is a command-line program to search and download torrents from torrent-hosting sites. It's compatible under **Linux and Windows** operating systems. 

* MacOS Users: I don't own a Mac hardware, so unable to test on it. But, I think it should work fine, considering the code is written keeping cross-platform in mind. Try and report back maybe? Thanks.
	* _Tested on **Yosemite** (by me as well as a user). Works great._
	* _Tested on **Sierra (10.12.6)**. Works great (Reported by a user)._

Torrents can be fetched from following websites:

1. linuxtracker.org - Download linux distros ISO torrents.
2. DistroWatch - Another linux distro ISOs repository.
3. The Pirate Bay (TPB)**\***
4. KickassTorrents (KAT)**\***
5. _More to come..._

![both](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/mix.gif)
_(Click to expand)_

### \* Using The Pirate Bay(TPB) / KickassTorrents(KAT)
By default, searching thepiratebay(TPB)/kickasstorrents(KAT) from torrench is disabled. The user should configure and enable it to use. I have provided configuration steps, but before moving to configuration, please note the following:

* Using TPB/KAT in many countries is illegal. Using TPB/KAT can get you into un-intended troubles (e.g notices/block from ISP). Read [Legal issues](https://en.wikipedia.org/wiki/The_Pirate_Bay#Legal_issues)
* Neither I, nor the tool shall be held responsible for any action taken against you for using TPB/KAT from torrench.
* Illegal searches [examples](https://github.com/kryptxy/torrench#searches-considered-illegal)
* This should be enough. Please see [Configuration steps](https://github.com/kryptxy/torrench#configuration-instructions) to enable TPB/KAT.

_Torrench initially began as a python learning project for me. I am sure there are ways to implement code I wrote in a much better/efficient way. Do [let me know](https://github.com/kryptxy/torrench#contact) or [Open issue](https://github.com/kryptxy/torrench/issues/new) if you come across any. Alternatively, you can also send a pull request._

---

## Installation/Building from Source
### Linux

* Requires [Python3](https://www.python.org/downloads/)
* Arch Users - Can install from [AUR](https://aur.archlinux.org/packages/torrench/)
* Other distro users [Ubuntu,Fedora,Suse,etc...] can use pip (python3-pip) (install/upgrade)
```
$ sudo python3 -m pip install torrench --upgrade
```
* Alternatively, build from source (python-setuptools)
```bash
$ sudo python3 setup.py install
```
	
### Windows
Windows does not require any additional packages. Everything required to run this software is provided in executable (Does not even require python pre-installed).

* Download latest [torrench executable](https://github.com/kryptxy/torrench/releases/download/v1.0.42/torrench-1.0.42.exe)
* That's it. Run using cmd/powershell [```> torrench.exe <search>```]

	* NOTE: 
		* In windows, the default location for storing [TPB] html files is ```C:\Users\<user>\.torrench\temp```

### Configuration instructions:
1. Download **config.ini** from [Sync](https://ln.sync.com/dl/26cd652e0/nqzvd8b3-9gqs3pdu-32btqm2c-9r6mbymm) / [TinyUpload](http://s000.tinyupload.com/index.php?file_id=14244138743753164476)
	* **Windows -** Copy the config file in ```C:\Users\<user>\.config\torrench\``` (create any missing directories)
	* **Linux -** Copy the config file to ```$HOME/.config/torrench/``` (Create any missing directories)
2. Enable it
	* Open config.ini file
	* Set ```enable=1```
	* Save and exit
3. That's it. 

---

## Usage
```bash
$ torrench SEARCH_STRING  ## Search linuxtracker
$ torrench -d SEARCH_STRING ## Search distrowatch
$ torrench [Options] <SEARCH_STRING>
```

## Options
```bash
  -h, --help            show this help message and exit
  
  -d, --distrowatch     Search distrowatch
  
  -t, --thepiratebay    Search thepiratebay
  
  -k, --kickasstorrent  Search KickassTorrent (KAT)
  
  -p LIMIT, --page-limit LIMIT
                        Number of pages to fetch results from (1 page = 30 results). [default: 1] [TPB]
						
  -c, --clear-html      Clear all [TPB] torrent description HTML files and exit.
						
  -v, --version         Display version and exit.
 ```

---

## Features
* Supports all \*nix distros
* Displays results in organized, tabular form.
* [linuxtracker] Supports filtering search using categories

### TPB/KAT only 
* Surf torrents Ad-free
* Fetch Torrents on basis of pages [1 page = 30 results (max)] [(-p) argument].
* **Display colored results on basis of uploader's status** (Very useful when choosing torrent).
	* TPB: 
		* VIP Uploaders [text in green]
		* Trusted Uploader [results in magenta]
		* General Uploader 
	* KAT (KickassTorrents):
		* Verified uploaders [Uploader's text in yellow]
		* Seeds [in green]
		* Leeches [in red]
* Add torrent directly to torrent client through **magnetic links** without opening/fetching details.
* Get upstream link which can be opened using browser.

**[TPB-Only]**
* Get complete torrent details (Description, comments, torrent download). **Torrent details are available in dynamically-generated HTML pages.**

* Fetch Comments on basis of pages [Useful when torrent has large number of comments, and not all comments are intended to be fetched].

### Note
* A torrent might take long to fetch results. I have generally faced this issue when running torrench for the first time. When this happens:
	* Abort the ongoing search [Ctrl+C]
	* Search again. The second time generally works fine.
* KAT Proxy is quite shaky, and might not work at all times. I have been unable to find any reliable KAT proxy. If you know of some working proxy, you can edit KAT_URL in config.ini  with that working proxy and hope that works (If it does, let me know?). Alternatively, use TPB. It's pretty reliable and works most of the time.
	
---

## Examples

```bash
$ torrench "ubuntu desktop 16.04"	## Search Linuxtracker for Ubuntu Desktop 16.04 distro ISO
$ torrench "fedora workstation"	## Search for Fedora Workstation distro ISO
$ torrench -d "opensuse" ## Search distrowatch for opensuse ISO
$ torrench -d "solus" ## Search distrowatch for solus ISO
```
#### Linuxtracker

![ubuntu](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/ubuntu.png)
![fedora](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/linux.gif)

#### DistroWatch

![distrowatch](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/distrowatch.png)
![distrowatch](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/distrowatch.gif)
---
### Searches considered illegal
#### TPB Examples
```bash
$ torrench -t "suicide squad"	## Search suicide squad TPB
$ torrench -t "game of thrones s07e02" -p 2	## Search and fetch 2 pages TPB for GOT s07e02
```
![illegal](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/tpb.png)

![illegal](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/html.png)
_(Dynamically-generated Torrent description HTML page)_ 

![illegal](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/got.gif)
_(Click to expand)_

#### KAT Examples
```bash
$ torrench -k "doctor strange"
$ torrench -k "guardians of the galaxy"
```
![illegal](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/kat.png)

![illegal](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/kat.gif)
_(Click to expand)_

---

## Disclaimer
This tool fetches torrent and details from already existing torrent website(s). I do not take any responsibility for availability of any kind of torrent data, or/and hosting of any torrent website(s). Also, I am  not responsible for closing of any of the torrent website(s). As long as the website(s) (proxies) are available, data will be fetched.

## Bug Report and/or Feedback
Found a bug? Please report and help improving this tool. You can [Open Issue](https://github.com/kryptxy/torrench/issues/new) or contact me directly.
Feedbacks/Suggestions are much appreciated. They help in improving the tool, and keep me motivated. 

## Contact
E-mail : kryptxy@protonmail.com

## Licence
```
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>

Torrench is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Torrench is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Torrench.  If not, see <http://www.gnu.org/licenses/>.
```
