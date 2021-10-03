# Digital Forensics Scenario Creator - DFSC

former Name: FiProTima

Firefox Browser Profile Timestamp Manipulator forked from hirthirt - https://github.com/hirthirt/fiprotima

The vision of a one tool solution for viewing and manipulating browser profiles in one place.
Currently sorting profile entries based on there initial url access and according to their timestamps.
Manipulation-wise there is already a feature to manipulate timestamps on large scale bases
thanks to the work of @hirthirt.

Version 0.2.0

## Development Roadmap (English)

- closed task
  - PoC to verify if Multithreading is actual capable to improve the loading speed of sqlite databases
    - for at the least one browser engine type Chromium (Chrome) or Gecko (Firefox)
    - after getting not the expected results with the Firefox Gecko Engine
    - further development was based solely on the Google Chrome Browser base
  - Creation of an additional debug-mode window for more detailed and complex log messages 
    - split the ERROR/DEBUG/CRITICAL log from the user-event INFO/WARNING log
    - introduce of a second logger to completely separate them
  - Design improvements of all log messages in the gui console logger
    - enumeration feature to have a unique identifier
    - show log level information in every log message
    - add a hint to log messages which also create new log information entries in the debug-mode
  - Manual script "change_ctime.sh" in Model to solve c-time manipulation under UNIX systems
    - https://stackoverflow.com/questions/16126992/setting-changing-the-ctime-or-change-time-attribute-on-a-file/17066309#17066309
  - GUI usability improvements - closed with new toolbar interface
    - changed "profile load" button placement and redesigned toolbar + adjusted gui sections positions
    - profile loading activity indicator visualized as loading bar + redesigned toolbar(order & icons)

- open task
  - Edge Downloads won't show
  - Direct Downloads (without displaying a website) won't show inside both, the DFSC and FiProTima Software

### On going
- possible changes in the browser profile database structure after browser updates
  - updating profile database changes in the browser model and views
  - e.g. time data format mismatch in browsermodel Edge DownloadHandler

### In future

- Building a commit log feature for every loaded profile, which will be shown before loading new profiles
  - a commit contains the changes between to profile storage points
- Adding another manipulating feature besides the time manipulation - TBD
  - URL manipulation in history, form entries, Downloads, etc.
  - Backup profile before manipulation process
  - GUI changes for adding, deleting and changing data
- Testing detection rate of a manipulated profile in forensic tools with specific forensic test cases
- GUI improvements e.g. resizing GUI sections in main view dynamically

## Installationsanleitung (German)

### Öffne ein Terminal Fenster und klone das Repository:

- ```git clone UpBeatMan/Abschlussarbeit```

### Lade die Python Distribution - Anaconda Individual Edition herunter und installiere sie:

- https://www.anaconda.com/products/individual
### Gebe „Anaconda“ Rechte zur Ausführung von RemoteSigned PowerShell Skripten und initialisiere die Python Distribution – öffne dazu ein Administrator PowerShell-Terminal und gebe beide Befehle ein:

1. ```Set-ExecutionPolicy RemoteSigned```
2. ```conda init```

### Schließe das Admin-Terminal und öffne ein normales PowerShell-Terminal:

Nun sollte in der Cursor-Zeile bevor dem PS <Ordnerpfad> das Label (base) stehen. Base ist das „base“ Environment, also die Standardumgebung.

Python Pakete werden mit Anaconda in conda Umgebungen, den Environments verwaltet. Dabei werden neben den Anaconda-Paketen auch Pip-Pakete unterstützt.

Verschiedene Environments können jeweils unterschiedliche Python Versionen und Softwarepakete aus unterschiedlichen Quellen (Anaconda und Pip) zusammenfassen.

**Für das DFSC Python-Projekt wurde die Vorlage „environment.yaml“ angelegt, in der bereits alle Anaconda- und Pip-Module in ihren richtigen Versionen konfiguriert sind und auch die passende Python Version (3.9.6) festgelegt wurde.**

### Anaconda kann mit der Vorlage „environment.yaml“ über den folgenden Befehl diese Umgebung reproduzieren:

- ```conda env create --file .\Abschlussarbeit\environment.yaml```

### environment.yaml

```
1.	###############################################################################
2.	# NOTE: This file has been originally auto-generated by poetry2conda
3.	#       poetry2conda version = 0.3.0
4.	#       date: Wed Jun 30 23:59:26 2021
5.	#
6.	#       and has been manually edited by Jan Weil
7.	#       continuously during the development process
8.	#
9.	###############################################################################
10.	name: dfsc-env
11.	dependencies:
12.	  - python>=3.9.6,<4.0
13.	  - lz4>=3.1.3,<4.0.0
14.	  - python-dateutil>=2.8.2,<3.0.0
15.	  - Pillow>=8.3.1,<9.0.0
16.	  - pywin32>=228,<229
17.	  - SQLAlchemy>=1.4.22,<2.0.0
18.	  - pytest>=6.2.4,<7.0.0
19.	  - pip>=21.1.3,<22.0.0
20.	  - selenium>=3.141.0,<4.0.0
21.	  - pip:
22.	      - tksheet>=5.0.27,<6.0.0
23.	      - tkcalendar>=1.6.1,<2.0.0
24.	      - Tcl>=0.2,<0.3
25.	      - PyPubSub>=4.0.3,<5.0.0
26.	      - black>=21.7b0,<22.0+
27.
```


### Nun kann in die reproduzierte Umgebung gewechselt werden:

```conda activate dfsc-env```

Nach dem erfolgreichen Wechseln ändert sich das (base) Label zu (dfsc-env).

Eine extra Python-Installation ist nicht mehr nötig. Das Ananconda Softwarepaket installiert Python bereits.

### Starten der DFSC Software in dem "dfsc-env" conda-Environment mit den zwei Befehlen:

Zuerst muss in der Powershell-Konsole in das Verzeichnis der Git-Kopie gewechselt werden.

1. ``` cd C:\PythonProject\Abschlussarbeit\ ```

Danach kann über die conda Python-Installation die Haupt-Initdatei `__init__.py` gestartet werden.

2. ``` C:/Users/<username>/.conda/envs/dfsc-env/python.exe c:/PythonProject/Abschlussarbeit/Core/__init__.py```

Dann sollte die DFSC Software starten.

#### side information: projekt management has been outsourced to ZenHub

Please install the ZenHub Browser Addon to see the ZenHub Boards - Agile - in GitHub as a tab between PRs and Discussions.
https://chrome.google.com/webstore/detail/zenhub-for-github/ogcgkffhplmphkaahpmffcafajaocjbd

Feel free to start a new discussion. I always appreciate constructive criticism and sharing our thoughts.
