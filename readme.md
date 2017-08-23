
Real time subtitles
======


Real time subtitles is for events or conferences with audio or video screenings where translations are prepared as text but not yet time coded or embedded to video.
This application provides functionality for real time syncking ad overlaying of subtitles on video screening.

Features:
-------

*Two windows:
  * control window with context view: current subtitle highlighted in the context of and previous and upcoming subtitle lines
  * keyboard control forward, backward stepping in subtitle queue
  * subtitle window which may be overlayed to the bottom of video playing in separate player

* settings for size, color and positioning of overlaying subtitles window


Requirements
-------
* Python 2.7
* PyQt 5

Perhaps easiest to get it running is to install Anaconda python distribution


Potential issue with anaconda and windows
if error: application failed because could not load qt platform plugin "windows"
 https://github.com/ContinuumIO/anaconda-issues/issues/1270
fix:  "COPY the Continuum\Anaconda3\Library\plugins\platforms
folder to Continuum\Anaconda3
