# Digital Forensics Scenario Creator - DFSC (formerName: fiprotima)

Browser Profile Timestamp Manipulator forked from hirthirt

A tool for viewing and manipulating browser profiles on one place.
Currently sorting profile entries domain-based and according to their timestamps.
Manipulation-wise there is already a feature to manipulate timestamps on large scale bases
thanks to the work of hirthirt

Version 0.1.0

## Currently in development

for at the least one browser type chromium or firefox - TBD

1. Performance boosting through the introduction of a multithreaded environment
2. Creation of a debug-mode (split it from the user-event log)
3. Smaller GUI improvements
   1. button placement (profile load)
   2. profile loading bar
   3. Resizing GUI fields dynamically
4. Adding another manipulating feature besides the time manipulation - TBD
   1. URL manipulation in history, form entries, Downloads, etc.
   2. Backup profile before manipulation process
   3. GUI changes for adding, deleting and changing data
5. Testing detection rate of a manipulated profile in autopsy and other forensic tools
6. Crosschecking the behavior of manipulated profiles with specific forensic test cases

### On going

- Fixing smaller bugs which will be discovered
  - TODO: Edge Downloads won't show
- Updating browser profile database changes in the browser views (browser updates)

### In future

1. Building a commit log feature for every loaded profile, which will be shown before loading new profiles --> a commit contains the changes between to profile storage points
2. Solving c-time manipulation in UNIX systems [ADD LINK]
3. GUI usability improvements

## Requirements

- Python 3
- Modules
  - SQLAlchemy
  - tksheet
  - tkcalendar
  - lz4
  - tcl
  - python-dateutil
  - pywin32
  - pypubsub
  - Pillow

## Installation Guide

Use poetry to install and manage the requirements.
Poetry will also automatically create a virtualenv for you.

**MANUAL will continue in GERMAN LANGUAGE**
TODO: to be changed to English

### Installation

Zunächst muss Python 3.8 auf dem System installiert werden (<https://www.python.org/downloads/>)
Danach muss mit pip das Modul 'pipenv' installiert werden (pip install pipenv)

Dann in diesem Ordner eine Kommandozeile öffner und mit nachfolgenden Befehlen die
virtuelle Python-Umgebung mitsamt benötigten Modulden installieren:

`pipenv install`

### Shell

Dann die virtuelle Umgebung starten:
`pipenv shell`

Deaktiviere Shell mit
`exit`

### Start

Um das Programm zu starten müssen mit folgenden Befehlen zunächst in das src/-Verzeichnis gewechselt werden
und anschliesend das Programm gestartet werden:
`cd .src/`
`python main.py`
