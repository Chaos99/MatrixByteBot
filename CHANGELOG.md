# MatrixByteBot Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## 0.3.8
-   added whole day events to date plugin
-   set cwd to script path to fix path bug in dates plugin

## 0.3.7
-   added auto-announce for status plugin
-   fixed some defaults in the conf file
-   improved status plugin tests

## 0.3.6
-   added ascii conf file

## 0.3.5
-   extend Status to Makerspace, identified on Channelname

## 0.3.4
-   re-organized files into folders
-   added test suite and tests for some plugins
-   added CI test tool at codacy.com
-   re-fixed encoding bug

## 0.3.3
-   removed logging by scheduler package 

## 0.3.2
-   fixed file encoding bug

## 0.3.1
-   fixed incompatibility between pathlib and python 3.5

## 0.3.0
-   added status plugin

## 0.2.4
-   fixes to make code checks happier

## 0.2.3
-   fix dates plugin help message

## 0.2.2
-   fix all-room messages
-   start-script assumes existing tmux session

## 0.2.1
-   fix check for existience of cache file

## 0.2.0
-   imported dates plugin
-   add scheduler

## 0.1.11
-   fixed update and deploy script

## 0.1.10
-   fixed accidental password leak in default settings file
-   password changed of course

## 0.1.9
-   publish license of base code

## 0.1.8
-   added start/stop/update linux script for CI
-   moved username/server/room to per-user settings file

## 0.1.7
-   added !history to maintenance plugin

## 0.1.6
-   added !about to help plugin

## 0.1.5
-   removed submodule
-   added docstrings
-   pep8 cleanup

## 0.1.4
-   added Maintenance plugin

## 0.1.3
-   added Help plugin

## 0.1.2
-   added SayHi plugin

## 0.1.1
-   added multi-plugin support
-   added multi-phrase support

## 0.1.0
-   fixed login
-   first working prototype

## 0.0.5
-   added logging for debugging
-   moved pw in non-version-controlled file

## 0.0.4
-   implementing own bot class based on bot-api example with mixed client/api access for login
-   works in interactive shell, still fails in script

## 0.0.3
-   couldn't get external Spyder with virtualenv kernel to work, including full spyder to virtualenv
-   forking matrix-bot-api and changing submodule source

## 0.0.2

-   virtualenv setup with matrix-client (via pip) and python-matrix-bot-api (via local git submodule)
-   added spyder-kernels for editing with Spyder IDE

## 0.0.1

-   Git(hub) repo creation, installation of base dependencies (Python3.6.6 via WinPython)
